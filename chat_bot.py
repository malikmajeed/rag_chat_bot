from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os


class ChatBot:
    def __init__(self, temperature=0.7):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

        self.master_prompt = (
            "You are an expert university admission counselor for UET (University of Engineering and Technology). "
            "Your role is to help students with questions about UET admissions, programs, requirements, and procedures.\n\n"
            "IMPORTANT GUIDELINES:\n"
            "1. Base your answers primarily on the provided context from the UET prospectus.\n"
            "2. If the context contains relevant information, use it to provide accurate and detailed answers.\n"
            "3. If the context does not contain the answer or is insufficient, clearly state that you don't have that specific information in the provided context.\n"
            "4. Be helpful, professional, and encouraging in your responses.\n"
            "5. If asked about something not in the context, politely explain that you can only answer based on the available UET prospectus information.\n"
            "6. Format your responses clearly with proper paragraphs and structure."
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=temperature,
            api_key=openai_api_key
        )

    def generate_response(self, context, user_prompt, history=None):
        # Check if context is empty or indicates no context found
        if not context or context.strip() == "No specific context found in the knowledge base for this query.":
            system_prompt = (
                f"{self.master_prompt}\n\n"
                "NOTE: No relevant context was found in the knowledge base for this query. "
                "Please respond politely that you don't have specific information about this topic in the available documents."
            )
        else:
            system_prompt = (
                f"{self.master_prompt}\n\n"
                "RELEVANT CONTEXT FROM UET PROSPECTUS:\n"
                f"{context}\n\n"
                "Use the above context to answer the user's question. If the context doesn't fully answer the question, "
                "provide what information you can and mention what specific details might be missing."
            )

        messages = [
            SystemMessage(content=system_prompt)
        ]

        # Add history if provided
        if history:
            for msg in history:
                if msg["sender"] == "user":
                    messages.append(HumanMessage(content=msg["message"]))
                else:
                    messages.append(HumanMessage(content=f"Assistant: {msg['message']}")) # Or AIMessage if imported

        # Finally add current user prompt
        messages.append(HumanMessage(content=user_prompt))

        try:
            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            # Return a user-friendly error message
            if "API key" in str(e).lower() or "authentication" in str(e).lower():
                return "I'm having trouble connecting to the AI service. Please check the API configuration."
            elif "rate limit" in str(e).lower():
                return "The service is currently busy. Please try again in a moment."
            else:
                return f"I encountered an error while processing your request. Please try again or rephrase your question."
