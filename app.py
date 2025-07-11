import streamlit as st
from backend.llm import get_ai_answer

st.set_page_config(page_title="Doctor Assistant", layout="wide")
st.title("🤖 Doctor Assistant")

tab1, tab2, tab3, tab4 = st.tabs(["👤 Paciente", "🩺 Histórico", "🧠 Análise", "💡 Sugestão"])


with tab1:
    st.subheader("Informações do Paciente")
    col1, col2, col3 = st.columns(3)
    sex = col1.radio("Sexo", ["Homem", "Mulher"], horizontal=True)
    age = col2.number_input("Idade", 0, 120)
    duration = col3.text_input("Duração do sintoma", placeholder="Ex: 3 dias")
    sintomas = st.multiselect("Sintomas", 
               ["Tosse","Coriza","Dor de Cabeça","Febre","Dor no corpo","Formigamento","Diarreia","Insônia","Dor nas costas"], 
               placeholder="Selecione os sintomas do paciente")
    condicoes = st.multiselect("Condições do Paciente", 
               ["Hipertensão","Diabetes","Cancer"], 
               placeholder="Selecione as condições do paciente")
    alergias = st.text_area("Alergias (separadas por vírgula)")

with tab2:
    st.subheader("Histórico de medicamentos")
    medicamentos_uso_continuo = st.text_input("Medicamentos de uso contínuo")
    reacoes_adversas_passado = st.text_input("Reações adversas passadas")

with tab3:
    st.subheader("Análise Inicial do Doutor")
    diagnostico = st.text_area("Diagnóstico / Análise inicial")

with tab4:
    st.subheader("Sugestões Inteligentes")

    patient_info = {
        "sex": sex,
        "age": age,
        "duration": duration,
        "sintomas": sintomas,
        "condicoes": condicoes,
        "alergias": alergias.split(","),
        "med_continuo": medicamentos_uso_continuo,
        "reacoes": reacoes_adversas_passado,
        "diagnostico": diagnostico,
        "info_desejada": ""
    }

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💊 Sugerir Medicamentos"):
            patient_info["info_desejada"] = "fornecer orientação sobre medicamentos"
            with st.spinner("Analisando..."):
                suggestion = get_ai_answer(patient_info)
                st.success(suggestion)

    with col2:
        if st.button("🧪 Sugerir Exames"):
            patient_info["info_desejada"] = "fornecer orientação sobre exames"
            with st.spinner("Analisando..."):
                suggestion = get_ai_answer(patient_info)
                st.success(suggestion)