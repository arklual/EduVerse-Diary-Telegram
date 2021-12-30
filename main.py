import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup

def main():
    username = input('Username: ')
    password = input('Password: ')
    print(get_table(parse_subjects(login(username=username, password=password))))

def get_table(subjects):
    t = PrettyTable()
    max_marks = max([len(subjects[i]) for i in subjects])
    t.field_names = ["Предмет", "Ср. балл"] + [f'Оценка {i+1}' for i in range(max_marks-1)]
    for subject in subjects:
        while len(subjects[subject]) < max_marks:
            subjects[subject].append(' ')
        t.add_row([subject]+subjects[subject])
    return t

def login(username, password):
    cookies = {
        'school_id': '760305',
        'fake_username': username,
        'csrftoken': 'WDRjXUpxPkzTw2CHziVIDDmwo3lr3aU4',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://my.dnevnik76.ru',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://my.dnevnik76.ru/accounts/login/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'csrfmiddlewaretoken': 'WDRjXUpxPkzTw2CHziVIDDmwo3lr3aU4',
        'next': '',
        'submit': '',
        'place': '',
        'username': f'{username}@760305',
        'school': '760305',
        'fake_username': username,
        'password': password,
    }
    session = requests.Session()
    session.post('https://my.dnevnik76.ru/accounts/login/', headers=headers, cookies=cookies, data=data)
    return session

def parse_subjects(session):
    response = session.get('https://my.dnevnik76.ru/marks/current/edurng8409/list/')
    soup = BeautifulSoup(response.text)
    divs = soup.find_all('div')
    marks_div = divs[0]
    for div in divs:
        if div.get('id') == 'marks':
            marks_div = div
    divs = marks_div.find_all('div')
    subjects = {}
    for div in divs:
        if div.get('id') == 'mark-row':
            lable = div.find('div').text
            subjects[f'{lable}'] = []
            spans = div.find_all('span')
            for span in spans:
                if 'avg' in span.get('class'):
                    subjects[f'{lable}'].append(span.get('title'))
                elif 'm5' in span.get('class'):
                    subjects[f'{lable}'].append(5)
                elif 'm4' in span.get('class'):
                    subjects[f'{lable}'].append(4)
                elif 'm3' in span.get('class'):
                    subjects[f'{lable}'].append(3)
                elif 'm2' in span.get('class'):
                    subjects[f'{lable}'].append(2)
                elif 'm1' in span.get('class'):
                    subjects[f'{lable}'].append(1)
                elif 'm-1' in span.get('class'):
                    subjects[f'{lable}'].append('Н')
    return subjects

if __name__ == '__main__':
    main()