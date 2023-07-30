import enum
from datetime import datetime
from pydantic import BaseModel
import typing

import uuid


class Identifiable(BaseModel):
    uuid: typing.Union[uuid.UUID, None]


class Adress(BaseModel):
    street1: str
    street2: str
    street3: str


class Client(Identifiable):
    first_name: str
    last_name: str
    email: str
    phone: str
    adress: Adress


class Hotel(Identifiable):
    name: str
    adress: Adress


class RoomCategory(enum.Enum):
    LUXE = "Luxe"
    CLASSIC = "Classic"
    PMR = "PMR"


class BedType(enum.Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    XXL_DOUBLE = "XXL_DOUBLE"


class Reservation(Identifiable):
    date_start: datetime
    date_end: datetime


class Room(Identifiable):
    number: int
    categ: RoomCategory


class User(BaseModel):
    login: str
    password: str
