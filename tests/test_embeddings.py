from app.rag.loader import DocumentLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embeddings import EmbeddingModel

loader = DocumentLoader()
splitter = DocumentSplitter()
embedding_model = EmbeddingModel()

pdf_path = "enterprise_docs/IT-Policy.pdf"

documents = loader.load_pdf(pdf_path)

chunks = splitter.split_documents(documents)

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

print(f"Total Chunks: {len(chunks)}")
print(f"Total Embeddings: {len(embeddings)}")
print(f"Embedding Dimension: {len(embeddings[0])}")

print("\nFirst 10 values of the first embedding:")
print(embeddings[0][:10])
