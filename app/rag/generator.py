import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from torch import chunk

from app.config import LLM_MODEL

load_dotenv()


class ResponseGenerator:
    """
    Generates answers using the retrieved
    document chunks.
    """

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

    def build_context(
        self,
        retrieved_chunks
    ) -> str:
        """
        Build structured context for the LLM.
        """

        context_parts = []

        for chunk in retrieved_chunks:

            document_name = chunk["document_name"]
            page_number = chunk["page"]
            chunk_text = chunk["chunk_text"]


            context_parts.append(f"""
Document : {document_name}
Page : {page_number}

{chunk_text}

------------------------------------------------------------

""" )

        return "\n --------------------------------------------------------------------------------------------------------------------------------------------\n".join(context_parts)

    def generate_answer(
        self,
        question: str,
        retrieved_chunks
    ) -> str:
        """
        Generate answer from retrieved chunks.
        """

        context = self.build_context(retrieved_chunks)

        prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY from the provided context.

Rules:

1. Do not use outside knowledge.
2. If the answer is unavailable, reply:
   "I couldn't find this information in the uploaded enterprise documents."
3. Give a concise and accurate answer.
4. Do not mention page numbers or document names in the answer.
5. Citations will be added separately.

Context:

{context}

Question:

{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content
