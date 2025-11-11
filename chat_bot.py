from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os


class ChatBot:
    def __init__(self, temperature=0.7):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")

        self.master_prompt = (
            "Act as an expert university admission counselor. "
            "Never give answers outside the provided context. "
            "If you don't know the answer, just say you don't know."
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",  # valid OpenAI model
            temperature=temperature,
            api_key=openai_api_key
        )

    def generate_response(self, context, user_prompt):
        system_prompt = f"{self.master_prompt}\n\nContext:\n{context}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.model.invoke(messages)
        return response.content
