import os

import six
from google.cloud import translate_v2 as translate


def translate_text(target, text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/maximmaximchuck/Downloads/quickstart-1554705327935-6b954f9a93e2.json"

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    print(f"[Google Translation API] Text: {result['input']}")
    print(f"[Google Translation API] Detected source language: {result['detectedSourceLanguage']}")
    print(f"[Google Translation API] Translation: {result['translatedText']}")

    return result['translatedText']


