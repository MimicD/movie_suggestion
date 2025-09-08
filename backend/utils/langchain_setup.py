from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores.pgvector import PGVector
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from django.conf import settings

# Кастомные embeddings для all-MiniLM-L6-v2
class SentenceTransformerEmbeddings:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    def embed_query(self, text):
        return self.model.encode(text).tolist()
    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

embeddings = SentenceTransformerEmbeddings("all-MiniLM-L6-v2")

# LLM
llm = ChatOllama(model="gemma2:9b", temperature=0.2)

# Vector store
vectorstore = PGVector(
    connection_string=settings.PGVECTOR_CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="movies",
    collection_metadata={"hnsw_ef_search": 100}
)

# RAG prompt
rag_prompt_template = """
You are a movie recommendation expert. The user query is: "{query}"

Examples:
Query: "superhero movies but not Superman"
Output: [
    {{"title": "The Avengers", "overview": "Team of superheroes...", "reason": "Matches superhero theme, no Superman"}},
    {{"title": "Spider-Man", "overview": "Peter Parker...", "reason": "Matches superhero theme, no Superman"}}
]

Use the following movie contexts to suggest top {top_k} relevant films.
Strictly exclude any films that match these terms (consider synonyms like 'Man of Steel' for 'Superman'): {exclude_terms}

Contexts:
{context}

Output only valid JSON array. Do not include any extra text, comments, or explanations outside the JSON.
[
    {{"title": "Film Title", "overview": "Short summary", "reason": "Why it matches the query"}}
]
"""
RAG_PROMPT = PromptTemplate(
    template=rag_prompt_template,
    input_variables=["query", "top_k", "exclude_terms", "context"]
)