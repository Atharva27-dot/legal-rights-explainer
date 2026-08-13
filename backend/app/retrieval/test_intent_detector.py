from app.retrieval.intent_detector import IntentDetector

detector = IntentDetector()

while True:

    question = input("Question: ")

    if question.lower() == "exit":
        break

    print("Intent:", detector.detect(question))
    print()