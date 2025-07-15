import requests
from checklib import rnd_password, rnd_useragent, rnd_username
from bs4 import BeautifulSoup
from random import choice
PORT = 5281


def rnd_type():
    return choice(['Melee', 'Magic'])

class User:
    @property
    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host: str):
        self.port = PORT
        self.host = host
        self.session = self.start()

    def login(self):
        self.session.post(f'{self.url}/login', data={'username': self.name, 'password': self.password})
    
    def start(self) -> requests.Session:
        s = requests.Session()
        self.name, self.password, self.type, self.secret = rnd_username(), rnd_password(), rnd_type(), rnd_password()
        s.post(f'{self.url}/register', data={'username': self.name, 'password':self.password, 'secret_word': self.secret})
        return s

    def recover_password(self, username: str, chat: list = []) -> str:
        r = self.session.post(f'{self.url}/forgor', cookies={'forgor': username}, json={'chat': chat})
        return r.json()['response'][0]['tech']


    def create_char(self, im_url : str):
        self.session.post(f'{self.url}/api/user/add_character', data={'name': rnd_username(), 'char_type':rnd_type(), 'image_url': im_url})
        r = self.session.get(f'{self.url}')
        soup = BeautifulSoup(r.text, 'html.parser')
        input_element = soup.find('input', {'name': 'character_id'})
        character_id = None
        if input_element and 'value' in input_element.attrs:
            character_id = input_element['value']
        self.session.post(f'{self.url}/api/user/select_character', data={'character_id': character_id})

    def get_usernames(self) -> list:
        r = self.session.get(f'{self.url}/leaderboard')
        soup = BeautifulSoup(r.text, 'html.parser')

        rows = soup.select('tbody tr')
        
        owners = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 6:
                owner = cells[6].get_text(strip=True)
                owners.append(owner)
        return owners
    
    def check_leaderboard(self,sort_column: str = "id"):
        r = self.session.get(f'{self.url}/leaderboard?sort_column={sort_column}')
        return r.text


    def play(self, session: requests.Session,  mode: str = 'pve'):
        data = session.post(f'{self.url}/api/game/battle', data={'type': mode})
        if data.json()['status'] == 'error' or data.json()['status'] == 'unknown':
            return False
        return True