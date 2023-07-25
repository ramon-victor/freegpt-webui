import os

languages = ['en_US', 'es_MX', 'pt_BR', 'ru_RU', 'zh_CN', 'zh_TW', 'fr_FR', 'de_DE', 'it_IT', 'ja_JP', 'ko_KR', 'ar_SA', 'hi_IN', 'tr_TR']

for lang in languages:
    os.system(f'pybabel init -i translations/messages.pot -d translations -l {lang}')
