import requests
import csv
import os
from datetime import datetime

def track_and_save():
    api_url = "https://www.winamax.fr/paris-sportifs/api/sports/100000"
    file_name = "historique_boosts.csv"
    
    # Headers pour simuler un navigateur mobile
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # Vérifie si la requête a réussi
        data = response.json()
        
        matches = data.get('matches', {})
        outcomes = data.get('outcomes', {})
        
        existing_data = set()
        if os.path.isfile(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 4:
                        existing_data.add((row[1], row[2], row[3]))

        file_exists = os.path.isfile(file_name)
        new_entries = 0
        
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Match', 'Pari', 'Cote'])

            for match in matches.values():
                match_name = match.get('title')
                for outcome_id in match.get('mainMarketOutcomes', []):
                    outcome = outcomes.get(str(outcome_id))
                    if outcome:
                        pari = outcome.get('label')
                        cote = str(outcome.get('odds'))
                        if (match_name, pari, cote) not in existing_data:
                            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), match_name, pari, cote])
                            new_entries += 1
        
        print(f"{new_entries} nouvelles cotes ajoutées.")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    track_and_save()
