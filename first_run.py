from pdf_handler import PDFHandler
from vector_db import VectorDatabase

# pdf_path = "./PROPECTUS 2022-23.pdf"
# # Creating an instance and giving it pdf path
# pdf_handler = PDFHandler(document_path=pdf_path)
# # getting the chunks list from the pdf_handler instance
# documents = pdf_handler.load_and_split()


# # creating instance of vector database
vector_db = VectorDatabase()
# # adding document recived from pdf handler to vector db
# vector_db.add_documents(documents=documents)

#now searching in vector db
query = "What are the admission requirements for undergraduate programs at UET?"
results = vector_db.search(query_text=query, docs_to_search=3)


for i in range(len(results)):
    print(f"Document {i+1}:\n{results[i].page_content}\n")
