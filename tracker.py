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
        
        # Correction des sélecteurs basés sur tes screenshots
        # On cherche les cartes blanches qui contiennent les paris
        boost_items = soup.select('div[style*="background-color: rgb(255, 255, 255)"]') 
        
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

            for item in boost_items:
                try:
                    # On récupère le texte principal (ex: "Toulouse - Lens : Florian Thauvin...")
                    full_text = item.find('h3').text.strip() if item.find('h3') else item.text.strip()
                    
                    if "Cote" in full_text:
                        # On sépare le match/pari de la cote
                        parts = full_text.split("Cote")
                        match_pari = parts[0].strip().strip(':')
                        cote = parts[1].strip()
                        
                        # Identification du bookmaker par l'image
                        img = item.find('img')
                        bookmaker = img['alt'] if img and img.has_attr('alt') else "Inconnu"
                        
                        if (bookmaker, "Match", match_pari, cote) not in existing_data:
                            writer.writerow([
                                datetime.now().strftime("%Y-%m-%d %H:%M"),
                                bookmaker,
                                "Voir Pari", # Le match est mélangé dans le texte sur TM
                                match_pari,
                                cote
                            ])
                            new_entries += 1
                except Exception as e:
                    continue
        
        print(f"Succès : {new_entries} nouveaux boosts détectés.")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_all_boosts()
