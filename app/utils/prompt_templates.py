from typing import Optional, List

SUMMARIZE_SYSTEM = """You are a technical document analyst specializing in engineering documentation. You extract key information accurately and concisely. You never add information that is not present in the document."""

def build_summarize_prompt(text: str, max_length: int, focus_areas: Optional[List[str]] = None) -> str:
    focus_instruction = ""
    if focus_areas:
        focus_instruction = f"\nPay special attention to these areas: {', '.join(focus_areas)}."

    return f"""Analyze the following technical document and produce a structured summary.{focus_instruction}

Your summary must be a maximum of {max_length} words.
Extract exactly 5 key points as short specific statements.

Respond ONLY with valid JSON — no extra text, no markdown code fences.
Use exactly this structure:

{{
  "summary": "Your concise summary here",
  "key_points": [
    "First key point",
    "Second key point",
    "Third key point",
    "Fourth key point",
    "Fifth key point"
  ]
}}

DOCUMENT:
{text}"""


ASK_SYSTEM = """You are a technical document expert. You answer questions based strictly on the provided document. You do not use external knowledge. If the answer is not in the document, say so clearly."""

def build_ask_prompt(question: str, context: str) -> str:
    return f"""Answer the following question using ONLY the information in the document below.

If the document clearly states the answer, provide it with confidence close to 1.0.
If the answer cannot be found, respond with confidence 0.0.

Respond ONLY with valid JSON — no extra text, no markdown code fences.
Use exactly this structure:

{{
  "answer": "Your answer here",
  "confidence": 0.85,
  "sources": [
    "Exact quote from the document that supports the answer"
  ]
}}

DOCUMENT:
{context}

QUESTION: {question}"""