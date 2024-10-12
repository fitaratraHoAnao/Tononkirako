from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/scrape_lyrics', methods=['GET'])
def scrape_lyrics():
    # Obtenir les paramètres artist et song_title à partir de la requête
    artist = request.args.get('artist', '')
    song_title = request.args.get('song', '')
    
    # Construire l'URL
    url = f"https://tononkira.serasera.org/hira/{artist}/{song_title}"
    
    # Envoyer une requête GET à l'URL
    response = requests.get(url)
    
    # Analyser le contenu HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver la div principale contenant les paroles
    main_div = soup.find('div', {'id': 'main'})
    
    if main_div:
        # Extraire le titre de la chanson
        title = main_div.find('h2').text.strip() if main_div.find('h2') else "Titre non trouvé"
        
        # Extraire les paroles de la chanson dans la div 'my-3'
        lyrics_content = main_div.find('div', {'class': 'my-3'})
        
        if lyrics_content:
            # Nettoyer les paroles en retirant les balises non désirées
            lyrics = lyrics_content.get_text(separator='\n', strip=True)
            
            # Nettoyer les paroles en retirant les lignes avec des chiffres ou texte indésiré
            lyrics = re.sub(r'\(Nalaina.*?\)', '', lyrics).strip()
            lyrics = '\n'.join([line for line in lyrics.split('\n') if not line.strip().isdigit()])
        else:
            lyrics = "Paroles non trouvées"
        
        # Extraire les informations supplémentaires si disponibles
        info_div = soup.find('div', {'class': 'col-md-4'})
        info = {}
        if info_div:
            info_items = info_div.find_all('div', {'class': 'border'})
            for item in info_items:
                item_title = item.find('h5')
                if item_title and item_title.text.strip() == "Momba ny hira":
                    info_text = item.text.strip().split('\n')
                    for line in info_text:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            info[key.strip()] = value.strip()
        
        # Retourner la réponse JSON avec le titre, les paroles, et les informations supplémentaires
        result = {
            'title': title,
            'lyrics': lyrics,
            'info': info
        }
        
        return jsonify(result)
    
    # Si le contenu principal n'est pas trouvé, retourner une erreur 404
    return jsonify({'error': 'Content not found'}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
