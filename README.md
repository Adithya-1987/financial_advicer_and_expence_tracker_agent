# 💸 Financial Advisor & Expense Manager

An AI agent that reads payment screenshots, turns them into structured expense
records, and gives financial guidance grounded in established personal-finance
principles.

`Python` · `Streamlit` · `Google Cloud Vision` · `LangChain`

---

## Status

Working today:

- Upload a payment screenshot (PhonePe / GPay / Paytm / receipt photo)
- OCR through Google Cloud Vision (`document_text_detection`, tuned for dense text)
- Full text + line-by-line view, with a text download

Not built yet: field parsing (amount, date, merchant), categorisation, storage,
advice layer. See [Roadmap](#roadmap).

---

## Quick start

```bash
git clone https://github.com/Adithya-1987/financial_advicer_and_expence_tracker_agent.git
cd financial_advicer_and_expence_tracker_agent

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then set GOOGLE_APPLICATION_CREDENTIALS
streamlit run app.py              # http://localhost:8501
```

Requires Python 3.9+ (`ocr.py` uses `list[str]` annotations).

---

## Google Vision credentials

1. Open <https://console.cloud.google.com> and create a project.
2. Enable **Cloud Vision API**.
3. **APIs & Services → Credentials → Create Credentials → Service Account**.
4. Open the service account → **Keys → Add Key → Create new key → JSON**.
5. Move the downloaded file into this project:

   ```bash
   mkdir -p keys
   mv ~/Downloads/your-key-file.json keys/vision-key.json
   ```

6. Point `.env` at its **absolute** path:

   ```
   GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/keys/vision-key.json
   ```

Billing must be enabled, but the first **1,000 OCR requests per month are
free** — well above what this project uses.

---

## Layout

```
.
├── app.py            # Streamlit UI: upload → OCR → display
├── ocr.py            # Image bytes → text (only Vision-aware file)
├── requirements.txt
├── .env.example      # Template for the credentials path
└── keys/             # Service-account JSON (git-ignored)
```

`ocr.py` is the single provider boundary — swapping Vision for Tesseract or
another OCR service means changing that file only.

### API

```python
from ocr import extract_text, extract_lines

extract_text(image_bytes)   # -> str   full text, "" if nothing found
extract_lines(image_bytes)  # -> list[str]  stripped, non-empty lines
```

Both raise `RuntimeError` on a Vision API error.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `GOOGLE_APPLICATION_CREDENTIALS is not set` | No `.env`, or the variable is missing from it. |
| `Credentials file not found at: ...` | Path is wrong or relative — use an absolute path. |
| `OCR failed: 403 ... has not been used` | Cloud Vision API not enabled on the project. |
| `OCR failed: 403 ... billing` | Enable billing (free tier still applies). |
| "No text found" | Screenshot too small or low contrast; try the original resolution. |

---

## Roadmap

- Parse amount, date, merchant and payment mode from OCR lines
- Categorise transactions and persist them
- Spending summaries and trends
- Advice layer over the transaction history
- Multi-screenshot batch import

---

## Security

- `keys/`, `*.json` and `.env` are git-ignored — credentials never enter the repo.
- If a key ever lands in a commit, revoke it in Google Cloud Console and issue a
  new one; rotating is faster than scrubbing history.
- Screenshots are processed in memory and not persisted in this version.

---

## Disclaimer

Educational project. Output is general information, not certified financial
advice. Consult a registered advisor before making investment decisions.
