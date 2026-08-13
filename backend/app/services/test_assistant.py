from app.services.legal_assistant import LegalAssistant

assistant = LegalAssistant()

while True:

    question = input("\nAsk a legal question: ")

    if question.lower() == "exit":
        break

    answer = assistant.ask(question)

    print("\n")
    print(answer)
    