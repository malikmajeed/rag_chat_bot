from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


class VectorDatabase:
    def __init__(self):
        self.persist_directory = "./vector_db"
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        self.vector_store = Chroma(
            collection_name="Uet_Prospectus",
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents=documents)

    # def persist(self):
    #     self.vector_store.persist()

    def search(self, query_text, docs_to_search=3):
        result = self.vector_store.similarity_search(query=query_text, k=docs_to_search)
        return result