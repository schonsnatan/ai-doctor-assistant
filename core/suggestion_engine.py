from typing import List
from core.patient import Patient
from strategies.base_strategy import BaseStrategy
from strategies.exam_strategy import ExamStrategy
from strategies.medicine_strategy import MedicineStrategy

class SuggestionEgine:
    
    def __init__(self):
        self._strategies = {
            "medicamentos": MedicineStrategy(),
            "exames": ExamStrategy()
        }
    
    def get_suggestion(self, strategy_name: str, patient: Patient) -> str:
        if strategy_name not in self._strategies:
            return "Tipo de sugestão desconhecida."
        
        strategy = self._strategies[strategy_name]
        return strategy.generate(patient)