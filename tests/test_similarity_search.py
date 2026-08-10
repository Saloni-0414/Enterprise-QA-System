from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore

embedding_model = EmbeddingModel()

db = VectorStore()

query = "What is the leave policy?"

query_embedding = embedding_model.embed_query(query)

results = db.similarity_search(query_embedding)

for result in results:

    print("=" * 60)

    print("Document :", result[0])

    print("Page     :", result[1])

    print("Distance :", result[3])

    print()

    print(result[2])
