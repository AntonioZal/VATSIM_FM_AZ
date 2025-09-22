import requests

url = "https://data.vatsim.net/v3/vatsim-data.json"

def requete_api_vatsim():
    try:
        results = requests.get(url)

        if results.status_code == 200:
            return results.json()['pilots']
        else:
            print("Erreur lors de la récupération des données VATSIM")
            return None
    except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None