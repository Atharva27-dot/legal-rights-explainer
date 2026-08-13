from app.rag.retriever import LegalRetriever
from app.llm.prompt_builder import PromptBuilder

retriever = LegalRetriever()

builder = PromptBuilder()

question = input("Question: ")

results = retriever.search(question)

documents = results["documents"][0]

prompt = builder.build(question, documents)

print(prompt)