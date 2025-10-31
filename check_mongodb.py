import sys
import os
import subprocess
from pathlib import Path
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import socket
import logging
from typing import Dict, Any, Optional, List, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("MongoDB_Check")

class MongoDBTester:
    def __init__(self):
        self.connection_string = "mongodb://localhost:27017/"
        self.db_name = "eim"
        self.collection_name = "reports"
        self.client = None
        self.db = None
        self.collection = None
        self.test_data = {
            "test": "connexion",
            "status": "ok",
            "timestamp": "2023-10-31T20:00:00Z"
        }

    def print_header(self, title: str) -> None:
        """Affiche un en-tête de section"""
        print(f"\n{'='*50}")
        print(f" {title.upper()} ".center(50, '='))
        print(f"{'='*50}")

    def check_mongodb_service(self) -> bool:
        """Vérifie si le service MongoDB est en cours d'exécution"""
        self.print_header("Vérification du service MongoDB")
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ['sc', 'query', 'MongoDB'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                if "RUNNING" in result.stdout:
                    logger.info("✅ Service MongoDB en cours d'exécution")
                    return True
                else:
                    logger.error("❌ Service MongoDB arrêté")
                    return False
            else:  # Linux/Mac
                result = subprocess.run(
                    ['systemctl', 'is-active', 'mongod'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info("✅ Service MongoDB en cours d'exécution")
                    return True
                else:
                    logger.error("❌ Service MongoDB arrêté")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la vérification du service: {e}")
            return False

    def check_port(self) -> bool:
        """Vérifie si le port 27017 est en écoute"""
        self.print_header("Vérification du port 27017")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 27017))
            sock.close()
            if result == 0:
                logger.info("✅ Le port 27017 est en écoute")
                return True
            else:
                logger.error("❌ Le port 27017 n'est pas en écoute")
                return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la vérification du port: {e}")
            return False

    def connect_to_mongodb(self) -> bool:
        """Établit une connexion à MongoDB"""
        self.print_header("Connexion à MongoDB")
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000
            )
            # Force la connexion
            self.client.server_info()
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            logger.info("✅ Connecté à MongoDB avec succès")
            return True
        except ConnectionFailure as e:
            logger.error(f"❌ Échec de la connexion à MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur inattendue: {e}")
            return False

    def test_read_write(self) -> bool:
        """Teste les opérations de lecture/écriture"""
        if not self.client:
            logger.error("❌ Non connecté à MongoDB")
            return False

        self.print_header("Test d'écriture/lecture")
        try:
            # Test d'écriture
            result = self.collection.insert_one(self.test_data.copy())
            logger.info(f"✅ Document inséré avec l'ID: {result.inserted_id}")

            # Test de lecture
            doc = self.collection.find_one({"_id": result.inserted_id})
            if doc:
                logger.info("✅ Lecture du document réussie")
                logger.info(f"   Contenu: {doc}")
                return True
            else:
                logger.error("❌ Échec de la lecture du document")
                return False
        except Exception as e:
            logger.error(f"❌ Erreur lors du test d'écriture/lecture: {e}")
            return False

    def check_database_structure(self) -> bool:
        """Vérifie la structure de la base de données"""
        if not self.client:
            return False

        self.print_header("Vérification de la structure")
        try:
            # Vérifie si la base de données existe
            db_list = self.client.list_database_names()
            if self.db_name not in db_list:
                logger.info(f"⚠️  La base de données '{self.db_name}' n'existe pas")
                return False

                    # Force la création de la collection en insérant un document
            
            self.db[self.collection_name].insert_one({"check": "structure"})
            self.db[self.collection_name].delete_one({"check": "structure"})
            
            # Vérifie si la collection existe
            coll_list = self.db.list_collection_names()
            if self.collection_name not in coll_list:
                logger.info(f"⚠️  La collection '{self.collection_name}' n'existe pas")
                return False

            logger.info(f"✅ Structure valide: base '{self.db_name}' et collection '{self.collection_name}'")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de la vérification de la structure: {e}")
            return False

    def run_all_checks(self) -> bool:
        """Exécute tous les tests et retourne True si tout est OK"""
        results = []
        
        results.append(("Service MongoDB", self.check_mongodb_service()))
        results.append(("Port 27017", self.check_port()))
        results.append(("Connexion", self.connect_to_mongodb()))
        
        if all(r[1] for r in results[:3]):  # Si les 3 premiers tests sont OK
            results.append(("Structure de la base", self.check_database_structure()))
            results.append(("Lecture/Écriture", self.test_read_write()))
        
        # Afficher le résumé
        self.print_header("RÉSUMÉ DES TESTS")
        for name, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {name}: {'Succès' if success else 'Échec'}")
        
        # Nettoyage
        if self.client:
            try:
                # Supprimer le document de test
                self.collection.delete_one(self.test_data)
                self.client.close()
            except:
                pass
        
        return all(r[1] for r in results)

def main():
    tester = MongoDBTester()
    success = tester.run_all_checks()
    
    if success:
        print("\n🎉 Tous les tests ont réussi !")
    else:
        print("\n⚠️  Certains tests ont échoué. Consultez les messages ci-dessus pour plus de détails.")
    
    print("\nConseils de dépannage:")
    print("1. Vérifiez que MongoDB est bien installé")
    print("2. Assurez-vous que le service MongoDB est en cours d'exécution")
    print("3. Vérifiez que le port 27017 n'est pas bloqué par un pare-feu")
    print("4. Consultez les journaux MongoDB pour plus d'informations")
    
    if os.name == 'nt':  # Windows
        print("\nPour démarrer manuellement le service MongoDB sous Windows:")
        print("  Ouvrez un terminal en tant qu'administrateur et exécutez:")
        print("  net start MongoDB")
    else:  # Linux/Mac
        print("\nPour démarrer manuellement le service MongoDB sous Linux/Mac:")
        print("  sudo systemctl start mongod")

if __name__ == "__main__":
    main()