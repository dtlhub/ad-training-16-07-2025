from datetime import date
from dataclasses import dataclass, asdict

import time
import requests
import jwt
import random

from checklib import *

PORT = 15151
PRIVATE_KEY = open("./private.key").read()


def rnd_date(diff):
    return date.fromtimestamp(time.time() + rnd_int(-diff, diff)).isoformat()


def rnd_int(min, max):
    return random.randint(min, max)


def set_jwt(session: requests.Session, account_name):
    token = jwt.encode({"account": {"name": account_name}}, PRIVATE_KEY, algorithm="RS256")
    session.headers.update({
        'authorization': f'Bearer {token}' 
    })


@dataclass
class Entity:
    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    def to_json(self):
        return asdict(self)

@dataclass
class Artist(Entity):
    name: str
    contact: str
    group: str = 'solo'
    spectialization: str = 'clown'
    fee: int = rnd_int(1, 100)

class Event(Entity):
    name: str
    date: str = rnd_date(1000000)
    description: str = rnd_string(100)
    raiting: int = rnd_int(1, 100)


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}/api'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def get_account_name(self, session: requests.Session):
        url = f'{self.url}/account/name'
        
        response = session.get(url)
        
        data = self.c.get_json(response, "Invalid response on get_account_name")
        self.c.assert_eq(type(data), dict, "Invalid response on get_account_name")
        
        return data['account_name']

    def put_entity(self, session: requests.Session, entity: Entity):
        url = f'{self.url}/entity/add?path=../models/{entity.model_name}.js'
        response = session.post(url, json=entity.to_json())

        data = self.c.get_json(response, "Invalid response on put_entity")
        self.c.assert_eq(type(data), dict, "Invalid response on put_entity")
        self.c.assert_in("success", data, "Invalid response on put_entity")
        self.c.assert_in("entity", data, "Invalid response on get_entity")
        self.c.assert_in("_id", data["entity"], "Invalid response on  put_entity")
        self.c.assert_eq(data["success"], True, "Can't put entity")

        return data['entity']['_id']

    def get_entity(self, session: requests.Session, _id: str, model: str, status: Status) -> str:
        url = f'{self.url}/entity/{_id}?path=../models/{model}.js'

        response = session.get(url)

        data = self.c.get_json(response, "Invalid response on get_entity", status)
        self.c.assert_eq(type(data), dict, "Invalid response on get_entity", status)
        self.c.assert_in("entity", data, "Invalid response on get_entity", status)
        self.c.assert_in("success", data, "Invalid response on get_entity")
        self.c.assert_eq(data["success"], True, "Can't get entity")

        return data['entity']
