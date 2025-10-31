from typing import List, Dict, Any
from datetime import datetime

class Transformer:
    @staticmethod
    def transform_report(report: Dict[str, Any]) -> Dict[str, Any]:
        """Transforme un rapport brut en un format standardisé."""
        patient = report.get('patient', {})
        drugs = patient.get('drug', [{}])
        reactions = patient.get('reaction', [{}])
        
        # Extraire les informations principales
        transformed = {
            'report_id': report.get('safetyreportid'),
            'received_date': report.get('receivedate'),
            'transmission_date': report.get('transmissiondate'),
            'patient': {
                'age': patient.get('patientonsetage'),
                'age_unit': patient.get('patientonsetageunit'),
                'sex': patient.get('patientsex'),
                'weight': patient.get('patientweight')
            },
            'drugs': [{
                'name': drug.get('medicinalproduct'),
                'active_ingredients': drug.get('openfda', {}).get('substance_name', []),
                'dosage_form': drug.get('drugdosageform'),
                'indication': drug.get('drugindication'),
                'start_date': drug.get('drugstartdate'),
                'end_date': drug.get('drugenddate')
            } for drug in drugs],
            'reactions': [{
                'term': r.get('reactionmeddrapt'),
                'outcome': r.get('reactionoutcome')
            } for r in reactions],
            'source': 'openfda',
            'processed_at': datetime.utcnow().isoformat()
        }
        return transformed
    
    def transform_reports(self, reports: List[Dict]) -> List[Dict]:
        """Transforme une liste de rapports bruts."""
        return [self.transform_report(report) for report in reports]