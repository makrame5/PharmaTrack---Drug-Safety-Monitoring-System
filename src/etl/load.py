from typing import List, Dict
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from pathlib import Path

class MongoDBLoader:
    def __init__(self):
        # Charger les variables d'environnement
        load_dotenv(Path(__file__).parent.parent.parent / '.env')
        
        # Connexion à MongoDB
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DATABASE_NAME", "eim_platform")]
        self.collection = self.db['adverse_events']
        
    def load_data(self, data: List[Dict]) -> int:
        """Charge les données transformées dans MongoDB."""
        if not data:
            print("⚠️ Aucune donnée à charger")
            return 0
            
        try:
            result = self.collection.insert_many(data)
            print(f"✅ {len(result.inserted_ids)} documents insérés avec succès")
            return len(result.inserted_ids)
        except PyMongoError as e:
            print(f"❌ Erreur lors du chargement dans MongoDB: {str(e)}")
            return 0
            
    def close(self):
        """Ferme la connexion à MongoDB."""
        self.client.close()