# 🩺 Doctor Assistant — AI Medical Support Tool

**Doctor Assistant** is an AI-powered application designed to assist doctors in suggesting medications and exams based on patient-provided clinical information.

The project is built with Python using Streamlit for the frontend, integrated with the LLaMA-3 model via Groq API. A RAG (Retrieval-Augmented Generation) module is under development to enhance suggestions with reliable sources, such as official documents from ANVISA (Brazil’s health regulatory agency).

---

## 🚧 Project Status

✅ Features already implemented:

- Interactive UI for structured patient data input
- Medication and exam suggestions powered by AI (via Groq API)
- Poetry-based dependency and environment management

🚧 In development:

- Integration with **RAG** using official Brazilian datasets (e.g., ANVISA)
- Validation against legally approved medications
- Evidence-based reasoning and citations in suggestions

---

## 🛠️ Tech Stack

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Poetry](https://python-poetry.org/)
- [LangChain](https://www.langchain.com/)
- [Groq API](https://console.groq.com/)
- [Pandas](https://pandas.pydata.org/)

---

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/doctor-assistant.git
   cd doctor-assistant

2. Install dependencies using Poetry:
   ```python
   poetry install

3. Add your Groq API key to a .env file:
   ```ini
   GROQ_API_KEY=your_key_here
   
4. Run the streamlit app:
   
   ```python
   poetry run streamlit run run_app.py
