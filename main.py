from api import requete_api_vatsim

disponible = False

donnees, disponible = requete_api_vatsim(disponible)

for donnee in donnees['pilots']:
    print(donnee['name'])