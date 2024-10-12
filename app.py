from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour extraire les conjugaisons depuis le site
def get_conjugation(verbe):
    url = f"https://www.conjugaison.com/verbe/{verbe}.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Verbe non trouvé ou problème de connexion"}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    conjugations = {}
    
    # Trouver la section du présent
    present_section = soup.find_all("div", class_="col-xs-6 col-sm-6 col-md-3 col-lg-3 verbebox")
    
    if present_section:
        # Parcourir les éléments <span class="conjugaison"> dans le présent
        present_conjugation = present_section[0].find_all("span", class_="conjugaison")
        if present_conjugation:
            # Capturer chaque personne (je, tu, il/elle, nous, vous, ils/elles)
            conjugations["present"] = {
                "je": present_conjugation[0].text.strip(),
                "tu": present_conjugation[1].text.strip(),
                "il/elle": present_conjugation[2].text.strip(),
                "nous": present_conjugation[3].text.strip(),
                "vous": present_conjugation[4].text.strip(),
                "ils/elles": present_conjugation[5].text.strip()
            }
        else:
            conjugations["present"] = "Pas de conjugaison trouvée pour ce verbe"
    else:
        conjugations["present"] = "Pas de conjugaison trouvée pour ce verbe"
    
    return conjugations
