from http.client import HTTPException
from typing import Union
from hotel_gest.models import Client
from hotel_gest.models import Adress
import sqlite3
import uuid


def get_connection():
    connexion = sqlite3.connect("hotel_gest.db")
    return connexion