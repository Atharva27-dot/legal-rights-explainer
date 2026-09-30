"""
Domain-aware legal document vector store.

Stores legal document embeddings and ensures every chunk
contains a legal domain in its metadata.
"""

import chromadb


class LegalVectorStore:

    DOMAIN_MAP = {

        "consumer protection act, 2019":
            "Consumer Protection",

        "information technology act, 2000":
            "Cyber / IT",

        "information technology act":
            "Cyber / IT",

        "motor vehicles act, 1988":
            "Motor Vehicle",

        "motor vehicles act":
            "Motor Vehicle",

        "indian contract act, 1872":
            "Contract",

        "indian contract act":
            "Contract",

        "industrial disputes act":
            "Employment / Labour",

        "code on wages":
            "Employment / Labour",

        "payment and settlement systems act":
            "Banking / Financial",

        "right to information act, 2005":
            "Right to Information",

        "right to information act":
            "Right to Information",

        "insurance":
            "Insurance / Financial",

    }

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="legal_documents"
        )

    # ============================================================
    # DOMAIN DETECTION
    # ============================================================

    def infer_domain(self, metadata):

        act = str(
            metadata.get("act", "")
        ).strip().lower()

        title = str(
            metadata.get("title", "")
        ).strip().lower()

        source = str(
            metadata.get("source", "")
        ).strip().lower()

        # --------------------------------------------------------
        # Explicit domain already provided
        # --------------------------------------------------------

        existing_domain = metadata.get("domain")

        if existing_domain:

            return existing_domain

        # --------------------------------------------------------
        # Match Act
        # --------------------------------------------------------

        for act_name, domain in self.DOMAIN_MAP.items():

            if act_name in act:

                return domain

        # --------------------------------------------------------
        # Fallback keyword detection
        # --------------------------------------------------------

        combined = " ".join([
            act,
            title,
            source
        ])

        if any(
            word in combined
            for word in [
                "consumer",
                "consumer protection"
            ]
        ):

            return "Consumer Protection"

        if any(
            word in combined
            for word in [
                "information technology",
                "cyber",
                "electronic transaction"
            ]
        ):

            return "Cyber / IT"

        if any(
            word in combined
            for word in [
                "motor vehicle",
                "motor vehicle",
                "road accident"
            ]
        ):

            return "Motor Vehicle"

        if any(
            word in combined
            for word in [
                "contract",
                "agreement"
            ]
        ):

            return "Contract"

        if any(
            word in combined
            for word in [
                "labour",
                "labor",
                "employment",
                "wages",
                "industrial dispute"
            ]
        ):

            return "Employment / Labour"

        if any(
            word in combined
            for word in [
                "insurance",
                "insurer",
                "insurance claim"
            ]
        ):

            return "Insurance / Financial"

        return "General Legal"

    # ============================================================
    # ADD CHUNKS
    # ============================================================

    def add_chunks(self, chunks, embeddings):

        ids = []
        documents = []
        metadatas = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            metadata = dict(
                chunk.metadata
            )

            # Add domain metadata
            metadata["domain"] = self.infer_domain(
                metadata
            )

            ids.append(
                chunk.id
            )

            documents.append(
                chunk.page_content
            )

            metadatas.append(
                metadata
            )

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings.tolist(),

            metadatas=metadatas

        )

        print(
            f"{len(ids)} chunks stored successfully."
        )

        # Show domains for debugging
        domains = sorted(
            set(
                metadata["domain"]
                for metadata in metadatas
            )
        )

        print(
            "Domains stored:",
            ", ".join(domains)
        )

    # ============================================================
    # COUNT
    # ============================================================

    def count(self):

        return self.collection.count()
