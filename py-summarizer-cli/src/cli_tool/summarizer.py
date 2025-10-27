from __future__ import annotations
import math
import re
from collections import Counter
from typing import List, Tuple, Dict

_SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')
_WORD_RE = re.compile(r"[A-Za-z0-9']+")

def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    sents = _SENT_SPLIT_RE.split(text)
    # Filter very short fragments
    return [s.strip() for s in sents if len(s.strip()) > 1]

def tokenize(text: str) -> List[str]:
    return [w.lower() for w in _WORD_RE.findall(text)]

def compute_word_scores(tokens: List[str]) -> Dict[str, float]:
    # Simple frequency with log dampening
    freq = Counter(tokens)
    total = sum(freq.values()) or 1
    scores = {}
    for w, c in freq.items():
        scores[w] = (1 + math.log(1 + c)) / total
    return scores

def select_top_sentences(sentences: List[str], scores: Dict[str, float], k: int) -> List[str]:
    # Rank by sum of token scores normalized by length
    def score_sent(s: str) -> float:
        toks = tokenize(s)
        if not toks: return 0.0
        return sum(scores.get(t, 0.0) for t in toks) / math.sqrt(len(toks))
    ranked = sorted(sentences, key=score_sent, reverse=True)
    # Keep original order for readability
    top = set(ranked[:k])
    return [s for s in sentences if s in top][:k]

def extract_keywords(tokens: List[str], top_n: int = 10) -> List[str]:
    freq = Counter(t for t in tokens if len(t) > 3)
    return [w for w, _ in freq.most_common(top_n)]

def summarize_and_insights(text: str, max_sentences: int = 5, insights_n: int = 5):
    sentences = split_sentences(text)
    tokens = tokenize(text)
    word_scores = compute_word_scores(tokens)
    summary_sents = select_top_sentences(sentences, word_scores, max_sentences)
    summary = " ".join(summary_sents)

    # Insights: pick top sentences not necessarily in summary; diversify
    remaining = [s for s in sentences if s not in summary_sents]
    insight_pool = summary_sents + remaining  # prioritize summary sentences
    insights = []
    seen = set()
    for s in insight_pool:
        # Turn to bullet-like phrasing (trim and ensure uniqueness)
        point = s.strip()
        if point and point.lower() not in seen:
            insights.append(point)
            seen.add(point.lower())
        if len(insights) >= insights_n:
            break

    keywords = extract_keywords(tokens, top_n=10)

    return {
        "summary": summary,
        "key_insights": insights,
        "top_keywords": keywords,
        "sentence_count": len(sentences),
        "word_count": len(tokens),
    }
