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
    
    # Extraction de la conjugaison, ici on prend l'exemple du présent de l'indicatif
    conjugations = {}
    present_section = soup.find("div", class_="col-xs-6 col-sm-6 col-md-3 col-lg-3 verbebox")
    if present_section:
        conjugations["present"] = present_section.text.strip()
    else:
        conjugations["present"] = "Pas de conjugaison trouvée pour ce verbe"
    
    return conjugations

# Route Flask pour récupérer la conjugaison en JSON
@app.route('/conjuguer', methods=['GET'])
def conjuguer():
    verbe = request.args.get('verbe', default='aller', type=str)
    conjugation = get_conjugation(verbe)
    return jsonify(conjugation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
