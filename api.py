from datetime import datetime
from http.client import HTTPException
from typing import Dict, Optional, Union
import sqlite3

from hotel_gest.models import Client, Room, Hotel, Reservation, User
from hotel_gest.models import Adress
import hotel_gest.CrudClient as CrudClient
import hotel_gest.CrudRoom as CrudRoom
import hotel_gest.CrudHotel as CrudHotel
import hotel_gest.CrudReservation as CrudReservation
import uuid

from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

# USER

users_db = {
    "alice": {"password": "alice123", "token": "alice"},
    "bob": {"password": "bob123", "token": "bob"},
}


async def verify_token(x_token: Annotated[str, Header()]):
    for user in users_db.values():
        if x_token == user["token"]:
            return
    raise HTTPException(status_code=401, detail="Invalid token")


async def verify_key(x_key: Annotated[str, Header()]):
    for user in users_db.values():
        if x_key == user["password"]:
            return
    raise HTTPException(status_code=401, detail="Invalid key")


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root endpoint!"}


@app.post("/user/{email}/password")
def set_password(email: str, password: str):
    user = User(login=email, password=password)

    return {"token": str(uuid.uuid4())}


@app.get("/user/{login}/auth")
def authenticate_user(login: str, x_auth_password: str):
    # Vérifiez si le login existe dans la base de données des utilisateurs
    if login not in users_db:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Vérifiez si le mot de passe fourni correspond à celui stocké dans la base de données
    if x_auth_password != users_db[login]["password"]:
        raise HTTPException(status_code=401, detail="Non authorisé")

    # Générez un nouveau token pour l'utilisateur et stockez-le dans la base de données
    token = str(uuid.uuid4())
    users_db[login]["token"] = token

    # Retournez le token au format JSON
    return {"token": token}


# CLIENT


@app.post("/Ajouterclient", tags=["client"])
def ajouterClient(client: Client):
    return CrudClient.AjouterClient(client)


@app.get("/ListerClient", tags=["client"])
def listeCLient():
    return CrudClient.ListeCLient()


@app.get("/Client", tags=["client"])
def client_by_id(client_id: Optional[str] = None, email: Optional[str] = None):
    return CrudClient.client_by_id(client_id, email)


@app.delete("/Client/{client_id}", tags=["client"])
def supp_by_id(client_id: str):
    return CrudClient.supp_by_id(client_id)


@app.put("/Client/{client_id}", tags=["client"])
def modifier(
    client_id: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    adress: Adress,
):
    return CrudClient.Modifier(client_id, first_name, last_name, email, phone, adress)


# ROOM


@app.post("/AjouterRoom", tags=["room"])
def ajouterRoom(room: Room):
    return CrudRoom.AjouterRoom(room)


@app.get("/ListerRoom", tags=["room"])
def listeRoom():
    return CrudRoom.ListeRoom()


@app.delete("/Room/{room_id}", tags=["room"])
def supp_by_id(room_id: str):
    return CrudRoom.supp_by_id(room_id)


@app.get("/Room/{room_id}", tags=["room"])
def room_by_id(room_id: str):
    return CrudRoom.room_by_id(room_id)


# HOTEL


@app.post("/AjouterHotel", tags=["hotel"])
def ajouterHotel(hotel: Hotel):
    return CrudHotel.AjouterHotel(hotel)


@app.get("/ListerHotel", tags=["hotel"])
def listeHotel():
    return CrudHotel.ListeHotel()


@app.get("/Hotel/{hotel_id}", tags=["hotel"])
def hotel_by_id(hotel_id: str):
    return CrudHotel.hotel_by_id(hotel_id)


@app.delete("/Hotel/{hotel_id}", tags=["hotel"])
def supp_by_id(hotel_id: str):
    return CrudHotel.supp_by_id(hotel_id)


@app.put("/Hotel/{hotel_id}", tags=["hotel"])
def modifier(hotel_id: str, name: str, adress: Adress):
    return CrudHotel.Modifier(hotel_id, name, adress)


# RESERVATION


@app.post("/AjouterReservation", tags=["reservations"])
def ajouterReservation(reservation: Reservation):
    return CrudReservation.AjouterReservation(reservation)


@app.get("/ListerReservation", tags=["reservations"])
def listeReservation(
    date_start: Optional[datetime] = None,
    date_end: Optional[datetime] = None,
    tri_par: Optional[str] = None,
    tri_ordre: Optional[str] = None,
):
    return CrudReservation.ListeReservation(date_start, date_end, tri_par, tri_ordre)


@app.get("/Reservation/{reservation_id}", tags=["reservations"])
def reservation_by_id(reservation_id: str):
    return CrudReservation.reservation_by_id(reservation_id)


@app.delete("/Reservation/{reservation_id}", tags=["reservations"])
def supp_by_id(reservation_id: str):
    return CrudReservation.supp_by_id(reservation_id)


@app.put("/Reservation/{reservation_id}", tags=["reservations"])
def modifier(reservation_id: str, date_start: datetime, date_end: datetime):
    return CrudReservation.Modifier(reservation_id, date_start, date_end)
