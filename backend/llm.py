from config.settings import get_groq_api
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def get_ai_answer(patient_info: dict) -> str:
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt_template = (
        f"Sexo: {patient_info['sex']}\n"
        f"Idade: {patient_info['age']}\n"
        f"Duração do sintoma: {patient_info['duration']}\n"
        f"Sintomas: {', '.join(patient_info['sintomas'])}\n"
        f"Condições: {', '.join(patient_info['condicoes'])}\n"
        f"Alergias: {', '.join(patient_info['alergias'])}\n"
        f"Medicamentos contínuos: {patient_info['med_continuo']}\n"
        f"Reações adversas passadas: {patient_info['reacoes']}\n"
        f"Diagnóstico inicial do doutor: {patient_info['diagnostico']}\n"
        f"Diagnóstico inicial do doutor: {patient_info['diagnostico']}\n"
        f"Informação desejada: {patient_info['info_desejada']}\n"
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role":"system",
                "content": "Você é uma AI especializada em medicina. Com base nas informações fornecidas, sugira medicamentos ou exames apropriados, considerando a segurança do paciente."            },
            {
                "role":"user",
                "content":prompt_template,
            }
        ],
    )
    return response.choices[0].message.content