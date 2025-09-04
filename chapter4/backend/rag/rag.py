"""RAG setup and chain for the TTRPG GM Assistant."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
import chromadb

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Connect to the Chroma DB service
client = chromadb.HttpClient(host="chroma", port=8000)
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma(
    client=client,
    collection_name="dnd_lore",
    embedding_function=embedding_function,
)
retriever = vector_store.as_retriever()

rag_prompt_template = """
You are a TTRPG Game Master assistant. Use the following pieces of context to answer the user's question about the campaign world.
If you don't know the answer, just say that you don't have that information. Do not try to make up an answer.

Context:
{context}

Question:
{question}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
