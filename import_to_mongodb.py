import sys
from pathlib import Path
from typing import List, Optional

# Ajout du dossier src au path
src_path = str(Path(__file__).parent / 'src')
sys.path.insert(0, src_path)

def main():
    # Demander le terme de recherche
    search_term = input("Entrez le nom du médicament à rechercher (par défaut: IBUPROFEN): ") or "IBUPROFEN"
    limit = int(input("Nombre maximum de rapports à importer (par défaut: 10): ") or "10")
    
    # Importer ici pour éviter les problèmes d'import circulaire
    from database.mongodb import db_client
    from models.report import AdverseEventReport
    from api.fda_client import FDAClient
    from src.database.mongodb import db_client
    from src.models.report import AdverseEventReport
    from src.api.fda_client import FDAClient
    
    print(f"\n🚀 Début de l'import pour: {search_term}")
    
    # Initialisation des clients
    fda_client = FDAClient()
    
    # Connexion à MongoDB
    if not db_client.connect():
        print("❌ Impossible de se connecter à MongoDB")
        return
    
    try:
        # Récupération des rapports
        print(f"\n🔍 Recherche des rapports pour: {search_term}")
        results = fda_client.search_reports(
            f'patient.drug.medicinalproduct:"{search_term.upper()}"', 
            limit=limit
        )
        
        if not results or 'results' not in results:
            print("❌ Aucun résultat trouvé")
            return
        
        print(f"✅ {len(results['results'])} rapports trouvés")
        
        # Traitement de chaque rapport
        saved_count = 0
        for i, report_data in enumerate(results['results'], 1):
            try:
                # Conversion en modèle
                report = AdverseEventReport.from_api_data(report_data)
                
                # Conversion en dictionnaire
                report_dict = report.to_dict()
                
                # Enregistrement dans MongoDB
                if db_client.insert_report(report_dict):
                    print(f"  [{i}/{len(results['results'])}] ✅ Rapport {report.report_id} sauvegardé")
                    saved_count += 1
                else:
                    print(f"  [{i}/{len(results['results'])}] ⚠️  Rapport {report.report_id} déjà existant")
            
            except Exception as e:
                print(f"  [{i}/{len(results['results'])}] ❌ Erreur: {str(e)}")
        
        # Afficher le résumé
        total = db_client.count_reports()
        print(f"\n📊 RÉSUMÉ DE L'IMPORT")
        print(f"- Rapports trouvés: {len(results['results'])}")
        print(f"- Nouveaux rapports enregistrés: {saved_count}")
        print(f"- Rapports existants ignorés: {len(results['results']) - saved_count}")
        print(f"- Total des rapports dans la base: {total}")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
    finally:
        db_client.close()
        print("\n✅ Opération terminée")

if __name__ == "__main__":
    main()