import sys
import os
from pathlib import Path
from src.models.report import AdverseEventReport
from src.api.fda_client import FDAClient
from pathlib import Path


print("=== DÉBUT DU SCRIPT ===")  # Ajout d'un message de débogage
print(f"Python version: {sys.version}")  # Vérification de la version Python
print(f"Répertoire de travail: {os.getcwd()}")  # Vérification du répertoire

# Ajout du chemin source
src_path = str(Path(__file__).parent / 'src')
print(f"Ajout du chemin: {src_path}")  # Vérification du chemin
sys.path.insert(0, src_path)
sys.path.append(str(Path(__file__).parent))


try:
    print("Tentative d'importation du client...")
    from api.fda_client import FDAClient
    print("✅ Client importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    print("Chemins Python actuels:")
    for p in sys.path:
        print(f" - {p}")
    sys.exit(1)

def main():
    print("\n=== Test du client OpenFDA ===")
    
    # Création du client
    print("\nCréation du client...")
    client = FDAClient()
    
    # Test de connexion
    print("\n🔍 Test de connexion à l'API...")
    if client.test_connection():
        print("✅ Connexion réussie !")
    else:
        print("❌ Échec de la connexion")
        return
    
    # Test de recherche
    print("\n🔍 Recherche d'effets secondaires pour l'ibuprofène...")
    try:
        resultats = client.search_reports('patient.drug.medicinalproduct:"IBUPROFEN"', limit=2)
        if resultats and 'results' in resultats:

            # Convertir le premier résultat en modèle
            rapport = AdverseEventReport.from_api_data(resultats['results'][0])
            
            print(f"✅ {len(resultats['results'])} résultats trouvés !")
            print("\n📝 Aperçu du premier résultat :")
            print(f"- ID: {rapport.report_id}")
            print(f"- Date: {rapport.received_date}")
            print(f"- Âge du patient: {rapport.patient.age} {rapport.patient.age_unit or ''}")
            print(f"- Médicaments: {[d.name for d in rapport.drugs]}")
            print(f"- Réactions: {[r.term for r in rapport.reactions]}")
        else:
            print("❌ Aucun résultat trouvé")

    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {str(e)}")


    try:
        resultats = client.search_reports('patient.drug.medicinalproduct:"IBUPROFEN"', limit=2)
        if resultats and 'results' in resultats:
            print(f"✅ {len(resultats['results'])} résultats trouvés !")
            
            # Convertir le premier résultat en modèle
            rapport = AdverseEventReport.from_api_data(resultats['results'][0])
            
            print("\n📝 Aperçu du premier résultat :")
            print(f"- ID: {rapport.report_id}")
            print(f"- Date: {rapport.received_date}")
            print(f"- Âge du patient: {rapport.patient.age} {rapport.patient.age_unit or ''}")
            print(f"- Médicaments: {[d.name for d in rapport.drugs]}")
            print(f"- Réactions: {[r.term for r in rapport.reactions]}")
            print(f"- Dates des médicaments: Début: {rapport.drugs[0].start_date if rapport.drugs else 'N/A'}, Fin: {rapport.drugs[0].end_date if rapport.drugs else 'N/A'}")

        else:
            print("❌ Aucun résultat trouvé")
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {str(e)}")

if __name__ == "__main__":
    print("\nDémarrage de l'exécution...")
    main()
    print("\n=== FIN DU SCRIPT ===")