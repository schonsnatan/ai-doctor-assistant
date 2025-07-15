# llm.py
from groq import Groq
from dotenv import load_dotenv
import os
from backend.rag_pipeline import get_medicines

load_dotenv()

def get_ai_answer(patient_info: dict) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    base_prompt = (
        f"Sexo: {patient_info['sex']}\n"
        f"Idade: {patient_info['age']}\n"
        f"Duração do sintoma: {patient_info['duration']}\n"
        f"Sintomas: {', '.join(patient_info['sintomas'])}\n"
        f"Condições: {', '.join(patient_info['condicoes'])}\n"
        f"Alergias: {', '.join(patient_info['alergias'])}\n"
        f"Medicamentos contínuos: {patient_info['med_continuo']}\n"
        f"Reações adversas passadas: {patient_info['reacoes']}\n"
        f"Diagnóstico inicial do doutor: {patient_info['diagnostico']}\n"
        f"Informação desejada: {patient_info['info_desejada']}\n"
    )

    first_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    '''Você é um motor de busca biomédico. Sua tarefa é converter um quadro clínico em uma lista de termos técnicos para uma busca vetorial em uma base de dados de medicamentos.

                    **Objetivo:** Gerar uma string, separada por vírgulas, contendo os termos mais relevantes para encontrar medicamentos adequados.

                    **O que incluir na sua resposta:**
                    - Classes terapêuticas relevantes (ex: "analgésico", "antipirético", "anti-inflamatório não esteroide", "anti-histamínico").
                    - Princípios ativos potencialmente indicados (ex: "ibuprofeno", "loratadina").
                    - Mecanismos de ação, se aplicável (ex: "inibidor da COX-2").
                    - Sintomas-chave a serem tratados (ex: "tosse produtiva", "congestão nasal", "dor de cabeça tensional").

                    **Regras CRÍTICAS:**
                    1.  **NUNCA** inclua na sua lista qualquer termo (princípio ativo, classe, etc.) que esteja presente nas 'Alergias' ou 'Reações adversas passadas' do paciente.
                    2.  Sua saída deve ser **APENAS** a lista de termos, separados por vírgula. Não adicione frases como "Com base no quadro, os termos são:" ou qualquer outra explicação.

                    **Exemplo de saída desejada para um paciente com febre e dor no corpo, sem alergias:**
                    analgésico, antipirético, anti-inflamatório, ibuprofeno, dor de cabeça, febre, dor muscular
                    '''
                )
            },
            {
                "role": "user",
                "content": base_prompt
            }
        ]
    )

    initial_analysis = first_response.choices[0].message.content

    retrieved_docs_raw = get_medicines(initial_analysis, k=30)

    filtered_docs = filter_allergic_medicines(
        documents=retrieved_docs_raw,
        allergies=patient_info['alergias'],
        reactions=patient_info['reacoes']
    )

    if not filtered_docs:
        return "Com base na análise inicial, não foi encontrado nenhum medicamento seguro no banco de dados que não esteja associado às alergias ou reações adversas do paciente. Recomenda-se uma avaliação médica mais aprofundada."

    docs_text = "\n---\n".join([doc.page_content for doc in filtered_docs])

    # 🧠 Etapa 3: Faz nova pergunta à LLM, agora com contexto do RAG
    final_prompt = (
        f"{base_prompt}\n"
        f"Análise clínica inicial da IA:\n{initial_analysis}\n\n"
        f"Lista de medicamentos encontrados com base nessa análise:\n{docs_text}\n\n"
        f"Com base no histórico clínico do paciente, nas alergias e reações passadas, e nos medicamentos encontrados, indique as melhores opções, justificando clinicamente sua recomendação. "
        f"Evite sugerir medicamentos com risco potencial. Use linguagem acessível."
    )

    final_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é uma IA médica confiável. Avalie cuidadosamente os dados clínicos e os medicamentos encontrados e dê sugestões seguras e bem fundamentadas. "
                    "Evite qualquer menção a medicamentos que o paciente não deve utilizar."
                )
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )

    print("🔬 Documentos retornados pelo RAG:\n", docs_text)  # Para debug opcional
    return final_response.choices[0].message.content


def filter_allergic_medicines(documents: list, allergies: list, reactions: str) -> list:
    """
    Filtra documentos de medicamentos que contêm substâncias alérgicas ou que causaram reações.
    """
    # Junta todas as substâncias a serem evitadas em uma lista
    forbidden_terms = [a.strip().lower() for a in allergies if a.strip()]
    if reactions.strip():
        # Adiciona também as reações passadas como termos a serem evitados
        forbidden_terms.extend([r.strip().lower() for r in reactions.split(',') if r.strip()])
    
    if not forbidden_terms:
        return documents

    safe_docs = []
    for doc in documents:
        content_lower = doc.page_content.lower()
        is_forbidden = False
        for term in forbidden_terms:
            # Verifica se o termo proibido está no conteúdo do documento
            if term in content_lower:
                is_forbidden = True
                print(f"DEBUG: Documento descartado por conter '{term}'.") # Opcional: para debug
                break
        
        if not is_forbidden:
            safe_docs.append(doc)
            
    return safe_docs