# Ask My Resume — RAG Chatbot (Option A)

**BSAN 6200: Text Mining & Social Media Analytics — Spring 2026**

**Author:** Sadaf Sarbazi

---

## 1. Project Title and Option

**Option A — "Ask My Resume" RAG Chatbot**

---

## 2. Project Description

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about my professional background using personal career documents (resume, statement of qualifications, LinkedIn profile, and project write-ups). Users can ask natural-language questions like "What experience do you have in data analytics?" and receive grounded, accurate answers pulled directly from source documents.

---

## 3. Setup Instructions

### Prerequisites
- Python 3.10+
- A free HuggingFace account and API token ([huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)) — enable "Make calls to Inference Providers"

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure API key
Create a `.env` file in the root directory:
```
HF_TOKEN=hf_your_token_here
```

### Add your documents
Place `.pdf` or `.txt` career documents in the `data/` folder (minimum 3–5 files).

### Run the Streamlit app
```bash
streamlit run streamlit_app.py
```

### Run the notebook
Open `notebooks/rag_pipeline.ipynb` in Jupyter and run all cells top-to-bottom.

---

## 4. Models & Tools Used

| Component | Tool / Model |
|---|---|
| LLM | HuggingFaceH4/zephyr-7b-beta (via HuggingFace Inference API) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 (local, free) |
| Vector Store | ChromaDB |
| UI | Streamlit |
| Document Loader | PyPDF |

---

## 5. Paid vs. Free Path

- **Free path used:** HuggingFace Inference API (free tier) for LLM; `sentence-transformers` for local embeddings — no credit card required
- **Paid alternative:** Replace with OpenAI `gpt-4o-mini` + `text-embedding-3-small` for higher throughput and quality

---

## 6. Key Findings

> *(To be completed after evaluation — see `evaluation/test_results.md`)*

- Chunking strategy comparison: fixed-size vs. sentence-aware splitting
- Retrieval accuracy across factual, inference, out-of-scope, and specificity queries
- Prompt iteration results and measurable improvements

---

## 7. File Descriptions

| File / Folder | Description |
|---|---|
| `streamlit_app.py` | Main Streamlit chat application |
| `notebooks/rag_pipeline.ipynb` | Full RAG pipeline: loading, chunking, embedding, retrieval, evaluation |
| `data/` | Personal career documents (local only — excluded from version control) |
| `evaluation/test_results.md` | Evaluation results: retrieval accuracy, prompt iterations, failure analysis |
| `memo.md` | Business memo summarizing findings for a technical manager audience |
| `ai_log.md` | AI usage log (8+ entries documenting tool use with progression) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from version control (includes all personal documents) |

---

## 8. Repository

[github.com/Sadifs/bsan6200-assignment5](https://github.com/Sadifs/bsan6200-assignment5)
