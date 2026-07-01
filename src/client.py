from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY

MODEL = "gemini-2.5-flash"


class GeminiClient:
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = MODEL):
        self.model = model
        self._client = genai.Client(api_key=api_key)

    def send_message(self, contents, tools=None, system_instruction=None):
        config = types.GenerateContentConfig(
            tools=tools,
            system_instruction=system_instruction,
        )
        return self._client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )
