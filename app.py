"""
app.py
------
Day 1 version of the Financial Advisor & Expense Manager agent.

What it does today:
  1. Let the user upload a payment screenshot
  2. Send it to Google Vision
  3. Show the raw text that came back

That's deliberately small. Once we trust that image -> text works,
everything else (parsing, categorising, advice) gets built on top.
"""

import os

import streamlit as st
from dotenv import load_dotenv

from ocr import extract_text, extract_lines

# Reads the .env file and puts GOOGLE_APPLICATION_CREDENTIALS into the
# environment so the Vision client can find your key.
load_dotenv()

st.set_page_config(page_title="Expense OCR", page_icon="💸", layout="wide")

st.title("💸 Financial Advisor & Expense Manager")
st.caption("Week 1 · Day 1 — screenshot to text")

# ---------------------------------------------------------------
# Credentials check: fail loudly and clearly instead of crashing
# with a confusing Google error later.
# ---------------------------------------------------------------
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not cred_path:
    st.error(
        "GOOGLE_APPLICATION_CREDENTIALS is not set. "
        "Create a `.env` file in this folder (copy `.env.example`) "
        "and point it at your service-account JSON file."
    )
    st.stop()

if not os.path.exists(cred_path):
    st.error(f"Credentials file not found at: `{cred_path}`")
    st.stop()

st.success("Google Vision credentials loaded ✓")

# ---------------------------------------------------------------
# Upload
# ---------------------------------------------------------------
uploaded = st.file_uploader(
    "Upload a payment screenshot (PhonePe, GPay, Paytm, or a receipt photo)",
    type=["png", "jpg", "jpeg", "webp"],
)

if uploaded is None:
    st.info("Pick a screenshot above to get started.")
    st.stop()

image_bytes = uploaded.getvalue()

left, right = st.columns(2)

with left:
    st.subheader("Your screenshot")
    st.image(image_bytes, use_column_width=True)

with right:
    st.subheader("What Google Vision read")

    with st.spinner("Reading the image..."):
        try:
            text = extract_text(image_bytes)
            lines = extract_lines(image_bytes)
        except Exception as e:
            st.error(f"OCR failed: {e}")
            st.stop()

    if not text:
        st.warning("No text found. Try a clearer or larger screenshot.")
        st.stop()

    st.text_area("Raw text", text, height=320)

    st.metric("Lines detected", len(lines))

    with st.expander("See it line by line"):
        for i, line in enumerate(lines, start=1):
            st.write(f"`{i:02d}`  {line}")

    st.download_button(
        "Download this text",
        data=text,
        file_name=f"{uploaded.name}.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "Next up (Day 2): pull the amount, date and merchant out of these lines."
)
