"""This script sets up the Chroma DB with the sample text."""
import chromadb
from sentence_transformers import SentenceTransformer

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
        client = chromadb.HttpClient(host="chroma", port=8000)

        # Create an embedding function
        embedding_function = SentenceTransformer("all-MiniLM-L6-v2")

        # Get or create the collection
        collection = client.get_or_create_collection(name="dnd_lore")

        # Load the sample text
        with open("sample.txt", "r", encoding="utf-8") as f:
            sample_text = f.read()

        # Split the text into chunks without LangGraph
        chunks = chunk_text(sample_text)

        # Add the chunks to the collection
        # Note: The sentence-transformer library can handle the embedding for us.
        collection.add(
            embeddings=embedding_function.encode(chunks).tolist(),
            documents=chunks,
            ids=[f"chunk_{i}" for i, _ in enumerate(chunks)],
        )

        print("Successfully set up the Chroma DB.")

    except Exception as e:
        print(f"An error occurred during RAG setup: {e}")

if __name__ == "__main__":
    setup_rag()
