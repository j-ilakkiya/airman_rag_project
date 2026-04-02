from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from ingest import load_pdfs, chunk_text
from mcq_parser import extract_mcqs

# 🔹 Load models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


# 🔹 Embeddings
def embed_texts(chunks):
    texts = [chunk["text"] for chunk in chunks]
    return np.array(embed_model.encode(texts))


# 🔹 FAISS
def create_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


# 🔹 Vector search
def vector_search(index, query, chunks, k=12):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]


# 🔹 Keyword search
def keyword_search(query, chunks, k=12):
    query_words = query.lower().split()
    scored = []

    for chunk in chunks:
        text = chunk["text"].lower()
        score = sum(1 for word in query_words if word in text)

        if " is " in text or " are " in text:
            score += 2

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]


# 🔹 Hybrid search
def hybrid_search(query, index, chunks):
    keyword_results = keyword_search(query, chunks, k=12)

    if len(keyword_results) < 5:
        vector_results = vector_search(index, query, chunks, k=12)
        return keyword_results + vector_results

    return keyword_results


# 🔥 Extract clean question (IMPORTANT FIX)
def extract_question_only(question):
    lines = question.split("\n")
    q_text = []

    for line in lines:
        line = line.strip().lower()

        if line.startswith(("a.", "b.", "c.", "d.")):
            break

        q_text.append(line)

    return " ".join(q_text)


# 🔹 Build context
def build_context(results):
    context = ""

    for r in results:
        context += r["text"] + "\n\n"

    return context


# 🔹 Extract options
def extract_options(question):
    options = {}

    for line in question.split("\n"):
        line = line.strip().lower()

        if line.startswith("a."):
            options["a"] = line[2:].strip()
        elif line.startswith("b."):
            options["b"] = line[2:].strip()
        elif line.startswith("c."):
            options["c"] = line[2:].strip()
        elif line.startswith("d."):
            options["d"] = line[2:].strip()

    return options


# 🔥 FINAL ANSWER LOGIC (SCORING)
def generate_answer(question, context):
    if not context:
        return "This information is not available in the provided document(s)."

    context = context[:2000]
    # 🔥 NEW (context quality check)
    if len(context.strip()) < 100:
        return "This information is not available in the provided document(s)."
    options = extract_options(question)

    best_option = None
    best_score = -1

    for key, option in options.items():

        input_text = f"""
You are an aviation expert.

Based ONLY on the context, rate how correct the following statement is.

Return ONLY a number from 0 to 10:
0 = completely incorrect
10 = completely correct

Context:
{context}

Statement:
{option}
"""

        inputs = tokenizer(input_text, return_tensors="pt", truncation=True)

        outputs = model.generate(**inputs, max_new_tokens=5)

        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        try:
            score = int(response)
        except:
            score = 0

# 🔥 NEW (keyword boost)
        if option.lower() in context.lower():
            score += 3
# 🔥 PARTIAL MATCH BOOST (important)
        common_words = set(option.lower().split()) & set(context.lower().split())
        score += len(common_words) * 0.5 

        if score > best_score:
            best_score = score
            best_option = key

    if best_option is None:
        return "This information is not available in the provided document(s)."

    if best_score < 3:
        return "This information is not available in the provided document(s)."

    return f"{best_option}. {options[best_option]}"


# 🔹 MAIN
if __name__ == "__main__":
    folder_path = r"C:\Users\mohan\OneDrive\Desktop\airman_rag_project\data"

    print("Loading PDFs...")
    pages = load_pdfs(folder_path)

    print("Chunking...")
    chunks = chunk_text(pages)

    print("Embedding...")
    embeddings = embed_texts(chunks)

    print("Building index...")
    index = create_faiss_index(embeddings)

    # 🔥 MCQ INPUT
    mcq_file = r"C:\Users\mohan\OneDrive\Desktop\airman_rag_project\mcq.pdf"
    questions = extract_mcqs(mcq_file)

    print(f"\nTotal MCQs found: {len(questions)}")

    for i, query in enumerate(questions):
        print(f"\n\n🔍 Question {i+1}:\n{query}")

        # 🔥 KEY FIX → CLEAN QUERY
        clean_query = extract_question_only(query) + " aviation concept explanation"

        results = hybrid_search(clean_query, index, chunks)

        context = build_context(results)

        answer = generate_answer(query, context)

        print("\n✅ Answer:")
        print(answer)

        print("\n📌 Citations:")
        for r in results[:3]:
            print(f"{r['doc_name']} - Page {r['page']}")