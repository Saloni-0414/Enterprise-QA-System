from app.rag.loader import DocumentLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore

loader = DocumentLoader()
splitter = DocumentSplitter()
embedding_model = EmbeddingModel()
db = VectorStore()

pdf_path = "enterprise_docs/IT-Policy.pdf"

documents = loader.load_pdf(pdf_path)

document_hash = loader.generate_document_hash(pdf_path)

existing = db.document_exists(document_hash)

if existing:
    document_id = existing[0]
else:
    document_id = db.add_document(
        "IT-Policy.pdf",
        document_hash,
        "General"
    )

chunks = splitter.split_documents(documents)

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

db.add_chunks(
    document_id,
    chunks,
    embeddings
)

print("Chunks Stored Successfully!")
