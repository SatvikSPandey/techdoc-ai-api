import cohere
from typing import Optional, List
from app.core.config import settings
from app.utils.prompt_templates import SUMMARIZE_SYSTEM, ASK_SYSTEM, build_summarize_prompt, build_ask_prompt
from app.utils.json_parser import parse_llm_json
from app.utils.logger import logger


class CohereBackend:
    MODEL = "command-r-08-2024"

    def __init__(self) -> None:
        if not settings.cohere_api_key:
            raise ValueError("COHERE_API_KEY is not set in .env file.")
        self._client = cohere.AsyncClient(api_key=settings.cohere_api_key)
        logger.info("Cohere backend initialised", extra={"model": self.MODEL})

    async def summarize(
        self,
        text: str,
        max_length: Optional[int] = 500,
        focus_areas: Optional[List[str]] = None,
    ) -> dict:
        user_prompt = build_summarize_prompt(text, max_length, focus_areas)

        logger.info("Sending summarize request to Cohere", extra={"model": self.MODEL})

        response = await self._client.chat(
            model=self.MODEL,
            preamble=SUMMARIZE_SYSTEM,
            message=user_prompt,
        )

        raw_text = response.text
        parsed = parse_llm_json(raw_text)

        return {
            "summary": parsed.get("summary", "Summary not available."),
            "key_points": parsed.get("key_points", []),
            "model_used": self.MODEL,
        }

    async def ask(self, question: str, context: str) -> dict:
        user_prompt = build_ask_prompt(question, context)

        logger.info("Sending ask request to Cohere", extra={"model": self.MODEL})

        response = await self._client.chat(
            model=self.MODEL,
            preamble=ASK_SYSTEM,
            message=user_prompt,
        )

        raw_text = response.text
        parsed = parse_llm_json(raw_text)

        return {
            "answer": parsed.get("answer", "Could not generate an answer."),
            "confidence": float(parsed.get("confidence", 0.0)),
            "sources": parsed.get("sources", []),
            "model_used": self.MODEL,
        }

    async def close(self) -> None:
        await self._client.close()