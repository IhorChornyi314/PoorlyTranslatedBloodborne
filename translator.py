from googletrans import Translator as tr
from google.cloud import translate_v2 as translate
from tqdm import tqdm
import random


class Translator:
    def __init__(self, use_cloud=True):
        self.languages = ['ru', 'de', 'fr', 'ja', 'zh-cn', 'nl', 'ko', 'no', 'it', 'ar', 'fi']
        self.use_cloud = use_cloud
        self.translator = translate.Client.from_service_account_json('token.json') if use_cloud else tr()

    def translate(self, lines, src, dst):
        result = []
        for i in range(0, len(lines), 128):
            text = lines[i: min(len(lines), i + 128)]
            if self.use_cloud:
                result += [_['translatedText'].replace('&#39;', "'") for _ in self.translator.translate(text, target_language=dst, source_language=src)]
            else:
                result += [self.translator.translate(line, src=src, dest=dst).text if line != '' else '' for line in text]
        return result

    def chain_translate(self, lines, runs=10):
        src = 'en'
        for _ in tqdm(range(runs)):
            random.shuffle(self.languages)
            dst = self.languages[0] if self.languages[0] != src else self.languages[1]
            lines = self.translate(lines, src, dst)
            src = dst
        return self.translate(lines, src, 'en')
