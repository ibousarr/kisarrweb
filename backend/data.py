import json
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
import uuid
import random

# Définition du modèle de la table
class Eleve(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  ien: str
  prenom: str
  nom: str
  sexe: str
  datnais: str
  lieunais: str
  classe_id: str


# Configuration de la base de données (ici SQLite)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def creer_tables():
  SQLModel.metadata.create_all(engine)


def inserer_donnees_json():
    # 1. Ouvrir et lire le fichier JSON
    with open("data.json", "r", encoding="utf-8") as f:
        donnees = json.load(f)
        print(donnees[0])
    # 2. Ouvrir une session avec la base de données
    with Session(engine) as session:
        classes = [
            "2ca38955-1375-4f48-9d0f-5776d5f35aaa",
            "89bcf47f-c492-4d35-976d-7a5035097b7a",
            "174c812e-2a3f-46ef-94d2-3c56c0cfa1e8",
            "18f98f31-a476-4844-8c98-fd5458b9713f",
            "ba5f3949-1ae7-438a-accd-ba6081488e49",
            "3778ae72-a8dc-4f7e-912e-50c1b49d0c97",
            "c12b5b2d-8b8b-4274-9fbd-8d38d7bca536",
            "e3d13f36-bd71-4331-a639-466801f7abb5",
            "39d4c182-823c-4af2-af40-6b4606efeece",
            "e70b56e4-3115-4898-8e8d-236c0c5e5f86",
        ]
        # Choisir une valeur au hasard
        valeur_aleatoire = random.choice(classes)

        print(valeur_aleatoire)
        # Parcourir chaque élément du fichier JSON
        for item in donnees:
            valeur_aleatoire = random.choice(classes)
            # Créer une instance du modèle SQLModel
            eleve = Eleve(
                ien=item.get("ien"), 
                prenom=item.get("prenom"), 
                nom=item.get("nom"), 
                sexe=item.get("sexe"), 
                datnais=item.get("datnais"), 
                lieunais=item.get("lieunais"), 
                classe_id=random.choice(classes)
            )
            # print(eleve)
            # Ajouter l'objet à la session
            session.add(eleve)

        # 3. Valider (commit) l'enregistrement dans la base
        session.commit()


if __name__ == "__main__":
  creer_tables()
  inserer_donnees_json()
  print("Données insérées avec succès !")
