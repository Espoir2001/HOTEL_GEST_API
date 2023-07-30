from http.client import HTTPException
from typing import Union
from hotel_gest.models import Adress, Client
from hotel_gest.models import Room
from hotel_gest.models import RoomCategory
from hotel_gest.models import Hotel
import sqlite3
import uuid
import connexion

from hotel_gest.connexion import get_connection
connexion = get_connection()


cursor = connexion.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='hotel';"
)
table_exists = cursor.fetchone() is not None

# Si la table n'existe pas, la créer
if not table_exists:
    connexion.execute(
        """CREATE TABLE hotel
                    (id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    street1 TEXT NOT NULL,
                    street2 TEXT NOT NULL,
                    street3 TEXT NOT NULL
                    );"""
    )
    connexion.commit()

# Fermeture de la connexion
connexion.close()


def AjouterHotel(hotel: Hotel):
    connection = connexion.get_connection()
    new_uuid = str(uuid.uuid4())
    connection.execute(
        "INSERT INTO hotel (id, name, street1, street2, street3) VALUES (?, ?, ?, ?, ?);",
        (
            new_uuid,
            hotel.name,
            hotel.adress.street1,
            hotel.adress.street2,
            hotel.adress.street3,
        ),
    )
    connection.commit()

    # Fermeture de la connexion
    connection.close()

    return {"hotel bien ajouté"}


def ListeHotel():
    connection = connexion.get_connection()
    cursor = connection.execute("SELECT * FROM hotel;")
    connection.commit()
    hotels = cursor.fetchall()

    # Transformer les tuples récupérés en objets Hotel
    result = []
    for hotel in hotels:
        result.append(
            Hotel(
                uuid=hotel[0],
                name=hotel[1],
                adress=Adress(street1=hotel[2], street2=hotel[3], street3=hotel[4]),
            )
        )

    # Fermeture de la connexion
    connection.close()

    # Retourner la liste des clients
    return {"hotels": hotels}


def hotel_by_id(hotel_id: str):
    connection = connexion.get_connection()
    cursor = connection.execute("SELECT * FROM clients WHERE id = ?", (hotel_id,))
    hotel = cursor.fetchone()
    # Si l'hotel n'existe pas, retourner une erreur 404
    if not hotel:
        raise HTTPException(status_code=404, detail="hotel non trouvé")
    # Transformer le tuple récupéré en objet hotel
    result = Client(
        uuid=hotel[0],
        name=hotel[1],
        adress=Adress(street1=hotel[2], street2=hotel[3], street3=hotel[4]),
    )
    connection.close()
    # Retourner l'hotel

    return result


def supp_by_id(hotel_id: str):
    connection = connexion.get_connection()

    # Vérifier que l'id existe avant de le supprimer
    cursor = connection.execute("SELECT * FROM hotel WHERE id = ?", (hotel_id,))
    hotel = cursor.fetchone()
    if not hotel:
        return {"error": f"Le client avec l'id {hotel_id} n'existe pas"}

    connection.execute("DELETE FROM hotel WHERE id = ?", (hotel_id,))
    connection.commit()
    connection.close()

    return {"hotel bien supprimé"}


def Modifier(hotel_id: str, name: str, adress: Adress):
    connection = connexion.get_connection()
    try:
        cursor = connection.execute(
            "UPDATE hotel SET name = ?, street1 = ? , street2= ?, street3 = ? WHERE id = ?",
            (name, adress.street1, adress.street2, adress.street3, hotel_id),
        )

        # Vérification que la réservation a été mise à jour
        if cursor.rowcount < 1:
            raise ValueError("L'hotel n'a pas pu être mise à jour")

        connection.commit()
        return {"hotel bien modifiée"}
    except:
        connection.rollback()
        raise
    finally:
        connection.close()
