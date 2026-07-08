import json
import logging
from typing import Any, AsyncGenerator, Optional

import httpx

from vanna import LlmRequest, LlmService, LlmStreamChunk, LlmResponse

logger = logging.getLogger(__name__)


class OpenAILlmService(LlmService):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        temperature: float = 0.1,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature

    def _build_messages(self, request: LlmRequest) -> list:
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        for m in request.messages:
            role = "assistant" if m.role == "assistant" else m.role
            messages.append({"role": role, "content": m.content})
        return messages

    def send_request(self, request: LlmRequest) -> LlmResponse:
        messages = self._build_messages(request)
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"] or ""
        return LlmResponse(content=content)

    async def stream_request(
        self, request: LlmRequest
    ) -> AsyncGenerator[LlmStreamChunk, None]:
        messages = self._build_messages(request)
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            yield LlmStreamChunk(finish_reason="stop")
                            return
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0]["delta"]
                            if delta.get("content"):
                                yield LlmStreamChunk(content=delta["content"])
                            if data["choices"][0].get("finish_reason"):
                                yield LlmStreamChunk(
                                    finish_reason=data["choices"][0]["finish_reason"]
                                )
                        except json.JSONDecodeError:
                            continue

    def validate_tools(self, tool_names: list[str]) -> list[str]:
        return tool_names
