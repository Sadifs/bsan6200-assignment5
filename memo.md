# Business Memo

**To:** BSAN 6200 Course Staff
**From:** Sadaf Sarbazi
**Date:** May 6, 2026
**Re:** Ask My Resume — RAG Chatbot (Option A)

---

## Executive Summary

This project built a Retrieval-Augmented Generation (RAG) chatbot that answers natural-language questions about my professional background using personal career documents — resume, CV, statement of qualifications, and GitHub project write-ups. The system runs entirely on free tools (HuggingFace Inference API and local sentence-transformers) with no paid API required. Evaluation across 10 test questions produced an average quality score of 4.2/5 with zero hallucinations, demonstrating that a free-tier RAG pipeline can deliver accurate, grounded answers suitable for a recruiter audience.

---

## Problem Statement

Recruiters and hiring managers often need to quickly assess a candidate's fit across multiple dimensions — experience, skills, projects, and goals. Traditional static resumes require manual reading and offer no interactivity. This project builds an AI-powered chatbot that allows anyone to ask natural-language questions about my professional background and receive accurate, grounded answers drawn directly from source documents.

---

## Technical Approach

Four career documents were loaded using PyPDF and plain-text readers: a resume, CV, statement of qualifications, and a GitHub portfolio summary. Documents were split using a paragraph-aware chunking strategy (26 chunks, avg 866 characters), which preserves semantic units like resume sections and project descriptions better than fixed-size splitting (which produced 64 fragmented chunks at 377 characters each). Chunks were embedded using `sentence-transformers/all-MiniLM-L6-v2` (local, free) and stored in a ChromaDB vector store. At query time, the top-3 most relevant chunks are retrieved and passed with the user's question to `Qwen/Qwen2.5-7B-Instruct` via the HuggingFace Inference API. The full pipeline is surfaced through a Streamlit chat interface.

| Component | Tool |
|---|---|
| LLM | Qwen/Qwen2.5-7B-Instruct (HuggingFace Inference API) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 (local, free) |
| Vector Store | ChromaDB |
| Document Loader | PyPDF |
| UI | Streamlit |

---

## Key Findings

The system achieved an average quality score of 4.2/5 across 10 evaluation questions spanning four categories. Out-of-scope questions (salary, address, years of experience) were handled correctly in all three cases — the chatbot refused to answer rather than hallucinate. Inference questions scored 4/5, demonstrating the system's ability to reason across documents. The weakest results came from factual retrieval: Q1 (degree information, 2/5) and Q2 (programming languages, 3/5) showed that details spread across multiple document sections or embedded in headers are sometimes missed at k=3. Faithfulness was strong overall — zero hallucinations recorded across all 10 questions.

---

## Prompt Engineering Insights

Three prompt iterations were tested against the same question: *"What experience does this person have with data analytics?"*

- **v1 (Baseline):** Identified the chatbot and its purpose. Output was broad and accurate but drew on general knowledge alongside the documents.
- **v2 (Grounding added):** Added an explicit constraint to answer only from provided context, with a fallback phrase for out-of-scope questions. Output became more detailed and document-specific.
- **v3 (Tone + format added):** Added recruiter-facing tone and instruction to use complete sentences. Output became concise, professional, and well-structured.

The main lesson: grounding the model to the retrieved context is the single most impactful change, and more detailed prompts consistently produced better outputs.

---

## Failure Analysis

Two main failure patterns were identified:

**Retrieval gaps on distributed facts:** Degree information (Q1) was embedded in resume header sections that got merged with other content during chunking, causing the retrieval step to miss it. The chatbot correctly said "I don't have that information" rather than guessing, but this left a recruiter without a basic fact.

**Incomplete skill coverage:** Programming language coverage (Q2) was incomplete because skills are spread across multiple document sections. With k=3, not all relevant chunks were retrieved. Increasing k to 5 would likely surface the full skills list.

Both issues point to the same fix: increasing k from 3 to 5 and potentially adding a dedicated structured skills/education summary document to the data folder.

---

## Conclusion

This project demonstrated that a free-tier RAG pipeline can produce a functional, recruiter-facing career chatbot with strong accuracy and zero hallucinations. Beyond the technical exercise, it was a useful way to better understand where I stand in the market — seeing how an AI characterizes my background based solely on my documents surfaced gaps (like incomplete skills coverage) that I can address in future resume iterations.
