# Python Text Summarizer CLI

A zero-dependency (standard-library only) Python CLI that reads a `.txt` file, summarizes it, extracts key insights, and saves results as **JSON** and **CSV**.

- Uses `argparse` and a modular code structure under `src/cli_tool`.
- Integrates with the OpenAI API **optionally**. If an API key is present and the `openai` package is installed, it will use OpenAI; otherwise it falls back to a built-in, offline summarizer (default), so it runs end-to-end without any setup.
- Includes a `Dockerfile` and tests.

## Directory Structure

py-summarizer-cli/
├─ README.md
├─ Dockerfile
├─ requirements.txt
├─ src/
│ └─ cli_tool/
│ ├─ init.py
│ ├─ main.py
│ ├─ summarizer.py
│ ├─ io_utils.py
│ └─ openai_client.py
└─ tests/
├─ init.py
├─ test_summarizer.py
├─ test_cli.py
└─ fixtures/
└─ sample.txt



## Quick Start

### 1) Run natively (no dependencies)
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
python src/cli_tool/main.py --input tests/fixtures/sample.txt --outdir out


2) Use OpenAI (optional)

If you want to use OpenAI instead of the built-in summarizer:

pip install openai
export OPENAI_API_KEY="sk-..."
python src/cli_tool/main.py --input tests/fixtures/sample.txt --outdir out --use-openai


3) Docker
docker build -t py-summarizer-cli .
docker run --rm -v "$PWD:/work" py-summarizer-cli \
  python src/cli_tool/main.py --input tests/fixtures/sample.txt --outdir out

CLI Usage
usage: main.py [-h] --input INPUT [--outdir OUTDIR] [--model MODEL]
               [--max-sentences MAX_SENTENCES] [--insights N]
               [--use-openai]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Path to input .txt file.
  --outdir OUTDIR       Directory to write outputs (default: out).
  --model MODEL         OpenAI model (default: gpt-4o-mini).
  --max-sentences MAX_SENTENCES
                        Max sentences in summary (default: 5).
  --insights N          Number of key insights to extract (default: 5).
  --use-openai          Force using OpenAI if available.

Outputs

For an input tests/fixtures/sample.txt, you will get:

out/sample_summary.json

out/sample_insights.csv

Tests
python -m unittest -v

Notes

The offline summarizer is intentionally simple (frequency-based extractive summary) to avoid external deps.

The tool is safe to run in restricted environments; OpenAI usage is strictly opt-in.


---

## Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /work
COPY . /work

# No requirements needed for offline mode; OpenAI is optional
# RUN pip install --no-cache-dir -r requirements.txt

# Run tests at build time (optional, non-fatal)
# If you prefer failing builds on failing tests, remove `|| true`
RUN python -m unittest -v || true

CMD ["bash", "-lc", "python src/cli_tool/main.py --input tests/fixtures/sample.txt --outdir out"]