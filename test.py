print("=== Test de base ===")
print("Si vous voyez ce message, Python fonctionne correctement !")

# Test des imports
try:
    import requests
    import dotenv
    print("✅ Tous les modules nécessaires sont installés")
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")