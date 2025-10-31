import sys
import os
from pathlib import Path

# Ajouter le dossier racine au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Importer après avoir défini le PYTHONPATH
try:
    from src.etl.extract import Extractor
    from src.etl.transform import Transformer
    from src.etl.load import MongoDBLoader
    print("✅ Tous les modules importés avec succès")
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("Vérifiez que la structure des dossiers est correcte")
    print("Structure actuelle :")
    for path in root_dir.rglob('*'):
        print(f"  {path.relative_to(root_dir)}")
    sys.exit(1)

def run_etl_pipeline(drug_name: str, limit: int = 100):
    print(f"\n🚀 Démarrage du pipeline ETL pour {drug_name}")
    
    # Étape 1: Extraction
    print("\n🔍 Étape 1/3 - Extraction des données...")
    extractor = Extractor()
    raw_reports = extractor.extract_drug_reports(drug_name, limit)
    
    if not raw_reports:
        print("❌ Aucune donnée à traiter")
        return
        
    # Sauvegarder les données brutes
    extractor.save_raw_data(raw_reports, drug_name)
    
    # Étape 2: Transformation
    print("\n🔄 Étape 2/3 - Transformation des données...")
    transformer = Transformer()
    transformed_data = transformer.transform_reports(raw_reports)
    
    # Étape 3: Chargement
    print("\n📤 Étape 3/3 - Chargement des données dans MongoDB...")
    loader = MongoDBLoader()
    loaded_count = loader.load_data(transformed_data)
    loader.close()
    
    print(f"\n✅ Pipeline ETL terminé avec succès! {loaded_count} documents chargés")

if __name__ == "__main__":
    run_etl_pipeline("IBUPROFEN", limit=5)