from bs4 import BeautifulSoup as bs
import requests
# from aiogram.utils.markdown import hbold, hcode, hitalic, hunderline, hlink, hstrikethrough
from db_file import DBFile

db = DBFile()
""" Test Account """

# Login: 03340858
# Password: 913982 
cookies = {
    '_ym_uid': '1640696081340171269',
    '_ym_d': '1640696081',
    'school_id': '760305',
    'fake_username': '03385350',
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


# headers = {
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"',
#     'Upgrade-Insecure-Requests': '1',
#     'Origin': 'https://my.dnevnik76.ru',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-User': '?1',
#     'Sec-Fetch-Dest': 'document',
#     'Referer': 'https://my.dnevnik76.ru/accounts/login/',
#     'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
# }



edu_instituts = {}
# no_school_here = hbold('Нам не удалось найти твою школу 😥.') + '\n' + 'Прости, но в твоем регионе нет школ. \nВыбери регион в котором находится твое образовательное учереждение. \nНе забудь, нужно ввести название региона, которое полность/ совпадает с тем, которое находится в дневнике. \n' + hbold('Где можно посмотреть название регионов?') + '\n' + hlink('Вот тут вот', 'https://my.dnevnik76.ru/accounts/login/')
# localities_id = [
#     '76002000000', #Большесельский р-н 
#     '76003000000', #Борисоглебский р-н
#     '76004000000', #Брейтовский р-н
#     '76005000000', #Гаврилов-Ямский р-н
#     '76006000000', #Даниловский р-н
#     '76007000000', #Любимский р-н
#     '76008000000', #Мышкинский р-н
#     '76009000000', #Некоузский р-н
#     '76010000000', #Некрасовский р-н
#     '76011000000', #Первомайский р-н
#     '76012000000', #Переславский р-н
#     '76013000000', #Пошехонский р-н
#     '76014000000', #Ростовский р-н
#     '76015000000', #Рыбинский р-н
#     '76016000000', #Тутаевский р-н
#     '76017000000', #Угличский р-н
#     '76001000000', #Ярославский р-н
#     '76000002000', #Переславль-Залесский г
#     '76015001000', #Рыбинск г
#     '76000001000', #Ярославль г
# ]

localities_id_dict = {
    'Большесельский р-н': "76002000000" ,
    'Борисоглебский р-н': "76003000000",
    'Брейтовский р-н': '76004000000',
    'Гаврилов-Ямский р-н': "76005000000",
    'Даниловский р-н': "76006000000",

    'Любимский р-н': "76007000000",
    'Мышкинский р-н': "76008000000",
    'Некоузский р-н': '76009000000',
    'Некрасовский р-н': '76010000000',
    'Первомайский р-н': '76011000000',
    'Переславский р-н': '76012000000',

    'Пошехонский р-н': '76013000000',
    'Ростовский р-н': '76014000000',
    'Рыбинский р-н': '76015000000',
    'Тутаевский р-н': '76016000000',
    'Угличский р-н': '76017000000',
    'Ярославский р-н': '76001000000',

    'Переславль-Залесский г': "76000002000",
    'Рыбинск г': '76015001000',
    'Ярославль г': '76000001000',
}

locality_for_signin = ''
school_for_signin = ''

def find_edu_instituts(message):
    locality_for_signin = message
    response = requests.get(f'https://my.dnevnik76.ru/ajax/school/frontend/{list(localities_id_dict.keys())[list(localities_id_dict.values()).index(message)]}/', headers=headers, cookies=cookies)
    soup = bs(response.text, 'lxml')
    full_instituts = soup.find_all(class_ = 'custom-select__item js-custom-select-option')
    no_instituts = soup.find(class_='text_danger')
    if full_instituts:
        for inst in full_instituts:
            edu_instituts[f'{inst.text}'] = inst['data-value']
    
            

    

def fill_edu_instituts():
    if edu_instituts == {}:
        find_edu_instituts()
    else:
        pass

def detect_academic_period():
    pass

def find_school_id_by_locality():
    pass

def get_school_for_sign_in(msg):
    school_for_signin = msg

def sign_in(user_id, school, locality, login, password):
    # find edu instituts
    #user_id = str(user_id)
    response = requests.get(f'https://my.dnevnik76.ru/ajax/school/frontend/{list(localities_id_dict.keys())[list(localities_id_dict.values()).index(locality)]}/', headers=headers, cookies=cookies)
    soup = bs(response.text, 'lxml')
    full_instituts = soup.find_all(class_ = 'custom-select__item js-custom-select-option')
    no_instituts = soup.find(class_='text_danger')
    if full_instituts:
        for inst in full_instituts:
            edu_instituts[f'{inst.text}'] = inst['data-value']
  
    
    # get IDs
    locality_id = list(localities_id_dict.keys())[list(localities_id_dict.values()).index(locality)]
    school_id = list(edu_instituts.keys())[list(edu_instituts.values()).index(school)]
    data = {
        'csrfmiddlewaretoken': 'WDRjXUpxPkzTw2CHziVIDDmwo3lr3aU4',
        'next': '',
        'submit': '',
        'place': '',
        'username': f'{login}@{school_id}',
        'school': f'{school_id}',
        'fake_username': login,
        'password': password,
    }        

    session = requests.Session()
    session.post('https://my.dnevnik76.ru/accounts/login/', headers=headers, cookies=cookies, data=data)
    db.signin(user_id, login, password, locality, locality_id, school, school_id)
    return session


