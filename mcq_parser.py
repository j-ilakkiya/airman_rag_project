import fitz
import re


def extract_mcqs(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    print("\n--- RAW TEXT PREVIEW ---\n")
    print(text[:1000])  # debug

    # 🔹 Split by question numbers like "1.", "2."
    questions = re.split(r'\n\s*\d+\.\s+', text)

    mcqs = []

    for q in questions:
        q = q.strip()

        # Check if it contains A, B, C, D options
        if all(opt in q for opt in ["A.", "B.", "C.", "D."]):

            # 🔹 Clean formatting
            q = re.sub(r'\n+', '\n', q)

            # 🔹 Ensure proper spacing
            q = q.replace("A.", "\nA.")
            q = q.replace("B.", "\nB.")
            q = q.replace("C.", "\nC.")
            q = q.replace("D.", "\nD.")

            mcqs.append(q.strip())

    return mcqs