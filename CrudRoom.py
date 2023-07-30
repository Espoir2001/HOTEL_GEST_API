from http.client import HTTPException
from typing import Union
from hotel_gest.models import Client
from hotel_gest.models import Room
from hotel_gest.models import RoomCategory
import sqlite3
import uuid
import connexion


from hotel_gest.connexion import get_connection
connexion = get_connection()

cursor = connexion.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='room';"
)
table_exists = cursor.fetchone() is not None

# Si la table n'existe pas, la créer
if not table_exists:
    connexion.execute(
        """CREATE TABLE room
                    (id TEXT PRIMARY KEY,
                    number INTEGER NOT NULL,
                    categ TEXT NOT NULL
                    );"""
    )
    connexion.commit()

# Fermeture de la connexion
connexion.close()


def AjouterRoom(room: Room):
    connection = get_connection()
    new_uuid = str(uuid.uuid4())
    connection.execute(
        "INSERT INTO room (id, number, categ) VALUES (?, ?, ?);",
        (new_uuid, room.number, room.categ.value),
    )
    connection.commit()

    # Fermeture de la connexion
    connection.close()
    return {"Room bien ajouté"}


def ListeRoom():
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM room;")
    connection.commit()
    rooms = cursor.fetchall()

    # Transformer les tuples récupérés en objets Client
    result = []
    for room in rooms:
        result.append(Room(uuid=room[0], number=room[1], categ=room[2]))

    # Fermeture de la connexion
    connection.close()

    # Retourner la liste des room
    return {"rooms": result}


def room_by_id(room_id: str):
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM room WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    # Si le client n'existe pas, retourner une erreur 404
    if not room:
        raise HTTPException(status_code=404, detail="room non trouvé")
    # Transformer le tuple récupéré en objet room
    result = Room(uuid=room[0], number=room[1], categ=room[2])
    connection.close()
    # Retourner le room

    return result


def supp_by_id(room_id: str):
    connection = get_connection()

    # Vérifier que l'id existe avant de le supprimer
    cursor = connection.execute("SELECT * FROM room WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    if not room:
        return {"error": f"Le room avec l'id {room_id} n'existe pas"}

    connection.execute("DELETE FROM room WHERE id = ?", (room_id,))
    connection.commit()
    connection.close()

    return {"room bien supprimé"}
