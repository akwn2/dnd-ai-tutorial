"""This script sets up the Chroma DB with the sample text."""
import chromadb
from google import genai
import os

from backend.services.llm import client


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Splits text into overlapping chunks."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def setup_rag():
    """Sets up the RAG chain by creating and populating a Chroma DB."""
    try:
        # Connect to the Chroma DB service
        db_client = chromadb.HttpClient(host="chroma", port=8000)

        # Create an embedding function
        embedding_model = "models/embedding-001"

        # Get or create the collection
        collection = db_client.get_or_create_collection(name="dnd_lore")

        # Load the sample text
        with open("sample.txt", "r", encoding="utf-8") as f:
            sample_text = f.read()

        # Split the text into chunks without LangGraph
        chunks = chunk_text(sample_text)

        # Add the chunks to the collection
        response = client.models.embed_content(
            model=embedding_model,
            contents=chunks,
        )
        collection.add(
            embeddings=[embedding.values for embedding in response.embeddings],
            documents=chunks,
            ids=[f"chunk_{i}" for i, _ in enumerate(chunks)],
        )

        print("Successfully set up the Chroma DB.")

    except Exception as e:
        print(f"An error occurred during RAG setup: {e}")

if __name__ == "__main__":
    setup_rag()
