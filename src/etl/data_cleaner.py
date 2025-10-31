from datetime import datetime
from typing import Dict, Any, List, Optional
from ..models.report import AdverseEventReport, Patient, Drug, Reaction

class DataCleaner:
    @staticmethod
    def clean_patient_data(patient_data: Dict[str, Any]) -> Patient:
        """Nettoie et valide les données du patient."""
        age = patient_data.get('patientonsetage')
        if age is not None:
            try:
                age = int(float(age))  # Gère les âges sous forme de chaînes
            except (ValueError, TypeError):
                age = None

        return Patient(
            age=age,
            age_unit=patient_data.get('patientonsetageunit', '').lower() or None,
            sex={'1': 'Male', '2': 'Female'}.get(str(patient_data.get('patientsex')), 'Unknown'),
            weight=float(patient_data.get('patientweight')) if patient_data.get('patientweight') else None
        )

    @staticmethod
    def clean_drug_data(drug_data: Dict[str, Any]) -> Drug:
        """Nettoie et valide les données d'un médicament."""
        return Drug(
            name=drug_data.get('medicinalproduct', 'Inconnu').strip(),
            active_igredients=drug_data.get('active_ingredients', []),
            dosage_form=drug_data.get('drugdosageform', '').strip() or None,
            start_date=DataCleaner._parse_date(drug_data.get('drugstartdate')),
            end_date=DataCleaner._parse_date(drug_data.get('drugenddate'))
        )

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[str]:
        """Convertit une date au format YYYYMMDD en ISO format."""
        if not date_str or not isinstance(date_str, str) or len(date_str) < 8:
            return None
        try:
            date_obj = datetime.strptime(date_str[:8], '%Y%m%d')
            return date_obj.isoformat()
        except ValueError:
            return None

    @staticmethod
    def clean_report(report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Nettoie un rapport complet."""
        patient_data = report_data.get('patient', {})
        
        return {
            'report_id': report_data.get('safetyreportid'),
            'received_date': DataCleaner._parse_date(report_data.get('receivedate')),
            'patient': DataCleaner.clean_patient_data(patient_data),
            'drugs': [DataCleaner.clean_drug_data(drug) for drug in patient_data.get('drug', [])],
            'reactions': [
                Reaction(
                    term=reaction.get('reactionmeddrapt', 'Inconnue').strip(),
                    outcome=reaction.get('reactionoutcome', '').strip() or None
                )
                for reaction in patient_data.get('reaction', [])
            ],
            'source': 'openfda',
            'processed_at': datetime.utcnow().isoformat()
        }