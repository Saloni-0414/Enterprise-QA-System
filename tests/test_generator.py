from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.rag.generator import ResponseGenerator

embedding_model = EmbeddingModel()
db = VectorStore()
generator = ResponseGenerator()

question = "What are the IT security guidelines?"

query_embedding = embedding_model.embed_query(question)

results = db.similarity_search(query_embedding)

print("\nRetrieved Chunks:\n")

for r in results:
    print("=" * 80)
    print("Document :", r[0])
    print("Page :", r[1])
    print("Distance :", r[3])
    print()
    print(r[2])

answer = generator.generate_answer(
    question,
    results
)

print("\nFinal Answer:\n")
print(answer)
