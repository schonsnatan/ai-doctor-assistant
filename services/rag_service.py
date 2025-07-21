import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

class RAGService:

    def __init__(self):
        self.base_path = "data"
        self.filtered_csv = os.path.join(self.base_path, "FILTERED_MEDICAMENTOS.csv")
        self.vector_dir = os.path.join(self.base_path, "vector_db", "medicines")

    @staticmethod
    def preprocess_and_save(input_path: str, output_path: str):
        '''
        Loads and filters the raw CSV
        '''

        df = pd.read_csv(input_path, 
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

    @staticmethod
    def load_documents_from_csv(path: str):
        ''' 
        Load a CSV file into a list of Documents. Each document represents one row of the CSV file. 
        Every row is converted into a key/value pair and outputted to a new line in the document’s page_content.
        '''
        loader = CSVLoader(file_path=path, 
                        encoding="utf-8")
        
        return loader.load()

    @staticmethod
    def create_vector_embeddings_from_csv(documents, persist_dir: str):
        '''Embeds and saves to FAISS'''
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(documents, embeddings)
        vector_store.save_local(persist_dir)
        
    @staticmethod
    def get_relevant_medicines(query: str, vector_db_path: str, k: int) -> str:
        ''' Can be imported by llm.py to retrieve top medicines based on query'''
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(vector_db_path, embeddings, allow_dangerous_deserialization=True)
        return db.similarity_search(query, k=k)
        
        
    def get_medicines(self, query: str, k: int):
        # Step 1: Check if filtered CSV exists
        if not os.path.exists(self.filtered_csv):
            self.preprocess_and_save(
                input_path=os.path.join(self.base_path, "DADOS_ABERTOS_MEDICAMENTOS.csv"),
                output_path=self.filtered_csv
            )

        # Step 2: Check if vector DB exists
        if not os.path.exists(self.vector_dir):
            docs = self.load_documents_from_csv(self.filtered_csv)
            self.create_vector_embeddings_from_csv(docs, self.vector_dir)

        # Step 3: Retrieve relevant medicines
        results = self.get_relevant_medicines(query, self.vector_dir, k)
        return results
