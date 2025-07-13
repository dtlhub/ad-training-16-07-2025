import requests
from checklib import *

PORT = 7000

class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def register(self, session: requests.Session, username: str, password: str):

        reg_data = {
            "user": username,
            "pass": password,
            "email": f"{username}@google.ru",
            'subjoin': 1
        }

        session.post(f'{self.url}/process.php', data=reg_data)

    def login(self, session: requests.Session, username: str, password: str, status: Status):

        log_data = {
            "user": username,
            "pass": password,
            "sublogin": 1
            }

        session.post(f'{self.url}/process.php', data=log_data)

    def put_publication(self, session: requests.Session, pub_text: str):
        url = f'{self.url}/postPub.php'

        response = session.post(url, data={
            "pubtext": pub_text
        }, allow_redirects=False)

        data = response.headers['Location'].split('fnPubilcation=')[1]
        self.c.assert_eq(len(data), 36, "Invalid filename length")

    def get_filename(self, session: requests.Session, pub_text: str):
         url_filename = f'{self.url}/getFilename.php'

         response = session.post(url_filename, data={
            "pubtext": pub_text
         })

         self.c.assert_eq(len(response.text), 36, "Invalid filename length")

         return response.text

    def get_publication(self, session: requests.Session, filename: str, status: Status) -> str:
        url = f'{self.url}/receipts/'

        response = session.get(url + filename)

        self.c.assert_eq(type(response.text), str, "Can't get publication", status)

        return response.text
