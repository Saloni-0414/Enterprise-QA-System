from app.rag.loader import DocumentLoader
from app.rag.splitter import DocumentSplitter

loader = DocumentLoader()
splitter = DocumentSplitter()

pdf_path = "enterprise_docs/IT-Policy.pdf"

documents = loader.load_pdf(pdf_path)

chunks = splitter.split_documents(documents)

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0].page_content)

print("\nMetadata:\n")
print(chunks[0].metadata)
