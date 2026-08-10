from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL


class EmbeddingModel:
    """
    Generates embeddings for document chunks
    and user queries.
    """

    def __init__(self):

        self.model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """
        Generate embeddings for document chunks.
        """

        if not texts:
            raise ValueError("No text found to generate embeddings.")

        return self.model.embed_documents(texts)

    def embed_query(
        self,
        query: str
    ) -> list[float]:
        """
        Generate embedding for a user query.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        return self.model.embed_query(query)
