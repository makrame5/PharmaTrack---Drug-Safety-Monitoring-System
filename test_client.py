import sys
import os
from pathlib import Path
from typing import Dict, Any

print("=== DÉBUT DU SCRIPT ===")
print(f"Python version: {sys.version}")
print(f"Répertoire de travail: {os.getcwd()}")

# Configuration des chemins
src_path = str(Path(__file__).parent / 'src')
print(f"Ajout du chemin: {src_path}")
sys.path.insert(0, src_path)
sys.path.append(str(Path(__file__).parent))

# Importations avec gestion d'erreurs
try:
    print("Tentative d'importation des modules...")
    from src.models.report import AdverseEventReport
    from src.api.fda_client import FDAClient
    from src.database.mongodb import db_client
    print("✅ Tous les modules importés avec succès")
except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    print("Chemins Python actuels:")
    for p in sys.path:
        print(f" - {p}")
    sys.exit(1)


def test_fda_api():
    """Test de l'API FDA seule"""
    print("\n=== Test du client OpenFDA ===")
    
    client = FDAClient()
    
    # Test de connexion
    print("\n🔍 Test de connexion à l'API...")
    if client.test_connection():
        print("✅ Connexion réussie !")
    else:
        print("❌ Échec de la connexion")
        return False
    
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
            print(f"- Sexe: {rapport.patient.sex or 'Non spécifié'}")
            print(f"- Poids: {rapport.patient.weight or 'Non spécifié'} kg")
            print(f"- Médicaments: {[d.name for d in rapport.drugs]}")
            print(f"- Réactions: {[r.term for r in rapport.reactions]}")
            if rapport.drugs:
                print(f"- Dates du premier médicament: Début: {rapport.drugs[0].start_date or 'N/A'}, Fin: {rapport.drugs[0].end_date or 'N/A'}")
            
            return True
        else:
            print("❌ Aucun résultat trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {str(e)}")
        return False


def test_fda_with_mongodb():
    """Test de l'API FDA avec sauvegarde dans MongoDB"""
    print("\n=== Test du client OpenFDA avec MongoDB ===")
    
    # Connexion à MongoDB
    if not db_client.connect():
        print("❌ Impossible de se connecter à MongoDB")
        return False
    
    try:
        # Création du client FDA
        client = FDAClient()
        
        # Recherche de rapports
        print("\n🔍 Recherche de rapports...")
        results = client.search_reports('patient.drug.medicinalproduct:"IBUPROFEN"', limit=2)
        
        if results and 'results' in results:
            print(f"✅ {len(results['results'])} rapports trouvés")
            
            for report_data in results['results']:
                # Conversion en modèle
                report = AdverseEventReport.from_api_data(report_data)
                
                # Sauvegarde dans MongoDB
                if db_client.insert_report(report.to_dict()):
                    print(f"  ✓ Rapport {report.report_id} sauvegardé")
                else:
                    print(f"  ✗ Erreur lors de la sauvegarde du rapport {report.report_id}")
            
            # Afficher le nombre total de rapports
            count = db_client.count_reports()
            print(f"\n📊 Total des rapports dans la base: {count}")
            return True
        else:
            print("❌ Aucun rapport trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        # Fermer la connexion
        db_client.close()


def main():
    """Fonction principale"""
    print("\nDémarrage des tests...")
    
    # Test 1: API FDA seule
    api_success = test_fda_api()
    
    # Test 2: API FDA + MongoDB
    mongo_success = test_fda_with_mongodb()
    
    # Résumé des tests
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    print(f"✅ Test API FDA: {'SUCCÈS' if api_success else 'ÉCHEC'}")
    print(f"✅ Test MongoDB: {'SUCCÈS' if mongo_success else 'ÉCHEC'}")
    
    if api_success and mongo_success:
        print("\n🎉 Tous les tests sont passés avec succès !")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez la configuration.")


if __name__ == "__main__":
    main()
    print("\n=== FIN DU SCRIPT ===")