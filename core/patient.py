from typing import List

class Patient:
    
    def __init__(self, sex: str, 
                 age: int, duration: str, 
                 sintomas: List[str], 
                 condicoes: List[str], 
                 alergias: List[str], 
                 med_continuo: str, 
                 reacoes: str, 
                 diagnostico: str):
        
        self.sex: str = sex
        self.age: int = age
        self.duration: str = duration
        self.sintomas: List[str] = sintomas
        self.condicoes: List[str] = condicoes
        self.alergias: List[str] = alergias
        self.med_continuo: str = med_continuo
        self.reacoes: str = reacoes
        self.diagnostico: str = diagnostico

    def get_patient_allergies(self) -> List[str]:
        return self.alergias
    
    def get_patient_reacoes(self) -> List[str]:
        return self.reacoes

    def get_patient_data(self) -> str:
        return (
            f"Sexo: {self.sex}\n"
            f"Idade: {self.age}\n"
            f"Duração dos sintomas: {self.duration}\n"
            f"Sintomas: {', '.join(self.sintomas)}\n"
            f"Condições: {', '.join(self.condicoes)}\n"
            f"Alergias: {', '.join(self.alergias)}\n"
            f"Medicamentos de uso contínuo: {self.med_continuo}\n"
            f"Reações adversas: {self.reacoes}\n"
            f"Diagnóstico inicial: {self.diagnostico}"
        )

        