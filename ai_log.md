# AI Usage Log — BSAN 6200 Assignment 5

**Project:** Ask My Resume RAG Chatbot (Option A)
**Author:** Sadaf Sarbazi

---

## Summary Table

| # | Date | Tool | What I Asked | What I Used | What I Modified |
|---|------|------|-------------|-------------|-----------------|
| 1 | 2026-05-04 | Claude Code | Set up repo structure and required files | Scaffold files (README, .gitignore, requirements.txt, ai_log, memo, evaluation) | Updated README sections to match assignment spec exactly |
| 2 | 2026-05-04 | Claude Code | Which HuggingFace model to use for free-tier LLM | Suggested zephyr-7b-beta | Switched to Qwen/Qwen2.5-7B-Instruct after zephyr failed with 400 error |
| 3 | 2026-05-04 | Claude Code | Build document loading and chunking pipeline | PyPDF + two chunking strategies (fixed-size and paragraph-aware) | Kept paragraph-aware after comparing chunk counts: 26 vs 64 chunks |
| 4 | 2026-05-04 | Claude Code | Build ChromaDB vector store with sentence-transformers | SentenceTransformerEmbeddingFunction with all-MiniLM-L6-v2 | Used as-is — verified with similarity search queries |
| 5 | 2026-05-04 | Claude Code | Build retrieval chain connecting vector store to LLM | rag_query() function with retrieve + ask_llm | Adjusted max_tokens from 150 to 300 for more complete answers |
| 6 | 2026-05-06 | Claude Code | Implement chunking function in streamlit_app.py | Copied chunk_paragraph from notebook | Used as-is — matches the strategy chosen in notebook |
| 7 | [Date] | Claude Code | [Your prompt engineering session — fill in] | [What it suggested] | [What you changed] |
| 8 | [Date] | [Tool] | [Case where your approach beat the AI — fill in] | [What AI suggested] | **Why your approach was better:** [explain] |

---

## Detailed Entries

### Entry 1 — 2026-05-04
**Tool:** Claude Code
**Prompt:** Set up repo structure with all required files for Option A
**AI Suggestion:** Created README.md, .gitignore, requirements.txt, ai_log.md, memo.md, evaluation/test_results.md with scaffold content
**What I Used:** All scaffold files
**Modified:** Revised README to include all 8 required sections per assignment spec; updated .gitignore to explicitly exclude data/*.pdf and data/*.txt for privacy

---

### Entry 2 — 2026-05-04
**Tool:** Claude Code
**Prompt:** What LLM should I use for the free HuggingFace inference path?
**AI Suggestion:** HuggingFaceH4/zephyr-7b-beta (from starter code)
**What I Used:** Qwen/Qwen2.5-7B-Instruct
**Modified:** Tested multiple models when zephyr returned a 400 Bad Request error ("not supported by any provider you have enabled"). Switched to Qwen2.5-7B-Instruct which worked correctly on the first attempt.

---

### Entry 3 — 2026-05-04
**Tool:** Claude Code
**Prompt:** Build document loading and chunking pipeline for career documents
**AI Suggestion:** Two strategies — fixed-size (chunk_size=400, overlap=50) and paragraph-aware (max_chunk=600, overlap=80)
**What I Used:** Kept both implementations for comparison as required
**Modified:** Chose paragraph-aware as final strategy based on quantitative comparison: 64 chunks (avg 377 chars) vs 26 chunks (avg 866 chars). Paragraph-aware preserves semantic units from the resume and SOQ structure.

---

### Entry 4 — 2026-05-04
**Tool:** Claude Code
**Prompt:** Build ChromaDB vector store using sentence-transformers embeddings
**AI Suggestion:** Use SentenceTransformerEmbeddingFunction with all-MiniLM-L6-v2 via chromadb.utils
**What I Used:** Used as suggested
**Modified:** Ran three test similarity queries to verify retrieval before proceeding — confirmed correct source documents returned for Python, data analytics, and machine learning queries.

---

### Entry 5 — 2026-05-04
**Tool:** Claude Code
**Prompt:** Connect vector store to HuggingFace LLM to build the full RAG chain
**AI Suggestion:** rag_query() combining retrieve() + ask_llm() with max_tokens=150
**What I Used:** Used the structure as suggested
**Modified:** Increased max_tokens from 150 to 300 — found that 150 tokens cut answers mid-sentence on technical questions. Verified the full pipeline returns grounded answers citing correct sources.

---

### Entry 6 — 2026-05-06
**Tool:** Claude Code
**Prompt:** Copy chunking strategy from notebook into streamlit_app.py
**AI Suggestion:** Paste chunk_paragraph() with the same parameters as the notebook
**What I Used:** Used as suggested
**Modified:** Confirmed parameters (max_chunk=600, overlap=80) match notebook choice — no changes needed.

---

### Entry 7 — [Date]
**Tool:** [Tool you used]
**Prompt:** [What you asked during prompt engineering]
**AI Suggestion:** [What it suggested — if anything]
**What I Used:** [What you actually used]
**Modified:** [What you changed from the suggestion]

---

### Entry 8 — [Date] *(Case where my approach beat AI suggestion)*
**Tool:** [Tool]
**Prompt:** [What you asked]
**AI Suggestion:** [What it suggested]
**What I Used:** [Your approach instead]
**Why My Approach Was Better:** [Explain the measurable difference]

---
