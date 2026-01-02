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
        
        # On cible tous les blocs de boosts
        # (Le script s'adapte à la structure visuelle de la page)
        boost_items = soup.select('.bet-boost-item') 
        
        existing_data = set()
        if os.path.isfile(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 4:
                        # Clé unique : Match + Pari + Cote
                        existing_data.add((row[1], row[2], row[3]))

        new_entries = 0
        file_exists = os.path.isfile(file_name) and os.stat(file_name).st_size > 0
        
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Match', 'Pari', 'Cote'])

            for item in boost_items:
                try:
                    # Extraction générique
                    match = item.select_one('.bet-boost-event').text.strip()
                    pari = item.select_one('.bet-boost-market').text.strip()
                    cote = item.select_one('.bet-boost-odds').text.strip()
                    
                    # Nettoyage de la cote (enlève "Cote" ou les espaces inutiles)
                    cote = cote.replace('Cote', '').strip()
                    
                    if (match, pari, cote) not in existing_data:
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M"),
                            match,
                            pari,
                            cote
                        ])
                        new_entries += 1
                except:
                    continue
        
        print(f"Succès : {new_entries} nouveaux boosts ajoutés au total.")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_all_boosts()
