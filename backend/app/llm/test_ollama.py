from app.llm.ollama_service import OllamaService

llm = OllamaService()

question = input("Ask: ")

answer = llm.generate(question)

print("\n")
print(answer)