from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.rag.generator import ResponseGenerator
from app.rag.citation import CitationGenerator


class QueryService:
    """
    Handles the complete question-answering workflow.
    """

    def __init__(self):

        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.generator = ResponseGenerator()
        self.citation_generator = CitationGenerator()

    def ask(self, question: str):
        """
        Process a user question and return
        answer with structured citations.
        """

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # 1. Generate query embedding
        query_embedding = self.embedding_model.embed_query(
            question
        )

        # 2. Retrieve relevant chunks
        retrieved_chunks = self.vector_store.similarity_search(
            query_embedding
        )

        # 3. Generate answer
        answer = self.generator.generate_answer(
            question,
            retrieved_chunks
        )

        # 4. Generate structured citations
        citations = self.citation_generator.generate_citations(
            retrieved_chunks
        )

        return {
            "answer": answer,
            "sources": citations
        }

    def close(self):
        """
        Close database connection.
        """

        self.vector_store.close()
