from __future__ import annotations
import os

class OptionalOpenAIClient:
    """
    A tiny wrapper that uses OpenAI if available and configured; otherwise it no-ops.
    This ensures the CLI can run end-to-end in offline environments.
    """
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._use_openai = False
        self._client = None
        key = os.getenv("OPENAI_API_KEY", "")
        if key:
            try:
                import openai  # type: ignore
                self._client = openai
                self._use_openai = True
            except Exception:
                # openai lib not installed or import error — fallback silently
                self._client = None
                self._use_openai = False

    def available(self) -> bool:
        return self._use_openai and (self._client is not None)

    def summarize(self, text: str, max_sentences: int = 5, insights_n: int = 5):
        if not self.available():
            return None  # caller should fallback
        prompt = (
            "Summarize the following text in up to "
            f"{max_sentences} sentences and provide {insights_n} bullet-point insights.\n\n"
            f"Text:\n{text}\n"
        )
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a concise assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content.strip()
            lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
            summary_lines = []
            insights = []
            for ln in lines:
                if ln.startswith("-") or ln.startswith("*"):
                    insights.append(ln.lstrip("-* ").strip())
                else:
                    summary_lines.append(ln)
            if not insights and len(lines) > 1:
                insights = lines[1: 1 + insights_n]
            summary = " ".join(summary_lines[:max_sentences])
            return {"summary": summary, "key_insights": insights[:insights_n]}
        except Exception:
            return None  # any error -> fallback
