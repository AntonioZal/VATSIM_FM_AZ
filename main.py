#!/usr/bin/python3.12

import requests, sys, pyodbc
from datetime import datetime

url = "https://data.vatsim.net/v3/vatsim-data.json"

def requete_api_vatsim():
    try:
        results = requests.get(url)

        if results.status_code == 200:
            return results.json()['pilots']
        else:
            print("Erreur lors de la récupération des données VATSIM")
            sys.exit(1)
    except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            sys.exit(1)

def information_pilote(pilotes):
    date_heure_zulu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for pilote in pilotes:
        print(pilote)
        

if __name__ == "__main__":
    datas = requete_api_vatsim()
    information_pilote(datas)