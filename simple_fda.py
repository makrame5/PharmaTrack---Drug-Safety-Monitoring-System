import os
import requests
from dotenv import load_dotenv

print("=== Client FDA Simplifié ===")

# Charger les variables d'environnement
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENFDA_API_KEY", "BCfAjSGaZqrs2pYSgJajLmUm6Rfv4FQqPussNGgz")
BASE_URL = "https://api.fda.gov/drug/event.json"

if not API_KEY:
    print("❌ Aucune clé API trouvée")
    exit(1)

# Faire une requête simple
print("\n🔍 Test de connexion à l'API OpenFDA...")
try:
    response = requests.get(
        BASE_URL,
        params={
            'api_key': API_KEY,
            'search': 'patient.drug.medicinalproduct:"IBUPROFEN"',
            'limit': 1
        },
        timeout=10
    )
    
    print(f"✅ Statut de la réponse: {response.status_code}")
    data = response.json()
    total = data.get('meta', {}).get('results', {}).get('total', 0)
    print(f"📊 Nombre total de rapports: {total}")
    
    if 'results' in data and data['results']:
        print("\n📝 Premier résultat :")
        print(f"Médicament: {data['results'][0].get('patient', {}).get('drug', [{}])[0].get('medicinalproduct', 'Inconnu')}")
        print(f"Réaction: {data['results'][0].get('patient', {}).get('reaction', [{}])[0].get('reactionmeddrapt', 'Inconnue')}")

except Exception as e:
    print(f"\n❌ Erreur lors de la requête : {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Code d'erreur: {e.response.status_code}")
        print(f"Réponse: {e.response.text[:200]}...")