from app.rag.loader import DocumentLoader

loader = DocumentLoader()

pdf_path = "enterprise_docs/IT-Policy.pdf"

documents = loader.load_pdf(pdf_path)

print(f"Total Pages: {len(documents)}")

print("\nDocument Hash:")
print(loader.generate_document_hash(pdf_path))

print("\nFirst Page Preview:")
print(documents[0].page_content[:500])

print("\nMetadata:")
print(documents[0].metadata)
