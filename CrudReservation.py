from http.client import HTTPException
from typing import Optional, Union
from hotel_gest.models import Adress, Client
from hotel_gest.models import Room
from hotel_gest.models import RoomCategory
from hotel_gest.models import Hotel
from hotel_gest.models import Reservation
import sqlite3
import uuid
import connexion
from datetime import datetime

from hotel_gest.connexion import get_connection
connexion = get_connection()


cursor = connexion.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='reservation';"
)
table_exists = cursor.fetchone() is not None

# Si la table n'existe pas, la créer
if not table_exists:
    connexion.execute(
        """CREATE TABLE reservation
                    (id TEXT PRIMARY KEY,
                    date_start TEXT NOT NULL,
                    date_end TEXT NOT NULL
                    );"""
    )
    connexion.commit()

# Fermeture de la connexion
connexion.close()


def AjouterReservation(reservation: Reservation):
    connection = get_connection()
    try:
        new_uuid = str(uuid.uuid4())
        connection.execute(
            "INSERT INTO reservation (id, date_start, date_end) VALUES (?, ?, ?);",
            (new_uuid, reservation.date_start, reservation.date_end),
        )
        connection.commit()
        return {"reservation bien ajouté"}
    except:
        connection.rollback()
        raise
    finally:
        connection.close()


def ListeReservation(
    date_start: Optional[datetime] = None,
    date_end: Optional[datetime] = None,
    tri_par: Optional[str] = None,
    tri_ordre: Optional[str] = None,
):
    connection = get_connection()
    try:
        # Gérer les filtres de date_start et date_end s'ils sont fournis
        if date_start and date_end:
            sql = "SELECT * FROM reservation WHERE date_start >= ? AND date_end <= ?"
            params = (date_start, date_end)
        elif date_start:
            sql = "SELECT * FROM reservation WHERE date_start >= ?"
            params = (date_start,)
        elif date_end:
            sql = "SELECT * FROM reservation WHERE date_end <= ?"
            params = (date_end,)
        else:
            sql = "SELECT * FROM reservation;"
            params = ()

        # Ajouter l'ordre de tri si spécifié
        if tri_par is not None:
            if tri_ordre is not None and tri_ordre.lower() == "desc":
                sql += f" ORDER BY {tri_par} DESC"
            else:
                sql += f" ORDER BY {tri_par} ASC"

        cursor = connection.execute(sql, params)
        connection.commit()
        reservations = cursor.fetchall()

        # Transformer les tuples récupérés en objets Client
        result = []
        for reservation in reservations:
            result.append(
                Reservation(
                    uuid=reservation[0],
                    date_start=datetime.strptime(
                        reservation[1], "%Y-%m-%d %H:%M:%S.%f%z"
                    ),
                    date_end=datetime.strptime(
                        reservation[2], "%Y-%m-%d %H:%M:%S.%f%z"
                    ),
                )
            )
        return {"reservations": result}
    except:
        raise
    finally:
        connection.close()


#


def reservation_by_id(reservation_id: str):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT * FROM reservation WHERE id = ?", (reservation_id,)
        )
        reservation = cursor.fetchone()
        # Si la reservation n'existe pas, retourner une erreur 404
        if not reservation:
            raise HTTPException(status_code=404, detail="reservation non trouvé")

        # Transformer le tuple récupéré en objet reservation
        result = Reservation(
            uuid=reservation[0],
            date_start=datetime.strptime(reservation[1], "%Y-%m-%d %H:%M:%S.%f%z"),
            date_end=datetime.strptime(reservation[2], "%Y-%m-%d %H:%M:%S.%f%z"),
        )
        return result
    except:
        raise
    finally:
        connection.close()


def Modifier(reservation_id: str, date_start: datetime, date_end: datetime):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "UPDATE reservation SET date_start = ?, date_end = ? WHERE id = ?",
            (date_start, date_end, reservation_id),
        )

        # Vérification que la réservation a été mise à jour
        if cursor.rowcount < 1:
            raise ValueError("La réservation n'a pas pu être mise à jour")

        connection.commit()
        return {"reservation bien modifiée"}
    except:
        connection.rollback()
        raise
    finally:
        connection.close()
