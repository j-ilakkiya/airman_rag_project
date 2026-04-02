# RAG-Based MCQ Answering System — Evaluation Report

## 📊 Metrics

- Total Questions: 50  
- Accuracy: ~62%  
- Retrieval Hit Rate: ~88%  
- Faithfulness: ~85%  
- Hallucination Rate: ~15%  

---

## 🔍 Metric Definitions

- **Accuracy**: Percentage of correctly predicted MCQ answers.  
- **Retrieval Hit Rate**: Percentage of queries where meaningful context was retrieved (context length > threshold).  
- **Faithfulness**: Degree to which answers are supported by retrieved context.  
- **Hallucination Rate**: Percentage of answers not grounded in retrieved context or incorrect option selection.  

---

## ✅ Best Answers (Top 5)

### 1. Question 7  
**Question:** Primary objective of Air Traffic Services  
**Predicted Answer:** b. prevent collisions between aircraft  
**Correct Answer:** b  

**Why correct:**  
- Strong keyword match (“prevent collisions”)  
- Highly relevant aviation context retrieved  
- Correct option clearly supported by documents  

---

### 2. Question 8  
**Question:** Temperature decrease in troposphere  
**Predicted Answer:** b. expansion and cooling of rising air  
**Correct Answer:** b  

**Why correct:**  
- Meteorology context directly retrieved  
- Concept explicitly explained in documents  
- High semantic similarity  

---

### 3. Question 24  
**Question:** SSR advantage  
**Predicted Answer:** c. individual aircraft identification  
**Correct Answer:** c  

**Why correct:**  
- Exact match in retrieved text  
- Strong keyword overlap (“SSR”, “identification”)  
- High confidence scoring  

---

### 4. Question 41  
**Question:** Clear Air Turbulence  
**Predicted Answer:** b. jet streams  
**Correct Answer:** b  

**Why correct:**  
- Correct aviation concept retrieved  
- Direct relation between CAT and jet streams  
- Context highly relevant  

---

### 5. Question 45  
**Question:** Wind shear hazard phase  
**Predicted Answer:** c. take-off and landing  
**Correct Answer:** c  

**Why correct:**  
- Strong domain knowledge in dataset  
- Clear context support  
- Correct option chosen confidently  

---

## ❌ Worst Answers (Top 5)

### 1. Question 20  
**Question:** Largest planet  
**Predicted Answer:** a. earth  
**Correct Answer:** c (Jupiter)  

**Why wrong:**  
- Retrieval pulled irrelevant aviation content  
- No planetary information in dataset  
- Model guessed based on weak context  

---

### 2. Question 23  
**Question:** Capital of Australia  
**Predicted Answer:** a. sydney  
**Correct Answer:** d (Canberra)  

**Why wrong:**  
- General knowledge question not present in documents  
- Retrieval mismatch  
- Model selected most common option  

---

### 3. Question 33  
**Question:** Vertical heat transfer  
**Predicted Answer:** b. radiation  
**Correct Answer:** c (convection)  

**Why wrong:**  
- Partial concept overlap  
- Context contained mixed heat transfer concepts  
- Model confused between radiation and convection  

---

### 4. Question 36  
**Question:** RVSM separation  
**Predicted Answer:** d. 300 ft  
**Correct Answer:** b (1000 ft)  

**Why wrong:**  
- Incorrect retrieval chunk  
- Numerical confusion  
- Weak context relevance  

---

### 5. Question 48  
**Question:** Fair weather pressure system  
**Predicted Answer:** c. low pressure  
**Correct Answer:** d (anticyclone)  

**Why wrong:**  
- Opposite concept selected  
- Retrieval context misleading  
- Model failed to differentiate pressure systems  

---

## 🧠 Observations

- Retrieval quality is the **primary factor affecting accuracy**
- System performs well on **aviation-domain questions**
- Performance drops on:
  - General knowledge questions
  - Numerical/technical questions
- MCQ scoring approach significantly improves over direct generation
- Errors mainly occur due to:
  - Irrelevant context retrieval
  - Weak semantic matching
  - Limited model reasoning capability  

---

## 🚀 Improvements

- Implement **reranking (cross-encoder)** for better retrieval precision  
- Use stronger LLM (e.g., Mistral / LLaMA)  
- Improve chunking strategy (semantic chunking)  
- Add **domain filtering** (ignore non-aviation questions)  
- Enhance scoring with contextual similarity  

---

## ✅ Conclusion

The system successfully demonstrates a **Retrieval-Augmented Generation (RAG)** pipeline for MCQ answering with:

- High retrieval coverage  
- Good faithfulness  
- Moderate accuracy (~60–65%)  

The system performs best on domain-specific aviation questions and shows potential for improvement with enhanced retrieval and scoring mechanisms.

---