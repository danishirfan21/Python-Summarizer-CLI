from __future__ import annotations
import argparse
import os
from typing import Dict, Any, List

from .io_utils import read_text, ensure_dir, stem_name, write_json, write_csv
from .summarizer import summarize_and_insights
from .openai_client import OptionalOpenAIClient

def run_cli(args: argparse.Namespace) -> Dict[str, Any]:
    text = read_text(args.input)
    outdir = args.outdir or "out"
    ensure_dir(outdir)
    base = stem_name(args.input)

    # Try OpenAI (optional)
    use_openai = args.use_openai
    openai_model = args.model
    openai_client = OptionalOpenAIClient(model=openai_model)

    summary_data = None
    if use_openai and openai_client.available():
        ai = openai_client.summarize(text, max_sentences=args.max_sentences, insights_n=args.insights)
        if ai:
            summary_data = {
                "summary": ai.get("summary", ""),
                "key_insights": ai.get("key_insights", []),
            }

    # Fallback to offline summarizer
    if not summary_data:
        summary_data = summarize_and_insights(
            text,
            max_sentences=args.max_sentences,
            insights_n=args.insights,
        )

    result = {
        "source": args.input,
        "word_count": summary_data.get("word_count", None),
        "sentence_count": summary_data.get("sentence_count", None),
        "summary": summary_data["summary"],
        "key_insights": summary_data["key_insights"],
        "top_keywords": summary_data.get("top_keywords", []),
    }

    json_path = os.path.join(outdir, f"{base}_summary.json")
    csv_path = os.path.join(outdir, f"{base}_insights.csv")

    write_json(json_path, result)
    write_csv(csv_path, [{"insight": x} for x in result["key_insights"]])

    return {"json": json_path, "csv": csv_path}

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Summarize a text file and extract key insights.")
    p.add_argument("--input", required=True, help="Path to input .txt file.")
    p.add_argument("--outdir", default="out", help="Directory to write outputs (default: out).")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI model (default: gpt-4o-mini).")
    p.add_argument("--max-sentences", type=int, default=5, help="Max sentences in summary (default: 5).")
    p.add_argument("--insights", type=int, default=5, help="Number of key insights to extract (default: 5).")
    p.add_argument("--use-openai", action="store_true", help="Force using OpenAI if available.")
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    outputs = run_cli(args)
    print(f"Wrote JSON: {outputs['json']}")
    print(f"Wrote CSV:  {outputs['csv']}")

if __name__ == "__main__":
    main()
