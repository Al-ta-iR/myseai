from translate import Translator
import re
import requests


def is_cyrillic(text):  # не работает
    cyrillic_pattern = re.compile('[а-яА-ЯёЁ]+')
    cyrillic_result = bool(cyrillic_pattern.fullmatch(text))
    return cyrillic_result


def translate_request(request):
    if any(is_cyrillic(word) for word in re.split(r'[ ,.:!-;]', request)):
        to_lang = 'en'
        from_lang = 'ru'
    else:
        to_lang = 'ru'
        from_lang = 'en'
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(request)
    return translation


if __name__ == "__main__":
    print(translate_request('Hi, how are you'))
    # print(translate_request('Привет друг. Как дела'))
