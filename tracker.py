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
        
        # Sélection des blocs de boosts
        boost_items = soup.select('.bet-boost-item') 
        
        existing_data = set()
        if os.path.isfile(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 5:
                        # On stocke : Bookmaker + Match + Pari + Cote
                        existing_data.add((row[1], row[2], row[3], row[4]))

        new_entries = 0
        file_exists = os.path.isfile(file_name) and os.stat(file_name).st_size > 0
        
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Bookmaker', 'Match', 'Pari', 'Cote'])

            for item in boost_items:
                try:
                    # Extraction des données
                    match = item.select_one('.bet-boost-event').text.strip()
                    pari = item.select_one('.bet-boost-market').text.strip()
                    cote = item.select_one('.bet-boost-odds').text.strip().replace('Cote', '').strip()
                    
                    # On devine le bookmaker via l'image ou le texte
                    bookmaker = "Inconnu"
                    img_alt = item.select_one('img')['alt'].lower() if item.select_one('img') else ""
                    if "winamax" in img_alt or "winamax" in str(item).lower(): bookmaker = "Winamax"
                    elif "unibet" in img_alt or "unibet" in str(item).lower(): bookmaker = "Unibet"
                    elif "betclic" in img_alt or "betclic" in str(item).lower(): bookmaker = "Betclic"
                    elif "pmu" in img_alt or "pmu" in str(item).lower(): bookmaker = "PMU"
                    elif "parions" in img_alt or "parions" in str(item).lower(): bookmaker = "ParionsSport"
                    
                    if (bookmaker, match, pari, cote) not in existing_data:
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M"),
                            bookmaker,
                            match,
                            pari,
                            cote
                        ])
                        new_entries += 1
                except:
                    continue
        
        print(f"Succès : {new_entries} nouveaux boosts ajoutés.")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_all_boosts()
