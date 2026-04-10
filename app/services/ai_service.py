import asyncio
from typing import Optional, List
from app.core.config import settings
from app.utils.logger import logger


class AIService:
    def __init__(self) -> None:
        self.backend = settings.ai_backend
        self._cohere = None

    async def summarize(
        self,
        text: str,
        max_length: Optional[int] = 500,
        focus_areas: Optional[List[str]] = None,
    ) -> dict:
        if self.backend == "stub":
            return await self._stub_summarize(text, max_length, focus_areas)
        if self.backend == "cohere":
            return await self._run_with_fallback("summarize", text=text, max_length=max_length, focus_areas=focus_areas)
        raise ValueError(f"Unknown AI_BACKEND: '{self.backend}'")

    async def ask(self, question: str, context: str) -> dict:
        if self.backend == "stub":
            return await self._stub_ask(question, context)
        if self.backend == "cohere":
            return await self._run_with_fallback("ask", question=question, context=context)
        raise ValueError(f"Unknown AI_BACKEND: '{self.backend}'")

    async def _run_with_fallback(self, operation: str, **kwargs) -> dict:
        try:
            instance = self._get_cohere()
            method = getattr(instance, operation)
            result = await method(**kwargs)
            logger.info("AI request succeeded", extra={"backend": "cohere", "operation": operation})
            return result
        except Exception as exc:
            logger.warning(f"Cohere failed: {exc}")
            raise RuntimeError(f"Cohere backend failed: {exc}") from exc

    def _get_cohere(self):
        if self._cohere is None:
            from app.services.backends.cohere_backend import CohereBackend
            self._cohere = CohereBackend()
        return self._cohere

    async def _stub_summarize(self, text, max_length, focus_areas) -> dict:
        await asyncio.sleep(0.15)
        word_count = len(text.split())
        focus_str = ", ".join(focus_areas) if focus_areas else "none"
        return {
            "summary": (
                f"[PHASE 1 STUB] Document has {word_count} words. "
                f"Focus areas: {focus_str}. "
                f"Real AI summary will appear in Phase 2."
            ),
            "key_points": [
                "Key point 1 — will be extracted by AI in Phase 2",
                "Key point 2 — will be extracted by AI in Phase 2",
                "Key point 3 — will be extracted by AI in Phase 2",
                "Key point 4 — will be extracted by AI in Phase 2",
                "Key point 5 — will be extracted by AI in Phase 2",
            ],
            "model_used": "stub-v1",
        }

    async def _stub_ask(self, question: str, context: str) -> dict:
        await asyncio.sleep(0.15)
        return {
            "answer": (
                f"[PHASE 1 STUB] Question was: '{question}'. "
                f"Context was {len(context.split())} words. "
                f"Real RAG-based answer will appear in Phase 2."
            ),
            "confidence": 0.0,
            "sources": ["stub — no retrieval in Phase 1"],
            "model_used": "stub-v1",
        }