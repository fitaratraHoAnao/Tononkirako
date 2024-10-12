from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/conjugate/<verbe>', methods=['GET'])
def conjugate(verbe):
    url = f"https://www.conjugaison.com/verbe/{verbe}.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Verbe non trouvé ou problème de connexion"}), 404
    
    soup = BeautifulSoup(response.content, 'html.parser')
    conjugations = {}

    # Trouver tous les modes (Indicatif, Subjonctif, etc.)
    mode_sections = soup.find_all("div", class_="col-xs-12 col-sm-12 col-md-12 col-lg-12 verbetitle")
    
    for mode_section in mode_sections:
        mode = mode_section.find('h3').text.strip()  # Récupérer le nom du mode (ex: "Indicatif")
        conjugations[mode] = {}  # Créer une entrée pour ce mode dans le dictionnaire
        
        # Trouver la section suivante contenant les temps de ce mode
        verb_boxes = mode_section.find_next_sibling().find_all("div", class_="col-xs-6 col-sm-6 col-md-3 col-lg-3 verbebox")
        
        for box in verb_boxes:
            tense = box.find('a').text.strip()  # Récupérer le nom du temps (ex: "Présent")
            # Récupérer toutes les conjugaisons pour ce temps
            conjugation_list = box.find_all("span", class_="conjugaison")
            
            # Stocker les conjugaisons sous le temps approprié pour ce mode
            conjugations[mode][tense] = [conj.text.strip() for conj in conjugation_list]
    
    return jsonify(conjugations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
