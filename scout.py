import requests


def search_scout(request):
    url = 'https://scoutai.ru/chat/message'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Host": "scoutai.ru",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru,ru-RU;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Content-Length": "113",
        "Origin": "https://scoutai.ru",
        "Alt-Used": "scoutai.ru",
        "Connection": "keep-alive",
        "Referer": "https://scoutai.ru/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }
    data = {
        "messages":[
            {
                "role": "user",
                "content": request,
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["content"]
