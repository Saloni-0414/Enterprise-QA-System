from pathlib import Path

from app.rag.loader import DocumentLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore

# Initialize modules
loader = DocumentLoader()
splitter = DocumentSplitter()
embedding_model = EmbeddingModel()
db = VectorStore()

pdf_path = "enterprise_docs/IT-Policy.pdf"

print("=" * 60)
print("STEP 1 : Loading PDF")
print("=" * 60)

documents = loader.load_pdf(pdf_path)

print(f"Pages Loaded : {len(documents)}")

print("\nSTEP 2 : Generating Document Hash")

document_hash = loader.generate_document_hash(pdf_path)

print(document_hash)

print("\nSTEP 3 : Checking Duplicate")

existing = db.document_exists(document_hash)

if existing:
    print(f"Document already exists (ID: {existing[0]})")
    exit()

print("No duplicate found.")

print("\nSTEP 4 : Storing Document Metadata")

document_name = Path(pdf_path).name

document_id = db.add_document(
    document_name=document_name,
    document_hash=document_hash
)

print(f"Document ID : {document_id}")

print("\nSTEP 5 : Splitting Document")

chunks = splitter.split_documents(documents)

print(f"Chunks Created : {len(chunks)}")

print("\nSTEP 6 : Generating Embeddings")

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

print(f"Embeddings Generated : {len(embeddings)}")

print("\nSTEP 7 : Storing Chunks")

stored = db.add_chunks(
    document_id=document_id,
    chunks=chunks,
    embeddings=embeddings
)

print(f"Chunks Stored : {stored}")

db.close()

print("\nSUCCESS! Document Indexed Successfully.")
