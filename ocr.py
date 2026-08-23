"""
ocr.py
------
One job: take image bytes, give back the text inside the image.

Nothing else lives here. Parsing amounts, categorising, saving to the
database - all of that comes in later days. Keeping this file small
means we can swap Google Vision for another provider later without
touching the rest of the app.
"""

from google.cloud import vision


def get_client() -> vision.ImageAnnotatorClient:
    """
    Creates the Google Vision client.

    It picks up your credentials automatically from the
    GOOGLE_APPLICATION_CREDENTIALS environment variable, which points
    to the service-account JSON file you downloaded from Google Cloud.
    """
    return vision.ImageAnnotatorClient()


def extract_text(image_bytes: bytes) -> str:
    """
    Send an image to Google Vision and return all the text it found.

    Args:
        image_bytes: the raw bytes of a png/jpg screenshot

    Returns:
        The full text as one string. Empty string if nothing was found.
    """
    client = get_client()
    image = vision.Image(content=image_bytes)

    # document_text_detection is tuned for dense text like receipts and
    # app screenshots. text_detection is better for signs and photos.
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise RuntimeError(f"Google Vision error: {response.error.message}")

    annotations = response.text_annotations
    if not annotations:
        return ""

    # The first annotation is always the complete block of text.
    # The rest are individual words, which we don't need today.
    return annotations[0].description


def extract_lines(image_bytes: bytes) -> list[str]:
    """
    Same as extract_text but split into clean, non-empty lines.

    Tomorrow's parser will work line by line, so this is a small
    head start.
    """
    text = extract_text(image_bytes)
    return [line.strip() for line in text.splitlines() if line.strip()]
