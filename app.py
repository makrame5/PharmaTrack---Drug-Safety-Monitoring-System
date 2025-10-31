import streamlit as st
from src.database.mongodb import db_client
from src.api.fda_client import FDAClient
from src.models.report import AdverseEventReport
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="FDA Reports Dashboard",
    page_icon="📊",
    layout="wide"
)

# Titre de l'application
st.title("📊 FDA Adverse Event Reports Dashboard")

# Initialisation des clients
fda_client = FDAClient()

# Initialisation de l'état de session
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False
    st.session_state.search_term = "IBUPROFEN"  # Valeur par défaut

# Barre latérale pour les paramètres
with st.sidebar:
    st.header("Paramètres de recherche")

    # Liste des médicaments courants
    common_drugs = {
        "IBUPROFEN": "Ibuprofène",
        "PARACETAMOL": "Paracétamol",
        "ASPIRIN": "Aspirine",
        "OMEPRAZOLE": "Oméprazole",
        "METFORMIN": "Metformine",
        "AMLODIPINE": "Amlodipine",
        "ATORVASTATIN": "Atorvastatine",
        "SERTRALINE": "Sertraline",
        "ESCITALOPRAM": "Escitalopram"
    }

    # Sélection du médicament
    selected_drug = st.selectbox(
        "Médicament",
        options=list(common_drugs.keys()),
        format_func=lambda x: common_drugs[x],  # Affiche le nom lisible
        index=0  # Par défaut sur IBUPROFEN
    )
    
    limit = st.number_input("Nombre de rapports", min_value=1, max_value=100, value=10)
    
    if st.button("Rechercher"):
        st.session_state.search_clicked = True
        st.session_state.search_term = selected_drug

# Section principale
if not st.session_state.search_clicked:
    st.info("Utilisez la barre latérale pour effectuer une recherche")
    st.stop()

# Connexion à MongoDB
if not db_client.connect():
    st.error("Impossible de se connecter à la base de données")
    st.stop()

# Récupération des rapports
with st.spinner("Recherche des rapports en cours..."):
    try:
        # Récupération des données de l'API FDA
        results = fda_client.search_reports(
            f'patient.drug.medicinalproduct:"{st.session_state.search_term}"', 
            limit=limit
        )
        
        if not results or 'results' not in results:
            st.warning("Aucun résultat trouvé")
            st.stop()
            
        # Affichage des statistiques
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rapports trouvés", len(results['results']))
        with col2:
            st.metric("Total en base", db_client.count_reports())
            
        # Affichage des rapports dans un tableau
        st.subheader("Derniers rapports")
        
        # Préparation des données pour le tableau
        reports_data = []
        for report_data in results['results']:
            try:
                report = AdverseEventReport.from_api_data(report_data)
                if report:
                    reports_data.append({
                        "ID": report.report_id,
                        "Date": report.received_date,
                        "Médicament": ", ".join([d.name for d in report.drugs]) if report.drugs else "N/A",
                        "Effets secondaires": ", ".join([r.term for r in report.reactions]) if report.reactions else "N/A"
                    })
            except Exception as e:
                st.error(f"Erreur lors du traitement d'un rapport: {e}")
        
        # Affichage du tableau
        if reports_data:
            df = pd.DataFrame(reports_data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": "ID",
                    "Date": "Date",
                    "Médicament": "Médicament",
                    "Effets secondaires": "Effets secondaires"
                }
            )
        else:
            st.warning("Aucun rapport valide à afficher")
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")
    finally:
        db_client.close()

# Pied de page
st.markdown("---")
st.caption("Application développée avec Streamlit - Données fournies par l'API OpenFDA")