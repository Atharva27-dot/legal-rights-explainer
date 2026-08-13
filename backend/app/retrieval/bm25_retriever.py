from rank_bm25 import BM25Okapi
import re


class BM25Retriever:

    def __init__(self, documents):

        self.documents = documents

        tokenized_docs = [
            re.findall(r"\b\w+\b", doc.lower())
            for doc in documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query, top_k=5):

        tokenized_query = re.findall(r"\b\w+\b", query.lower())

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]