from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path
from ..api.fda_client import FDAClient

class Extractor:
    def __init__(self):
        self.client = FDAClient()
        
    def extract_drug_reports(self, drug_name: str, limit: int = 100) -> List[Dict]:
        """Extrait les rapports pour un médicament donné."""
        print(f"🔍 Extraction des rapports pour {drug_name}...")
        reports = self.client.get_drug_reports(drug_name, limit)
        print(f"✅ {len(reports)} rapports extraits avec succès")
        return reports
    
    def save_raw_data(self, data: List[Dict], drug_name: str) -> str:
        """Sauvegarde les données brutes dans un fichier JSON."""
        # Créer le dossier s'il n'existe pas
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Générer un nom de fichier avec horodatage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = raw_dir / f"{drug_name.lower()}_raw_{timestamp}.json"
        
        # Sauvegarder les données
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 Données brutes sauvegardées dans {filename}")
        return str(filename)