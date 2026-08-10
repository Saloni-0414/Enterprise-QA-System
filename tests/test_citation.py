from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.rag.generator import ResponseGenerator
from app.rag.citation import CitationGenerator


embedding_model = EmbeddingModel()

db = VectorStore()

generator = ResponseGenerator()

citation_generator = CitationGenerator()


question = "What is the password policy?"

query_embedding = embedding_model.embed_query(question)

retrieved_chunks = db.similarity_search(
    query_embedding
)


print("\n" + "=" * 60)
print("RETRIEVED CHUNKS")
print("=" * 60)

for chunk in retrieved_chunks:

    print("\nDocument:", chunk["document_name"])
    print("Page:", chunk["page"])
    print("Distance:", chunk["distance"])
    print("Content:", chunk["chunk_text"][:300])


answer = generator.generate_answer(
    question,
    retrieved_chunks
)

citations = citation_generator.generate_citations(
    retrieved_chunks
)

final_response = citation_generator.format_response(
    answer,
    citations
)


print("\n" + "=" * 60)
print("FINAL RESPONSE")
print("=" * 60)

print(final_response)

db.close()
