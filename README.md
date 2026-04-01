# Audio Books Index

A simple searchable web catalog for an audio book collection.

## Usage

1. Generate `books.json` from the index:
   ```bash
   python generate.py
   ```
   This reads `/workspace/index.md` and writes `books.json`.

2. Serve locally:
   ```bash
   python -m http.server
   ```
   Open `http://localhost:8000` in your browser.

## Files

| File | Description |
|------|-------------|
| `index.html` | Single-page search UI (HTML + CSS + JS, zero dependencies) |
| `generate.py` | Parses `index.md` and outputs `books.json` |
| `test_generate.py` | Unit tests for the parser (run with `pytest`) |
| `books.json` | Generated data file (auto-generated, do not edit) |

## Running Tests

```bash
pip install pytest
pytest
```
