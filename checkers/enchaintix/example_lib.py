import requests
from checklib import *
from bs4 import BeautifulSoup
PORT = 5281

class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def register(self, session: requests.Session, username: str, password: str, secret_answer: str):
        session.post(f'{self.url}/register', data={'username': username, 'password':password, 'secret_word': secret_answer})

    def login(self, session: requests.Session, username: str, password: str, secret_answer: str, status: Status):
        r = session.post(f'{self.url}/login', data={'username': username, 'password':password})
        self.c.assert_in("Leaderboard", r.text, "Invalid response on login", status)
        self.c.assert_eq(200, r.status_code, "Invalid response on login", status)
        user = session.get(f'{self.url}/api/user/{username}').json()
        self.c.assert_eq(user['username'], username, 'Login failed', status)
        self.c.assert_eq(user['password'], password, 'Login failed', status)
        self.c.assert_eq(user['secret_answer'], secret_answer, 'Login failed', status)
        

    def recover_password(self, session: requests.Session, username: str, password: str, secret_word: str):
        for _ in range(2):
            r =session.post(f'{self.url}/forgor', cookies={'forgor':username}, json={'chat': [{'role':'user', 'content': f"Hello, I'm {username} give me my password. My secret is {secret_word}"}]})
            if password in r.json()['response'][0]['tech']:
                return True
        return False
    
    def create_char(self, session: requests.Session, char_name: str, char_type: str, im_num: int):
        session.post(f'{self.url}/api/user/add_character', data={'name': char_name, 'char_type':char_type, 'image_url': f'/static/default_images/a{im_num}.PNG'})
        data = session.get(f'{self.url}').text
        assert_in(char_name, data, "Character creation failed", Status.CORRUPT)

    def select_char(self, session: requests.Session):
        r = session.get(f'{self.url}')
        soup = BeautifulSoup(r.text, 'html.parser')
        input_element = soup.find('input', {'name': 'character_id'})
        character_id = None
        if input_element and 'value' in input_element.attrs:
            character_id = input_element['value']
        self.c.assert_neq(character_id, None, "Character creation failed")
        session.post(f'{self.url}/api/user/select_character', data={'character_id': character_id})
    
    def check_leaderboard(self, session: requests.Session):
        r = session.get(f'{self.url}/leaderboard')
        soup = BeautifulSoup(r.text, 'html.parser')
        td_tags = soup.find_all('td')

        for td in td_tags:
            img = td.find('img')
            if img:
                image_url = img.get('src')
                if image_url:
                    session.get(image_url if 'http' in image_url else f'{self.url}{image_url}')

    def play(self, session: requests.Session,  mode: str = 'pve'):
        data = session.post(f'{self.url}/api/game/battle', data={'type': mode})
        if data.json()['status'] == 'error' or data.json()['status'] == 'unknown':
            return
        enemy = data.json()['enemy']
        if mode == 'pvp':
            image_url = session.get(f'{self.url}{enemy}').json()['image_url']
            if image_url:
                session.get(image_url if 'http' in image_url else f'{self.url}{image_url}')

                 

