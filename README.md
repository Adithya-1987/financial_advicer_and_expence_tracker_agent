# 💸 Financial Advisor & Expense Manager AI Agent

An AI agent that reads your payment screenshots, tracks your expenses, and gives
financial advice grounded in established personal-finance principles.

**Track A** · Python · Streamlit · Google Vision · LangChain

---

## Current status

| Week | Focus | Status |
|------|-------|--------|
| 1–2 | Foundation: OCR + categorisation + deploy | 🔨 In progress |
| 3–4 | Advisory engine + Splitwise + charts | ⬜ Not started |
| 5–6 | Indian finance context (PPF, ELSS, SIP, tax) | ⬜ Not started |
| 7–8 | Polish, exports, docs, demo | ⬜ Not started |

**Today:** upload a payment screenshot → extract the text with Google Vision.

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd finance-agent

python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a Google Vision API key

1. Go to <https://console.cloud.google.com>
2. Create a new project (e.g. `finance-agent`)
3. Search for **Cloud Vision API** → **Enable**
4. Go to **APIs & Services → Credentials → Create Credentials → Service Account**
5. Give it a name, click through the optional steps, then **Create**
6. Open the service account → **Keys → Add Key → Create new key → JSON**
7. A `.json` file downloads. Move it into a `keys/` folder in this project:

```bash
mkdir keys
mv ~/Downloads/your-key-file.json keys/vision-key.json
```

> Billing must be enabled on the project, but the first **1,000 OCR requests
> per month are free**. This project will not come close to that.

### 4. Point the app at your key

```bash
cp .env.example .env
```

Then edit `.env` and set the full path to your key file:

```
GOOGLE_APPLICATION_CREDENTIALS=/Users/yourname/finance-agent/keys/vision-key.json
```

### 5. Run it

```bash
streamlit run app.py
```

Opens at <http://localhost:8501>.

---

## Project structure

```
finance-agent/
├── app.py            # Streamlit UI
├── ocr.py            # Image → text (Google Vision)
├── requirements.txt
├── .env.example      # Template for your credentials path
├── .gitignore        # Keeps .env and keys/ out of git
└── keys/             # Your API key lives here (git-ignored)
```

---

## Security

- The service-account key is **never** committed — `keys/` and `*.json` are
  git-ignored.
- If you ever paste a key into a commit, delete the key in Google Cloud
  Console immediately and create a new one.
- No financial data is stored permanently in this version.

---

## Disclaimer

This is an educational project. Any financial guidance it produces is general
information, not certified financial advice. Consult a registered advisor
before making investment decisions.
