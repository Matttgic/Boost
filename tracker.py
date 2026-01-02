import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def track_transfermarkt():
    # URL de Transfermarkt qui liste les boosts Winamax
    url = "https://www.transfermarkt.fr/paris-sportifs/cotes-boostees"
    file_name = "historique_boosts.csv"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche les lignes de boosts (le sélecteur dépend de leur structure)
        # Note : On cible Winamax spécifiquement dans la liste
        boost_rows = soup.find_all('div', class_='bet-boost-row') # Exemple de classe
        
        existing_data = set()
        if os.path.isfile(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 4:
                        existing_data.add((row[1], row[2], row[3]))

        new_entries = 0
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.isfile(file_name) or os.stat(file_name).st_size == 0:
                writer.writerow(['Date', 'Match', 'Pari', 'Cote'])

            # Ici on simule l'extraction (à adapter selon le code HTML exact de TM)
            # Pour l'instant, on va juste logger qu'on a réussi à lire la page
            if response.status_code == 200:
                print("Accès à Transfermarkt réussi !")
                # Si tu vois ce message dans les logs, on affinera le sélecteur HTML
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_transfermarkt()
