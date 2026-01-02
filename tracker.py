import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def track_all_boosts():
    url = "https://www.transfermarkt.fr/paris-sportifs/cotes-boostees"
    file_name = "historique_boosts.csv"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche tous les blocs de texte qui contiennent "Cote"
        # C'est la méthode la plus sûre par rapport à tes screens
        all_texts = soup.find_all(text=True)
        
        existing_data = set()
        if os.path.isfile(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 5:
                        existing_data.add((row[1], row[2], row[3], row[4]))

        new_entries = 0
        file_exists = os.path.isfile(file_name) and os.stat(file_name).st_size > 0
        
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Bookmaker', 'Match', 'Pari', 'Cote'])

            for text in all_texts:
                if "Cote" in text and len(text) > 10:
                    try:
                        # On nettoie le texte (ex: "Toulouse - Lens : ... Cote 3.25")
                        clean_text = text.strip().replace('\n', ' ')
                        parts = clean_text.split("Cote")
                        pari_complet = parts[0].strip().strip(':')
                        cote_valeur = parts[1].strip()

                        # On cherche le bookmaker autour du texte
                        parent = text.parent.parent.parent
                        img = parent.find('img')
                        bookmaker = img['alt'] if img and img.has_attr('alt') else "Inconnu"

                        if (bookmaker, "Boost", pari_complet, cote_valeur) not in existing_data:
                            writer.writerow([
                                datetime.now().strftime("%Y-%m-%d %H:%M"),
                                bookmaker,
                                "Boost",
                                pari_complet,
                                cote_valeur
                            ])
                            new_entries += 1
                    except:
                        continue
        
        print(f"Succès : {new_entries} nouveaux boosts détectés.")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_all_boosts()
