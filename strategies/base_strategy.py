from abc import ABC, abstractmethod
from core.patient import Patient

class BaseStrategy(ABC):
    @abstractmethod
    def generate(self, patient: Patient) -> str:
        "Generate a suggestion based on patient data"
        pass
