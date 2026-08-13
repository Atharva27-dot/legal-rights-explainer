from app.retrieval.keyword_extractor import KeywordExtractor

extractor = KeywordExtractor()

while True:

    question = input("Question: ")

    if question.lower() == "exit":
        break

    keywords = extractor.extract(question)

    print("Keywords:")

    print(keywords)

    print()