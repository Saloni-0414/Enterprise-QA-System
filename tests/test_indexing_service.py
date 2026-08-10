from app.services.indexing_service import IndexingService


service = IndexingService()

result = service.index_document(
    pdf_path="enterprise_docs/IT-Policy.pdf",
    document_name="IT-Policy.pdf"
)

print(result)

service.close()
