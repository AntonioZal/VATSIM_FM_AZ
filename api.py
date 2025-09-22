import requests
from datetime import datetime
# from BDD import recuperation_enregistrement_precedent, ajouter_enregistrement, commit_bdd
from fonction_gps import sexagesimal_nord_sud, sexagesimal_est_west, metres_position_gps

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

# Fonction qui récupère les informations principale pour chaque pilote et renvoi le nombre de lignes affectées
def informations_pilotes(donnees_api, connexion, curseur):
    # Récupération des pilotes
    pilotes = donnees_api.get("pilots", [])

    # Information Zulu
    date_heure_zulu = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    id = 1

    # Pour chaque pilote, récupération des données
    for pilote in pilotes:
        
        cid = pilote.get("cid")
        name = pilote.get("name")
        callsign = pilote.get("callsign")
        
        latitude = pilote.get("latitude")
        longitude = pilote.get("longitude")
        
        latitude_gps = ""
        longitude_gps = ""

        if isinstance(latitude, float) and isinstance(longitude, float):
            latitude_gps = sexagesimal_nord_sud(latitude)
            longitude_gps = sexagesimal_est_west(longitude)

        altitude = pilote.get("altitude")
        groundspeed = pilote.get("groundspeed")
        heading = pilote.get("heading")
        date = date_heure_zulu[:8]
        heure = date_heure_zulu[9:]

        logon_time = pilote.get("logon_time")

        # Récupération du plan de vol
        flight_plan = pilote.get("flight_plan")
        if flight_plan:
            depart = flight_plan.get("departure")
            arrivee = flight_plan.get("arrival")
            alternatif = flight_plan.get("alternate")
            avion = flight_plan.get("aircraft_short")
        
            distance_metres = 0.0
            distance_km = 0.0
            distance_mille_km = 0.0
            distance_nm = 0.0
            latitude_enregistree = None
            longitude_enregistree = None
            logon_time_enregistree = None

            # Récupération des données GPS de la ligne précédente
            # latitude_enregistree, longitude_enregistree, num_recup, logon_time_enregistree = recuperation_enregistrement_precedent(curseur, cid, callsign, depart, arrivee)

            # Si les coordonnées GPS sont différentes alors on enregistre la ligne dans la base de données
            if latitude_enregistree != latitude or longitude_enregistree != longitude:
                if latitude != 0.0 and longitude != 0.0:
                    if latitude_enregistree is not None and longitude_enregistree is not None and logon_time_enregistree is not None:
                        if logon_time_enregistree == logon_time:
                            
                            distance_metres = metres_position_gps(latitude_enregistree, longitude_enregistree, latitude, longitude)
                            distance_km = distance_metres / 1000
                            distance_mille_km = distance_km / 1000
                            distance_nm = distance_km / 1.852

                    # Ajouter l'enregistrement dans la base de données
                    # ajouter_enregistrement(curseur, cid, name, callsign, avion, latitude, longitude, latitude_gps, longitude_gps, distance_metres, distance_km, distance_mille_km, distance_nm, altitude, groundspeed, heading, depart, arrivee, alternatif, date, heure, date_heure_zulu, logon_time, num_recup)
                    print(f"Traitement du pilote {id} / {len(pilotes)} : {callsign} - {avion} - {name} - {depart} -> {arrivee}, Position GPS : {latitude_gps} / {longitude_gps}")
        id += 1


    # commit_bdd(connexion)

    print("")
    print(f"{len(pilotes)} pilotes traités.")
    print("")