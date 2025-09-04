"""This script sets up the Chroma DB with the sample text."""
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def setup_rag():
    """Sets up the RAG chain by creating and populating a Chroma DB."""
    try:
        # Connect to the Chroma DB service
        client = chromadb.HttpClient(host="chroma", port=8000)

        # Create an embedding function
        embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Get or create the collection
        collection = client.get_or_create_collection(
            name="dnd_lore"
        )

        # Load the sample text
        with open("sample.txt", "r", encoding="utf-8") as f:
            sample_text = f.read()

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(sample_text)

        # Add the chunks to the collection
        collection.add(
            embeddings=embedding_function.embed_documents(chunks),
            documents=chunks,
            ids=[f"chunk_{i}" for i, _ in enumerate(chunks)],
        )

        print("Successfully set up the Chroma DB.")

    except Exception as e:
        print(f"An error occurred during RAG setup: {e}")

if __name__ == "__main__":
    setup_rag()
