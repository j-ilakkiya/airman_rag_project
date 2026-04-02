from fastapi import FastAPI
from pydantic import BaseModel

# 🔥 Import your functions from rag.py
from rag import (
    load_pdfs,
    chunk_text,
    embed_texts,
    create_faiss_index,
    hybrid_search,
    build_context,
    generate_answer,
    extract_question_only
)

app = FastAPI()


# 🔹 Request format
class QueryRequest(BaseModel):
    question: str


# 🔥 LOAD EVERYTHING ONCE (IMPORTANT)
print("Loading RAG system...")

folder_path = r"C:\Users\mohan\OneDrive\Desktop\airman_rag_project\data"

pages = load_pdfs(folder_path)
chunks = chunk_text(pages)
embeddings = embed_texts(chunks)
index = create_faiss_index(embeddings)

print("RAG system ready!")


# 🚀 MAIN API
@app.post("/ask")
def ask_question(request: QueryRequest):
    query = request.question

    # 🔥 Clean query for better retrieval
    clean_query = extract_question_only(query) + " aviation concept explanation"

    results = hybrid_search(clean_query, index, chunks)
    context = build_context(results)

    answer = generate_answer(query, context)

    citations = [
        {"document": r["doc_name"], "page": r["page"]}
        for r in results[:3]
    ]

    return {
        "question": query,
        "answer": answer,
        "citations": citations
    }