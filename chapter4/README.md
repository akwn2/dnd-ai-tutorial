# Chapter 4: Add Knowledge – Build a Lore Keeper with RAG

Time to give your assistant a memory. You’ll wire a vector database (Chroma) and retrieve relevant context for better answers.

## What you’ll build
- A Chroma service that persists across rebuilds
- A seeding script that embeds `sample.txt`
- A RAG function that retrieves and augments prompts

## Step 1: Seed Chroma
`rag_setup.py` reads `sample.txt`, chunks it, computes embeddings, and writes them to the `dnd_lore` collection.

Run the stack:
```
docker-compose up --build
```

## Step 2: Ask questions
Open `http://localhost:8501` and ask: “What are the Sunken Spires?” The model reads retrieved context before answering.

## Diagram
```mermaid
flowchart TD
    A[User question] --> B[Embed question]
    B --> C[Query Chroma (top‑K)]
    C --> D[Build context string]
    D --> E[Call model with augmented prompt]
    E --> F[Return grounded answer]
```

## How it works
- `backend/rag/rag.py`: Encodes the question, queries Chroma (HTTP client), builds a context string, and calls the model with the augmented prompt.
- `docker-compose.yaml`: Adds the `chroma` service with a volume so your vectors persist.

## Exercises
- Change chunk sizes/overlap in the seeding script and observe answer quality.
- Add a “Top-K” selector to experiment with different retrieval depths.

## Tips
- High-quality, diverse chunks → better retrieval. Keep `sample.txt` curated.

## Theory background
- RAG basics: Retrieve top‑K relevant chunks, then let the model answer with those chunks as context. This reduces hallucinations and improves grounding.
- Embeddings: Sentences are mapped to vectors such that similar meanings are near each other in vector space. Cosine similarity is commonly used.
- Vector stores: Chroma stores your vectors and provides fast similarity search.

## Milestone checks
- Milestone 1: `rag_setup.py` logs added chunks and there are IDs in the collection.
- Milestone 2: Questions about your lore produce grounded answers, not “I don’t have that information.”

## Common pitfalls
- Forgetting to seed the DB—your retriever returns nothing.
- Using too large/small chunk sizes—hurts retrieval quality.

## Knowledge check
- What problem does RAG solve compared to prompting alone?
- Why do we need both documents and embeddings to be persisted?

## Resources
- RAG overview: https://www.coursera.org/learn/retrieval-augmented-generation-rag
- Chroma docs: https://docs.trychroma.com/docs/overview/getting-started
- Google AI for Developers - Embeddings: https://ai.google.dev/gemini-api/docs/embeddings
- Similarity search basics: https://towardsdatascience.com/what-is-cosine-similarity-how-to-compare-text-and-images-in-python-d2bb6e411ef0/