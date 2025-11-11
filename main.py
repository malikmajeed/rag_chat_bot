from chat_bot import ChatBot
from vector_db import VectorDatabase
edu_bot = ChatBot()
vector_db = VectorDatabase()

#taking user prompt as input

user_prompt = input("Enter your question about UET admission: ")

# searching in vector db to get context related to user prompt

context_docs = vector_db.search(query_text=user_prompt, docs_to_search=3)

# generating response from chat bot through its method and passing it
#context and user prompt
response = edu_bot.generate_response(context=context_docs, user_prompt=user_prompt)

print(f"Response: {response}")