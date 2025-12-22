from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import warnings
import os
import sys
import logging
from io import StringIO

# Suppress TensorFlow and protobuf warnings/errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning messages

# Suppress warnings
warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('transformers').setLevel(logging.ERROR)

# Filter stderr to suppress protobuf AttributeError messages
class FilterStderr:
    def __init__(self):
        self.stderr = sys.stderr
        self.buffer = StringIO()
    
    def write(self, text):
        # Filter out protobuf AttributeError messages
        if 'AttributeError' in text and 'GetPrototype' in text:
            return  # Suppress this specific error
        self.stderr.write(text)
    
    def flush(self):
        self.stderr.flush()


class VectorDatabase:
    def __init__(self):
        self.persist_directory = "./vector_db"
        
        # Suppress protobuf errors during model loading
        filter_stderr = FilterStderr()
        original_stderr = sys.stderr
        sys.stderr = filter_stderr
        
        try:
            # Suppress warnings during model loading
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            # Restore stderr to show real errors
            sys.stderr = original_stderr
            print(f"Error during embedding model initialization: {e}")
            raise
        finally:
            # Restore original stderr
            sys.stderr = original_stderr

        self.vector_store = Chroma(
            collection_name="Uet_Prospectus",
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

    def add_documents(self, documents):
        if not documents:
            return
        
        source = documents[0].metadata.get('source', 'unknown source')
        print(f"Embedding step started for: {source}")
        self.vector_store.add_documents(documents=documents)
        print(f"Successfully added documents from: {source}")

    def is_document_present(self, source_name):
        """Check if documents from this source are already in the vector database."""
        try:
            results = self.vector_store.get(where={"source": source_name}, limit=1)
            return len(results['ids']) > 0
        except Exception as e:
            print(f"Error checking for document presence: {e}")
            return False

    # def persist(self):
    #     self.vector_store.persist()

    def search(self, query_text, docs_to_search=3):
        try:
            if not query_text or not query_text.strip():
                return []
            
            # Perform similarity search
            result = self.vector_store.similarity_search(query=query_text.strip(), k=docs_to_search)
            
            # Filter out empty results
            result = [doc for doc in result if doc.page_content and doc.page_content.strip()]
            
            return result
        except Exception as e:
            print(f"Error in vector database search: {e}")
            # Return empty list instead of raising to allow graceful degradation
            return []