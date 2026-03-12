"""
ChromaDB-backed RAG (Retrieval-Augmented Generation) operations.

All queries and upserts are scoped by event_id metadata to enforce
multi-tenant isolation within a single ChromaDB collection.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings

# ---------------------------------------------------------------------------
# ChromaDB Client Initialization
# ---------------------------------------------------------------------------

_chroma_client: chromadb.ClientAPI | None = None
_COLLECTION_NAME = "event_knowledge_base"


def get_chroma_client() -> chromadb.ClientAPI:
    """
    Return the singleton persistent ChromaDB client.

    Lazily initializes on first call.
    """
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _chroma_client


def get_collection() -> chromadb.Collection:
    """Get or create the shared knowledge-base collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


# ---------------------------------------------------------------------------
# RAG Query
# ---------------------------------------------------------------------------

def query_rag(event_id: int, question: str, n_results: int = 3) -> tuple[str, float]:
    """
    Query the ChromaDB collection filtered by event_id.

    Args:
        event_id: The tenant event identifier.
        question: The user's natural-language question.
        n_results: Maximum number of results to retrieve.

    Returns:
        A tuple of (best_answer, confidence_score).
        If no documents are found, returns ("", 0.0).
    """
    collection = get_collection()

    # Check if the collection has any documents for this event
    try:
        results = collection.query(
            query_texts=[question],
            n_results=n_results,
            where={"event_id": str(event_id)},
        )
    except Exception:
        # Collection may be empty or have no matching metadata
        return ("", 0.0)

    # Extract the best result
    if not results["documents"] or not results["documents"][0]:
        return ("", 0.0)

    best_document = results["documents"][0][0]
    # ChromaDB returns distances; for cosine space, similarity = 1 - distance
    best_distance = results["distances"][0][0] if results["distances"] else 1.0
    confidence = max(0.0, 1.0 - best_distance)

    return (best_document, round(confidence, 4))


# ---------------------------------------------------------------------------
# RAG Upsert (Active Learning)
# ---------------------------------------------------------------------------

def add_to_rag(event_id: int, question: str, answer: str) -> str:
    """
    Concatenate Q&A, embed, and upsert into ChromaDB with event_id metadata.

    This enables active learning: organizer-provided answers become part
    of the knowledge base for future RAG queries.

    Args:
        event_id: The tenant event identifier.
        question: The original user question.
        answer: The organizer-provided answer.

    Returns:
        The document ID used for the upsert.
    """
    collection = get_collection()

    # Create a meaningful document from Q&A
    document = f"Question: {question}\nAnswer: {answer}"
    doc_id = f"event_{event_id}_q_{abs(hash(question)) % 10**10}"

    collection.upsert(
        ids=[doc_id],
        documents=[document],
        metadatas=[{"event_id": str(event_id), "source": "organizer_resolution"}],
    )

    return doc_id
