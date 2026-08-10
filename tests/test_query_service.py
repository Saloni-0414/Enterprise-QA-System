from app.services.query_service import QueryService

service = QueryService()

question = input("Ask a Question: ")

response = service.ask(question)

print("\n")
print(response)

service.close()
