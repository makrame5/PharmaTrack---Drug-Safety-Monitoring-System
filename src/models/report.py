from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Reaction:
    term: str
    outcome: Optional[str] = None


@dataclass
class Drug:
    name: str
    active_ingredients: List[str]
    dosage_form: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@dataclass
class Patient:
    age: Optional[int] = None
    age_unit: Optional[str] = None
    sex: Optional[str] = None
    weight: Optional[float] = None


@dataclass
class AdverseEventReport:
    report_id: str
    received_date: str
    patient: Patient
    drugs: List[Drug]
    reactions: List[Reaction]
    source: str = "FDA"
    processed_at: str = None

    @classmethod
    def from_api_data(cls, data: dict) -> 'AdverseEventReport':
        """Crée un rapport à partir des données brutes de l'API."""
        patient_data = data.get('patient', {})
        
        return cls(
            report_id=data.get('safetyreportid', ''),
            received_date=data.get('receivedate', ''),
            patient=Patient(
                age=patient_data.get('patientonsetage'),
                age_unit=patient_data.get('patientonsetageunit'),
                sex=patient_data.get('patientsex'),
                weight=patient_data.get('patientweight')
            ),
            drugs=[
                Drug(
                    name=drug.get('medicinalproduct', 'Inconnu'),
                    active_ingredients=drug.get('openfda', {}).get('substance_name', []),
                    dosage_form=drug.get('drugdosageform'),
                    start_date=drug.get('drugstartdate'),
                    end_date=drug.get('drugenddate')
                )
                for drug in patient_data.get('drug', [])
            ],
            reactions=[
                Reaction(
                    term=reaction.get('reactionmeddrapt', 'Inconnue'),
                    outcome=reaction.get('reactionoutcome')
                )
                for reaction in patient_data.get('reaction', [])
            ]
        )

    @classmethod
    def from_api_data_cleaned(cls, data: dict) -> 'AdverseEventReport':
        """Crée un rapport à partir des données nettoyées de l'API."""
        from src.etl.data_cleaner import DataCleaner
        cleaned_data = DataCleaner.clean_report(data)
        
        return cls(
            report_id=cleaned_data['report_id'],
            received_date=cleaned_data['received_date'],
            patient=cleaned_data['patient'],
            drugs=cleaned_data['drugs'],
            reactions=cleaned_data['reactions'],
            source=cleaned_data['source'],
            processed_at=cleaned_data['processed_at']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le rapport en dictionnaire pour la sérialisation."""
        data = asdict(self)
        # Convertir les objets Patient, Drug, Reaction en dictionnaires
        data['patient'] = asdict(self.patient)
        data['drugs'] = [asdict(drug) for drug in self.drugs]
        data['reactions'] = [asdict(reaction) for reaction in self.reactions]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdverseEventReport':
        """Crée un rapport à partir d'un dictionnaire."""
        # Convertir les dictionnaires en objets
        patient_data = data.pop('patient', {})
        drugs_data = data.pop('drugs', [])
        reactions_data = data.pop('reactions', [])
        
        patient = Patient(**patient_data)
        drugs = [Drug(**drug) for drug in drugs_data]
        reactions = [Reaction(**reaction) for reaction in reactions_data]
        
        return cls(
            patient=patient,
            drugs=drugs,
            reactions=reactions,
            **data
        )