from http.client import HTTPException
from typing import Union
from hotel_gest.models import Client
from hotel_gest.models import Adress
import sqlite3
import uuid
import connexion

from hotel_gest.connexion import get_connection

connexion = get_connection()
cursor = connexion.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='clients';"
)
table_exists = cursor.fetchone() is not None

# Si la table n'existe pas, la créer
if not table_exists:
    connexion.execute(
        """CREATE TABLE clients
                    (id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    street1 TEXT NOT NULL,
                    street2 TEXT NOT NULL,
                    street3 TEXT NOT NULL
                    );"""
    )
    connexion.commit()

# Fermeture de la connexion
connexion.close()


def AjouterClient(client: Client):
    connection = get_connection()
    new_uuid = str(uuid.uuid4())
    connection.execute(
        "INSERT INTO clients (id, first_name, last_name, email, phone , street1, street2, street3) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        (
            new_uuid,
            client.first_name,
            client.last_name,
            client.email,
            client.phone,
            client.adress.street1,
            client.adress.street2,
            client.adress.street3,
        ),
    )
    connection.commit()

    # Fermeture de la connexion
    connection.close()

    return {"Client bien ajouté"}


def ListeCLient():
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM clients;")
    connection.commit()
    clients = cursor.fetchall()

    # Transformer les tuples récupérés en objets Client
    result = []
    for client in clients:
        result.append(
            Client(
                uuid=client[0],
                first_name=client[1],
                last_name=client[2],
                email=client[3],
                phone=client[4],
                adress=Adress(street1=client[5], street2=client[6], street3=client[7]),
            )
        )

    # Fermeture de la connexion
    connection.close()

    # Retourner la liste des clients
    return {"clients": result}


def client_by_id(client_id: Union[str, None], email: Union[str, None]):
    connection = get_connection()

    if client_id is not None:
        # Rechercher le client par id
        cursor = connection.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    elif email is not None:
        # Rechercher le client par email
        cursor = connection.execute("SELECT * FROM clients WHERE email = ?", (email,))
    else:
        # Lever une exception si ni l'id ni l'email ne sont fournis
        raise ValueError("L'id ou l'email doit être fourni")

    client = cursor.fetchone()

    # Si le client n'existe pas, retourner une erreur 404
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    # Transformer le tuple récupéré en objet Client
    result = Client(
        uuid=client[0],
        first_name=client[1],
        last_name=client[2],
        email=client[3],
        phone=client[4],
        adress=Adress(street1=client[5], street2=client[6], street3=client[7]),
    )

    connection.close()

    # Retourner le client
    return result


def supp_by_id(client_id: str):
    connection = get_connection()

    # Vérifier que l'id existe avant de le supprimer
    cursor = connection.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    if not client:
        return {"error": f"Le client avec l'id {client_id} n'existe pas"}

    connection.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    connection.commit()
    connection.close()

    return {"Client bien supprimé"}


def Modifier(
    client_id: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    adress: Adress,
):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "UPDATE clients SET first_name = ?, last_name = ? ,email =?,street1= ?, street2= ?, street3 = ? WHERE id = ?",
            (
                first_name,
                last_name,
                email,
                adress.street1,
                adress.street2,
                adress.street3,
                client_id,
            ),
        )

        # Vérification que le client a été mise à jour
        if cursor.rowcount < 1:
            raise ValueError("Le client n'a pas pu être mise à jour")

        connection.commit()
        return {"client bien modifiée"}
    except:
        connection.rollback()
        raise
    finally:
        connection.close()
