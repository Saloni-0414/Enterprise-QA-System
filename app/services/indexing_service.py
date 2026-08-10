from pathlib import Path

from app.rag.loader import DocumentLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


class IndexingService:
    """
    Handles the complete document indexing workflow.

    Workflow:
    PDF → Load → Hash → Duplicate Check → Split
        → Embeddings → PostgreSQL + pgvector
    """

    def __init__(self):

        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter()
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def index_document(
        self,
        pdf_path: str,
        document_name: str
    ):
        """
        Index a PDF document into PostgreSQL + pgvector.

        Returns:
            Dictionary containing indexing status and metadata.
        """

        pdf_path = Path(pdf_path).resolve()

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"Document not found: {pdf_path}"
            )

        # 1. Generate document hash
        document_hash = self.loader.generate_document_hash(
            str(pdf_path)
        )

        # 2. Check for duplicate document
        existing_document = self.vector_store.document_exists(
            document_hash
        )

        if existing_document:
            return {
                "success": False,
                "message": "Document already exists.",
                "document_id": existing_document[0]
            }

        # 3. Load PDF
        documents = self.loader.load_pdf(
            str(pdf_path)
        )

        if not documents:
            raise ValueError(
                "No content could be extracted from the PDF."
            )

        # 4. Split document into chunks
        chunks = self.splitter.split_documents(
            documents
        )

        if not chunks:
            raise ValueError(
                "No chunks were created from the document."
            )

        # 5. Store document metadata
        document_id = self.vector_store.add_document(
            document_name=document_name,
            document_hash=document_hash
        )

        # Add document ID to chunk metadata
        for chunk in chunks:
            chunk.metadata["document_id"] = document_id

        # 6. Generate embeddings
        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        # 7. Store chunks and embeddings
        stored_chunks = self.vector_store.add_chunks(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "success": True,
            "message": "Document indexed successfully.",
            "document_id": document_id,
            "document_name": document_name,
            "pages": len(documents),
            "chunks": stored_chunks
        }

    def close(self):
        """
        Close database connection.
        """

        self.vector_store.close()
