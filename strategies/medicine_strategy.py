from .base_strategy import BaseStrategy
from core.patient import Patient
from services.llm_service import LLMService
from services.rag_service import RAGService
import re

class MedicineStrategy(BaseStrategy):
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()
    
    def generate(self, patient: Patient) -> str:
        
        initial_query = self.llm_service.generate_medicine_query(patient.get_patient_data())
        retrieved_docs = self.rag_service.get_medicines(initial_query, k=30)
        safe_docs = self._filter_allergic_medicines(retrieved_docs, patient)
        final_suggestion = self.llm_service.generate_final_medicine_suggestion(patient.get_patient_data(), safe_docs, initial_query)
        return final_suggestion

    def _filter_allergic_medicines(self, documents: list, patient: Patient) -> list:
        """
        Filtra documentos que contenham termos associados a alergias ou reações adversas do paciente.
        """

        # 🔹 Extrai e normaliza termos proibidos
        def normalize_terms(raw):
            if isinstance(raw, str):
                return [t.strip().lower() for t in raw.split(",") if t.strip()]
            elif isinstance(raw, list):
                return [t.strip().lower() for t in raw if t.strip()]
            return []

        allergies = normalize_terms(patient.alergias)
        reactions = normalize_terms(patient.reacoes)
        forbidden_terms = set(allergies + reactions)

        print(f"DEBUG: termos proibidos detectados => {forbidden_terms}")

        if not forbidden_terms:
            return documents  # Nenhum termo para filtrar

        safe_docs = []

        for doc in documents:
            content = doc.page_content.lower()
            if any(re.search(rf'\b{re.escape(term)}\b', content) for term in forbidden_terms):
                matched_term = next(term for term in forbidden_terms if re.search(rf'\b{re.escape(term)}\b', content))
                print(f"DEBUG: Documento descartado por conter '{matched_term}'")
                continue
            safe_docs.append(doc)

        print(f"DEBUG: {len(safe_docs)} documentos aprovados.")
        return safe_docs