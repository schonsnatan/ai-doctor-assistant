from .base_strategy import BaseStrategy
from core.patient import Patient
from services.llm_service import LLMService
from services.rag_service import RAGService

# TO BE IMPLEMENTED

class ExamStrategy(BaseStrategy):
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_Service = RAGService()
    
    def generate(self, patient) -> str:
        
        return self.llm_service.generate_exam_suggestion(patient.get_patient_data())