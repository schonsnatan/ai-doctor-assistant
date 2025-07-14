import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os
'''
1. Direct Vector Embedding Approach
- Process: Convert CSV rows/columns → Text chunks → Vector embeddings → Vector database
- Best for: Smaller datasets with clear semantic meaning
- Tools: LangChain's CSVLoader, LlamaIndex's CSVNodeParser
- Advantage: Simplest implementation with minimal preprocessing

'''


def preprocess_and_save(input_path: str, output_path: str):
    '''Loads and filters the raw CSV'''

    df = pd.read_csv("input_path", 
                    encoding="ISO-8859-1", sep=";")
    df = df[df["SITUACAO_REGISTRO"] == "VÁLIDO"].reset_index()
    df = df.drop(columns=["TIPO_PRODUTO", 
                        "DATA_FINALIZACAO_PROCESSO", 
                        "CATEGORIA_REGULATORIA", 
                        "NUMERO_REGISTRO_PRODUTO",
                        "DATA_VENCIMENTO_REGISTRO",
                        "NUMERO_PROCESSO",
                        "EMPRESA_DETENTORA_REGISTRO",
                        "SITUACAO_REGISTRO",
                        "index"]).drop_duplicates()
    df.to_csv(output_path, index=False, encoding="utf-8")


def load_documents_from_csv(path: str):
    ''' Load a CSV file into a list of Documents. Each document represents one row of the CSV file. 
        Every row is converted into a key/value pair and outputted to a new line in the document’s page_content.'''
    loader = CSVLoader(file_path=path, 
                       encoding="utf-8")
    
    return loader.load()



def create_vector_embeddings_from_csv(documents, persist_dir: str = "../data/vector_db/medicines"):
    '''Embeds and saves to FAISS'''
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(persist_dir)
     

def get_relevant_medicines(query: str, perist_dir: str = "../data/vector_db/medicines", k: int=5):
    ''' Can be imported by llm.py to retrieve top medicines based on query'''
     
if __name__ == "__main__":
    preprocess_and_save("../data/DADOS_ABERTOS_MEDICAMENTOS.csv", "../data/FILTERED_MEDICAMENTOS.csv")
    load_documents_from_csv("../data/FILTERED_MEDICAMENTOS.csv")