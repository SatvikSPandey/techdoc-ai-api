import json
import re
from typing import Any


def parse_llm_json(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("LLM returned an empty response.")

    # Strategy 1: direct parse
    result = _try_parse(text.strip())
    if result is not None:
        return result

    # Strategy 2: strip markdown code fences
    cleaned = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    result = _try_parse(cleaned)
    if result is not None:
        return result

    # Strategy 3: extract first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        result = _try_parse(match.group())
        if result is not None:
            return result

    raise ValueError(f"Could not parse JSON from LLM response. First 200 chars: {text[:200]!r}")


def _try_parse(text: str) -> Any | None:
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        return None
    except (json.JSONDecodeError, ValueError):
        return None