from bs4 import BeautifulSoup as bs
import requests

edu_instituts = {}
localities_id = {
    '76002000000': "Большесельский р-н" ,
    '76003000000': "Борисоглебский р-н",
    '76004000000': 'Брейтовский р-н',
    '76005000000': "Гаврилов-Ямский р-н",
    '76006000000': "Даниловский р-н",

    '76007000000': "Любимский р-н",
    '76008000000': "Мышкинский р-н",
    '76009000000': 'Некоузский р-н',
    '76010000000': 'Некрасовский р-н',
    '76011000000': 'Первомайский р-н',
    '76012000000': 'Переславский р-н',

    '76013000000': 'Пошехонский р-н',
    '76014000000': 'Ростовский р-н',
    '76015000000': 'Рыбинский р-н',
    '76016000000': 'Тутаевский р-н',
    '76017000000': 'Угличский р-н',
    '76001000000': 'Ярославский р-н',

    '76000002000': "Переславль-Залесский г",
    '76015001000': 'Рыбинск г',
    '76000001000': 'Ярославль г',
}
print(localities_id.popitem())
cookies = {
    '_ym_uid': '1640696081340171269',
    '_ym_d': '1640696081',
    'school_id': '760305',
    'fake_username': '03340858',
    '_ym_isad': '2',
    'csrftoken': 'pBRkxGexqeGAQECIa9crWRWQlaAgBRcu',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://my.dnevnik76.ru/accounts/login/',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

response = requests.get('https://my.dnevnik76.ru/ajax/school/frontend/76000001000/', headers=headers, cookies=cookies)
soup = bs(response.text, 'lxml')
instituts = soup.find_all(class_ = 'custom-select__item js-custom-select-option')
for inst in instituts:
    edu_instituts[f'{inst.text}'] = inst['data-value']

        
# for category in category_of_instituts:
#     if category.text == 'Общеобразовательное учреждение (90 шт.)':
#         instituts = category.find_all(class_ = 'custom-select__item js-custom-select-option')
#         #for i in instituts:
#         #    edu_instituts[f'{i.text}'] = i['data-value']
#             #edu_instituts['']

print(edu_instituts)