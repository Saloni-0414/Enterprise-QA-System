from app.rag.vector_store import VectorStore

db = VectorStore()

document_id = db.add_document(
    document_name="HR_Policy.pdf",
    document_hash="abc123456789",
    department="HR"
)

print("Document ID:", document_id)
