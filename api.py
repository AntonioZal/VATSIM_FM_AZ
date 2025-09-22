import requests

# Fonction qui retourne les données disponibles via l'API Vatsim
def requete_api_vatsim(disponible):
    url = "https://data.vatsim.net/v3/vatsim-data.json"

    # Gérer les exceptions pour capturer les erreurs potentielles lors de la requête
    try:
        resultat = requests.get(url, timeout = 10)

        if resultat.status_code == 200:
            disponible = True
            donnees = resultat.json()
            return donnees, disponible
        else:
            # Si la requête échoue, afficher le code erreur
            print(f"Erreur HTTP {resultat.status_code}")
            return None, disponible
    except Exception as e:
        # Gérer les exceptions et afficher un message d'erreur
        print(f"Erreur lors de l'exécution de la requête : {e}") 
        return None, disponible
