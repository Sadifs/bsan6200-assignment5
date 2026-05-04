# Ask My Resume — RAG Chatbot (Option A)

**BSAN 6200: Text Mining & Social Media Analytics — Spring 2026**

**Author:** Sadaf Sarbazi

---

## 1. Project Description

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about my professional background using my personal career documents (resume, LinkedIn profile, GitHub portfolio, and personal bio). Users can ask natural-language questions like "What experience do you have in data analytics?" and receive grounded, accurate answers pulled directly from source documents.

---

## 2. Setup Instructions

### Prerequisites
- Python 3.10+
- An OpenAI API key (or alternative — see below)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure API key
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_key_here
```

### Run the Streamlit app
```bash
streamlit run streamlit_app.py
```

### Run the notebook
Open `notebooks/rag_pipeline.ipynb` in Jupyter and run all cells top-to-bottom.

---

## 3. Models & Tools Used

| Component | Tool / Model |
|---|---|
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | text-embedding-3-small (OpenAI) |
| Vector Store | FAISS |
| RAG Framework | LangChain |
| UI | Streamlit |
| Document Loader | PyPDF, LangChain loaders |

---

## 4. Paid vs. Free Path

- **Paid path used:** OpenAI API (~$1–3 estimated total cost)
- **Free alternative:** Replace OpenAI embeddings with `sentence-transformers/all-MiniLM-L6-v2` and LLM with a HuggingFace Inference API model or local Ollama (`llama3`)

---

## 5. Key Findings

- Chunking strategy comparison: fixed-size vs. sentence-aware splitting
- Retrieval accuracy on standard vs. edge-case queries
- Prompt iteration results and measurable improvements

---

## 6. File Descriptions

| File / Folder | Description |
|---|---|
| `streamlit_app.py` | Main Streamlit chat application |
| `notebooks/rag_pipeline.ipynb` | Full RAG pipeline: loading, chunking, embedding, retrieval, evaluation |
| `data/` | Personal career documents (resume, LinkedIn, GitHub, bio) |
| `evaluation/test_results.md` | Evaluation results: retrieval accuracy, prompt iterations, failure analysis |
| `memo.md` | Business memo summarizing findings |
| `ai_log.md` | AI usage log (8+ entries) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from version control |

---

## 7. Repository

[github.com/Sadifs/bsan6200-assignment5](https://github.com/Sadifs/bsan6200-assignment5)
