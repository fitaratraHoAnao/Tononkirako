from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/scrape_lyrics', methods=['GET'])
def scrape_lyrics():
    # Get the artist and song title from the request parameters
    artist = request.args.get('artist', '')
    song_title = request.args.get('song', '')
    
    # Construct the URL
    url = f"https://tononkira.serasera.org/hira/{artist}/{song_title}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content div
    main_div = soup.find('div', {'id': 'main'})
    
    if main_div:
        # Extract the title
        title = main_div.find('h2').text.strip() if main_div.find('h2') else "Titre non trouvÃ©"
        
        # Extract the lyrics
        lyrics_content = main_div.find('div', {'class': 'my-3'})
        if lyrics_content:
            # Remove any script tags
            for script in lyrics_content(["script", "style"]):
                script.decompose()
            lyrics = lyrics_content.get_text(separator='\n', strip=True)
            # Remove any lines that are just numbers (verse numbers)
            lyrics = '\n'.join([line for line in lyrics.split('\n') if not line.strip().isdigit()])
            # Remove any remaining unwanted text
            lyrics = re.sub(r'\(Nalaina.*?\)', '', lyrics).strip()
        else:
            lyrics = "Paroles non trouvÃ©es"
        
        # Extract additional information
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
        
        # Create a dictionary with the extracted information
        result = {
            'title': title,
            'lyrics': lyrics,
            'info': info
        }
        
        return jsonify(result)
    else:
        return jsonify({'error': 'Content not found'}), 404
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
                              
