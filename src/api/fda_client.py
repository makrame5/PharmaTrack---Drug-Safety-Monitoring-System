import os
import sys
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Optional, List, Any

print("=== Le script démarre ===")
print(f"Python version: {sys.version}")
print(f"Dossier de travail: {os.getcwd()}")
print(f"Chemin du script: {__file__}")

# Configuration du chargement des variables d'environnement
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path)

class FDAClient:
    def __init__(self):
        """Initialise le client FDA avec la configuration de base."""
        self.base_url = "https://api.fda.gov/drug/event.json"
        # Utilisation de la clé API depuis les variables d'environnement
        self.api_key = os.getenv("OPENFDA_API_KEY", "BCfAjSGaZqrs2pYSgJajLmUm6Rfv4FQqPussNGgz")
        
        if not self.api_key:
            print("⚠️ Attention: Aucune clé API n'a été trouvée")
            print("Veuillez créer un fichier .env avec votre clé API:")
            print("OPENFDA_API_KEY=votre_cle_api_ici")
    
    def _make_request(self, endpoint: str = "", params: Optional[Dict] = None) -> Optional[Dict]:
        """Effectue une requête à l'API OpenFDA."""
        if params is None:
            params = {}
            
        # Ajout de la clé API aux paramètres
        params['api_key'] = self.api_key
        
        try:
            print(f"\n🔍 Envoi de la requête à {self.base_url}")
            print(f"Paramètres: {json.dumps(params, indent=2)}")
            
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=10  # Timeout de 10 secondes
            )
            
            print(f"✅ Réponse reçue - Statut: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            total = data.get('meta', {}).get('results', {}).get('total', 0)
            print(f"📊 {total} résultats trouvés")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Erreur lors de la requête:")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Code d'erreur: {e.response.status_code}")
                print(f"Message: {e.response.text[:200]}...")
            else:
                print(f"Détails: {str(e)}")
            return None
        
    def search_reports(self, search_term: str, limit: int = 5) -> Optional[Dict]:
        """
        Recherche des rapports d'effets indésirables
        
        Args:
            search_term: Terme de recherche (ex: 'patient.drug.medicinalproduct:"IBUPROFEN"')
            limit: Nombre maximum de résultats à retourner (1-100)
            
        Returns:
            Dictionnaire contenant les résultats de la recherche ou None en cas d'erreur
        """
        print(f"\n🔎 Recherche de rapports pour: {search_term}")
        
        params = {
            'search': search_term,
            'limit': min(max(1, limit), 100)  # S'assure que la limite est entre 1 et 100
        }
        
        return self._make_request(params=params)

    
    def main():
        """Fonction principale pour tester le client."""
        print("=== Test du client OpenFDA ===\n")
        
        # Création du client
        client = FDAClient()
        
        # Vérification de la clé API
        if not client.api_key:
            print("❌ Impossible de continuer sans clé API")
            return
        
        # Recherche de test
        search_term = 'patient.drug.medicinalproduct:"IBUPROFEN"'
        print(f"\n🧪 Test de recherche pour: {search_term}")
        
        results = client.search_reports(search_term, limit=2)
        
        if results and 'results' in results:
            print("\n📝 Premier résultat:")
            print(json.dumps(results['results'][0], indent=2, ensure_ascii=False)[:500] + "...")
        
        print("\n✅ Test terminé")

    # Dans src/api/fda_client.py, ajoutez cette méthode à la classe FDAClient

    def test_connection(self) -> bool:
        """Teste la connexion à l'API OpenFDA avec une requête simple."""
        try:
            response = requests.get(
                self.base_url,
                params={'api_key': self.api_key, 'limit': 1},
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Erreur de connexion: {str(e)}")
            return False

if __name__ == "__main__":
    main()