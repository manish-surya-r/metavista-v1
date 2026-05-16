from __future__ import annotations

import httpx


class OpenAICompatibleClient:
    def __init__(self, api_key: str | None, base_url: str, model: str, provider_name: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.provider_name = provider_name

    async def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.25) -> str:
        if not self.api_key:
            raise RuntimeError(f'{self.provider_name} API key is missing')

        url = f'{self.base_url}/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': self.model,
            'temperature': temperature,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
