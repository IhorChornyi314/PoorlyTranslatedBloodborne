from googletrans import Translator
from google.cloud import translate_v2 as translate
import random

sample_text = ['Blood Vial', open('sample_text.txt').read()]
random_languages = ['ru', 'de', 'fr', 'ja', 'zh-cn', 'nl', 'ko', 'no', 'it', 'ar', 'fi']


def translate_text_cloud(text, src, dst):
    translate_client = translate.Client.from_service_account_json('token.json')
    result = translate_client.translate(text, target_language=dst, source_language=src)
    return result['translatedText']


def translate_text_simple(text, src, dst):
    translator = Translator()
    result = translator.translate(text, dst, src=src)
    return result.text


def run_translation(text, n, use_cloud=True):
    src = 'en'
    for i in range(n):
        random.shuffle(random_languages)
        dst = random_languages[i] if random_languages[i] != src else random_languages[1]
        text = translate_text_cloud(text, src, dst) if use_cloud else translate_text_simple(text, src, dst)
        src = dst
    dst = 'en'
    return translate_text_cloud(text, src, dst) if use_cloud else translate_text_simple(text, src, dst)


print(run_translation(sample_text, 11, True))
