from googlesearch import search


def search_google(request):
    num_page = 10
    term = 'com'
    lang='en'
    answer = ''
    for i in search(request, num_page, term, lang): 
        answer += i + '\n'
    return answer
