from app.rag.vector_store import VectorStore

db = VectorStore()

document_hash = "abc123"

result = db.document_exists(document_hash)

if result:
    print(f"Document already exists. ID: {result[0]}")
else:
    print("Document does not exist.")
