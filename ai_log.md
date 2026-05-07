# AI Usage Log — BSAN 6200 Assignment 5

## Tool: Claude Code
---

### Entry 1 

**Prompt:** Set up repo structure with all required files for Option A

**AI Suggestion:** Created README.md, .gitignore, requirements.txt, ai_log.md, memo.md, evaluation/test_results.md with scaffold content

**What I Used:** All scaffold files

**Modified:** Revised README to include all 8 required sections per assignment spec; updated .gitignore to explicitly exclude data/*.pdf and data/*.txt for privacy

---

### Entry 2 

**Prompt:** What LLM should I use for the free HuggingFace inference path?

**AI Suggestion:** HuggingFaceH4/zephyr-7b-beta (from starter code)

**What I Used:** Qwen/Qwen2.5-7B-Instruct

**Modified:** Tested multiple models when zephyr returned a 400 Bad Request error ("not supported by any provider you have enabled"). Switched to Qwen2.5-7B-Instruct which worked correctly on the first attempt.

---

### Entry 3

**Prompt:** Build document loading and chunking pipeline for career documents

**AI Suggestion:** Two strategies — fixed-size (chunk_size=400, overlap=50) and paragraph-aware (max_chunk=600, overlap=80)

**What I Used:** Kept both implementations for comparison as required

**Modified:** Chose paragraph-aware as final strategy based on quantitative comparison: 64 chunks (avg 377 chars) vs 26 chunks (avg 866 chars). Paragraph-aware preserves semantic units from the resume and SOQ structure.

---

### Entry 4

**Prompt:** Build ChromaDB vector store using sentence-transformers embeddings

**AI Suggestion:** Use SentenceTransformerEmbeddingFunction with all-MiniLM-L6-v2 via chromadb.utils

**What I Used:** Used as suggested

**Modified:** Ran three test similarity queries to verify retrieval before proceeding — confirmed correct source documents returned for Python, data analytics, and machine learning queries.

---

### Entry 5

**Prompt:** Connect vector store to HuggingFace LLM to build the full RAG chain

**AI Suggestion:** rag_query() combining retrieve() + ask_llm() with max_tokens=150

**What I Used:** Used the structure as suggested

**Modified:** Increased max_tokens from 150 to 300 — found that 150 tokens cut answers mid-sentence on technical questions. Verified the full pipeline returns grounded answers citing correct sources.

---

### Entry 6

**Prompt:** Copy chunking strategy from notebook into streamlit_app.py

**AI Suggestion:** Paste chunk_paragraph() with the same parameters as the notebook

**What I Used:** Used as suggested

**Modified:** Confirmed parameters (max_chunk=600, overlap=80) match notebook choice — no changes needed.

---

### Entry 7

**Prompt:** Help me understand what my system prompt needs to do per assignment instructions

**AI Suggestion:** Explained 5 elements: who the bot is, where answers come from, out-of-scope handling, tone, format — and suggested a v1→v2→v3 progression structure

**What I Used:** Used the structural framework to write 3 iterations myself

**Modified:** Provided my own content for each version; AI formatted/cleaned the language but the design decisions (what to include at each stage, what the grounding constraint should say) were mine

---

### Entry 9 — 2026-05-06

**Prompt:** Fix chromadb import error on Streamlit Cloud (TypeError in opentelemetry/protobuf chain)

**AI Suggestion:** Pin protobuf<5.0.0 to resolve the version conflict

**What I Used:** Removed chromadb entirely; replaced with numpy cosine similarity over sentence-transformers embeddings

**Modified:** The protobuf pin didn't fix the issue because Streamlit Cloud was running Python 3.14, which breaks protobuf's C extension metaclass regardless of version. Replacing chromadb with a lightweight numpy dot-product search eliminated the entire opentelemetry/protobuf dependency chain. This was a better solution than fighting version constraints — simpler code, no external vector store dependency, works on any Python version, and produces identical retrieval results since the same embedding model is used.

---

### Entry 8 *(Case where my approach beat AI suggestion)*

**Prompt:** What LLM should I use for the HuggingFace Inference API free path?

**AI Suggestion:** HuggingFaceH4/zephyr-7b-beta (from starter code)

**What I Used:** Qwen/Qwen2.5-7B-Instruct

**Why My Approach Was Better:** Zephyr returned a 400 Bad Request error ("not supported by any provider you have enabled") immediately — the AI's suggestion was non-functional on my account's free tier. I tested Qwen/Qwen2.5-7B-Instruct as an alternative and it worked correctly on the first attempt, returning grounded, well-formed answers. The measurable difference: zephyr produced zero usable outputs; Qwen powered the entire evaluation set of 10 questions with an average score of 4.2/5. The AI defaulted to the starter code recommendation without accounting for provider availability — my approach of testing an alternative directly was faster and more effective.
