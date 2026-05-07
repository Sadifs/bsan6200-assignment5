# Ask My Resume — RAG Chatbot (Option A)

**BSAN 6200: Text Mining & Social Media Analytics — Spring 2026**

**Author:** Sadaf Sarbazi

---

## 1. Project Title and Option

**Option A — "Ask My Resume" RAG Chatbot**

---

## 2. Project Description

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about my professional background using personal career documents (resume, CV, statement of qualifications, and project write-ups). Users can ask natural-language questions like "What is this person's environmental science background?" and receive grounded, accurate answers pulled directly from source documents. Deployed live on Streamlit Cloud.

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
A public career summary (`data/about.txt`) is already included and powers the live demo. To enrich answers, add additional `.pdf` or `.txt` career documents to the `data/` folder — or use the sidebar file uploader in the running app.

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
| LLM | Qwen/Qwen2.5-7B-Instruct (via HuggingFace Inference API) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 (local, free) |
| Vector Store | NumPy cosine similarity |
| UI | Streamlit |
| Document Loader | PyPDF |

---

## 5. Paid vs. Free Path

- **Free path used:** HuggingFace Inference API (free tier) for LLM; `sentence-transformers` for local embeddings — no credit card required
- **Paid alternative:** Replace with OpenAI `gpt-4o-mini` + `text-embedding-3-small` for higher throughput and quality

---

## 6. Key Findings

- **Chunking:** Paragraph-aware chunking (26 chunks, avg 866 chars) outperformed fixed-size (64 chunks, avg 377 chars) by preserving semantic units from resume and SOQ sections
- **Evaluation:** Average quality score 4.2/5 across 10 test questions; 0 hallucinations; all 3 out-of-scope questions correctly refused
- **Prompt engineering:** Each iteration improved output quality — adding grounding reduced hallucination risk; adding tone/format guidance produced recruiter-appropriate responses
- **Failure patterns:** Factual retrieval missed degree information (Q1, score 2/5) because degree details were embedded in header sections; language coverage was incomplete (Q2, score 3/5) due to skills being spread across multiple chunks — increasing k from 3 to 5 would address both

---

## 7. File Descriptions

| File / Folder | Description |
|---|---|
| `streamlit_app.py` | Main Streamlit chat application |
| `notebooks/rag_pipeline.ipynb` | Full RAG pipeline: loading, chunking, embedding, retrieval, evaluation |
| `data/about.txt` | Public career summary (committed) — powers the live Streamlit demo |
| `data/` | Personal career documents (PDF/TXT — excluded from version control for privacy) |
| `evaluation/test_results.md` | Evaluation results: retrieval accuracy, prompt iterations, failure analysis |
| `memo.md` | Business memo summarizing findings for a technical manager audience |
| `ai_log.md` | AI usage log (8+ entries documenting tool use with progression) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from version control (includes all personal documents) |

---

## 8. Live Demo & Repository

**Live app:** [bsan6200-assignment5-ragchatbot.streamlit.app](https://bsan6200-assignment5-ragchatbot.streamlit.app)

**GitHub:** [github.com/Sadifs/bsan6200-assignment5](https://github.com/Sadifs/bsan6200-assignment5)
