# ✈️ RAG-Based MCQ Answering System

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system to answer multiple-choice questions (MCQs) using aviation-related documents.

The system retrieves relevant information from a collection of PDFs and selects the correct option based on grounded context, minimizing hallucination and improving answer reliability.

---

## 🚀 Features

* 📄 PDF-based knowledge ingestion
* 🔍 Hybrid retrieval (Keyword + Vector Search)
* 🧠 MCQ answering using option scoring
* ❌ Hallucination control (context-based answering)
* 📊 Evaluation metrics (accuracy, faithfulness, etc.)
* 🌐 FastAPI-based `/ask` endpoint

---

## 🧠 System Architecture

```
PDF Documents → Chunking → Embeddings → FAISS Index
        ↓
MCQ Input → Query Cleaning → Hybrid Retrieval
        ↓
Context → Option Scoring (LLM) → Final Answer
```

---

## 🧱 Tech Stack

* Python
* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS (Vector Database)
* HuggingFace Transformers (`flan-t5-base`)
* FastAPI (API layer)

---

## 📂 Project Structure

```
airman_rag_project/
│
├── data/                  # Aviation PDFs
├── mcq.pdf                # MCQ input file
├── ingest.py              # PDF loading & chunking
├── rag.py                 # Core RAG pipeline
├── mcq_parser.py          # Extract MCQs from PDF
├── api.py                 # FastAPI application
├── evaluate.py            # Evaluation script
├── report.md              # Evaluation report
└── README.md              # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd airman_rag_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install sentence-transformers faiss-cpu transformers fastapi uvicorn pydantic pymupdf
```

---

## ▶️ How to Run

### 🔹 Run RAG System

```bash
python rag.py
```

---

### 🔹 Run API

```bash
uvicorn api:app
```

Open in browser:

👉 http://127.0.0.1:8000/docs

---

### 🔹 Test API

```json
{
  "question": "The primary objective of Air Traffic Services is:\n\na. Maximise airport capacity\nb. Prevent collisions between aircraft\nc. Control airline schedules\nd. Enforce customs regulations"
}
```

---

### 🔹 Run Evaluation

```bash
python evaluate.py
```

---

## 📊 Evaluation Metrics

| Metric             | Description                 |
| ------------------ | --------------------------- |
| Accuracy           | Correct MCQ answers         |
| Retrieval Hit Rate | Relevant context retrieved  |
| Faithfulness       | Answers grounded in context |
| Hallucination Rate | Unsupported answers         |

---

## 📈 Results

* Accuracy: ~60–65%
* Retrieval Hit Rate: ~85–90%
* Faithfulness: High
* Hallucination Rate: Low

---

## ✅ Key Design Decisions

* MCQ questions are **not stored in vector DB** (avoids data leakage)
* Hybrid retrieval improves relevance
* Scoring-based MCQ selection instead of text generation
* Query cleaning improves embedding quality

---

## ⚠️ Limitations

* Depends heavily on retrieval quality
* Struggles with general knowledge questions
* Limited reasoning capability of base model

---

## 🚀 Future Improvements

* Use stronger LLM (Mistral / LLaMA)
* Add reranking for retrieval
* Improve chunking strategy
* Domain filtering for better precision

---

## 📌 Conclusion

This project demonstrates a complete end-to-end RAG system for grounded MCQ answering with strong retrieval and explainability.

---

## 🙌 Acknowledgment

Developed as part of an AI/ML project to explore document-based question answering systems.

---
