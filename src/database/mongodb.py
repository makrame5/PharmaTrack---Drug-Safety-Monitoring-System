from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import Dict, Any, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class MongoDBClient:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "eim"):
        """
        Initialise la connexion à MongoDB.
        """
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        self.reports = None
        
    def is_connected(self) -> bool:
        """Vérifie si la connexion est active."""
        try:
            if self.client is None:
                return False
            # Test de la connexion
            self.client.server_info()
            return True
        except:
            return False
        
    def connect(self) -> bool:
        """Établit la connexion à MongoDB."""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test de la connexion
            self.client.server_info()
            self.db = self.client[self.db_name]
            self.reports = self.db['reports']
            
            # Création d'un index unique sur report_id pour éviter les doublons
            self.reports.create_index("report_id", unique=True)
            
            logger.info(f"Connecté à MongoDB: {self.connection_string}")
            logger.info(f"Base de données: {self.db_name}")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"Échec de la connexion à MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la connexion: {e}")
            return False
    
    def close(self):
        """Ferme la connexion à MongoDB."""
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
            self.reports = None
            logger.info("Connexion à MongoDB fermée")
    
    def insert_report(self, report_data: Dict[str, Any]) -> bool:
        """
        Insère un nouveau rapport dans la base de données.
        """
        try:
            # Vérification de la connexion
            if not self.is_connected() or not hasattr(self, 'reports') or self.reports is None:
                logger.error("Non connecté à la base de données")
                return False
            
            # Validation des données
            if not report_data.get("report_id"):
                logger.error("Le rapport doit avoir un report_id")
                return False
            
            # Insertion du rapport
            result = self.reports.insert_one(report_data)
            logger.info(f"Rapport {report_data['report_id']} inséré avec l'ID: {result.inserted_id}")
            return True
            
        except DuplicateKeyError:
            logger.warning(f"Le rapport {report_data.get('report_id')} existe déjà")
            return False
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion du rapport {report_data.get('report_id')}: {e}")
            return False

    # ... (le reste des méthodes reste inchangé)
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un rapport par son ID.
        
        Args:
            report_id: ID du rapport à récupérer
            
        Returns:
            Le rapport s'il existe, None sinon
        """
        try:
            if not self.reports:
                logger.error("Non connecté à la base de données")
                return None
                
            report = self.reports.find_one({"report_id": report_id})
            if report:
                logger.info(f"Rapport {report_id} trouvé")
            else:
                logger.info(f"Rapport {report_id} non trouvé")
            return report
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du rapport {report_id}: {e}")
            return None
    
    def count_reports(self) -> int:
        """Retourne le nombre total de rapports dans la base."""
        try:
            if not self.reports:
                logger.error("Non connecté à la base de données")
                return 0
            return self.reports.count_documents({})
        except Exception as e:
            logger.error(f"Erreur lors du comptage des rapports: {e}")
            return 0
    
    def delete_report(self, report_id: str) -> bool:
        """
        Supprime un rapport par son ID.
        
        Args:
            report_id: ID du rapport à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        try:
            if not self.reports:
                logger.error("Non connecté à la base de données")
                return False
                
            result = self.reports.delete_one({"report_id": report_id})
            if result.deleted_count > 0:
                logger.info(f"Rapport {report_id} supprimé")
                return True
            else:
                logger.warning(f"Rapport {report_id} non trouvé pour suppression")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du rapport {report_id}: {e}")
            return False
    
    def list_reports(self, limit: int = 10) -> list:
        """
        Liste les rapports avec une limite.
        
        Args:
            limit: Nombre maximum de rapports à retourner
            
        Returns:
            Liste des rapports
        """
        try:
            if not self.reports:
                logger.error("Non connecté à la base de données")
                return []
                
            reports = list(self.reports.find().limit(limit))
            logger.info(f"{len(reports)} rapports récupérés")
            return reports
            
        except Exception as e:
            logger.error(f"Erreur lors de la liste des rapports: {e}")
            return []

# Instance globale pour une utilisation facile
db_client = MongoDBClient()