# from BDD import connection_bdd, deconnexion_bdd
from api import requete_api_vatsim, informations_pilotes

while True:

    # Connection à la base de données
    # connexion, curseur = connection_bdd()

    # Connection et récupération des données API VATSIM
    disponible = False
    donnees, disponible = requete_api_vatsim(disponible)

    # Traitement des données de l'API en base de données
    if disponible:
        informations_pilotes(donnees, connexion, curseur)
    else:
        print("")
        print("Données non disponibles via l'API Vatsim.")
        print("")

    # Deconnexion de la base de données
    # deconnexion_bdd(connexion)

    print("--------------------------------------------------")
    print("")
    print("--------------------------------------------------")
