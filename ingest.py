import fitz
import os
import re


def load_pdfs(folder_path):
    documents = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            doc = fitz.open(file_path)

            for i, page in enumerate(doc):
                text = page.get_text()

                if not text.strip():
                    continue

                text_lower = text.lower()

                # ❌ Remove noisy pages
                if any(word in text_lower for word in ["contents", "index", "appendix"]):
                    continue

                documents.append({
                    "text": text,
                    "page": i + 1,
                    "doc_name": file_name
                })

    return documents


# 🔹 Smart chunk filter
def is_good_chunk(text):
    text_lower = text.lower()

    # ❌ Remove MCQs
    if re.search(r"\b(a\.|b\.|c\.|d\.)", text_lower):
        return False

    # ❌ Remove question patterns
    if "refer to" in text_lower or "question" in text_lower:
        return False

    # ❌ Remove short chunks
    if len(text) < 200:
        return False

    # ❌ Remove numeric-heavy chunks
    if len(re.findall(r"\d+", text)) > 15:
        return False

    # ❌ Must have sentence structure
    if "." not in text:
        return False

    return True


def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if is_good_chunk(chunk):
                chunks.append({
                    "text": chunk,
                    "page": page["page"],
                    "doc_name": page["doc_name"]
                })

            start += chunk_size - overlap

    return chunks


# 🔹 TEST
if __name__ == "__main__":
    folder_path = r"C:\Users\mohan\OneDrive\Desktop\airman_rag_project\data"

    pages = load_pdfs(folder_path)
    print("Pages:", len(pages))

    chunks = chunk_text(pages)
    print("Chunks:", len(chunks))

    print("\nSample chunk:\n", chunks[0])