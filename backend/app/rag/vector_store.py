"""
vector_store.py

Stores legal document embeddings in ChromaDB.
"""

import chromadb


class LegalVectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="legal_documents"
        )

    def add_chunks(self, chunks, embeddings):

        ids = []
        documents = []
        metadatas = []

        for chunk, embedding in zip(chunks, embeddings):

            ids.append(chunk.id)

            documents.append(chunk.page_content)

            metadatas.append(chunk.metadata)

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings.tolist(),

            metadatas=metadatas

        )

        print(f"{len(ids)} chunks stored successfully.")

    def count(self):

        return self.collection.count()