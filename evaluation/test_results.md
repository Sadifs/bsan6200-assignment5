# Evaluation Results

**Project:** Ask My Resume RAG Chatbot (Option A)
**Author:** Sadaf Sarbazi

---

## Test Query Set

| # | Category | Question | Sources Retrieved | Retrieval Quality | Faithfulness | Score (1–5) |
|---|----------|----------|-------------------|-------------------|--------------|-------------|
| 1 | Factual | What degree(s) does this person hold? | Resume.pdf, CV.pdf, CV.pdf | Partial | Faithful | 2 |
| 2 | Factual | What programming languages does this person know? | Resume.pdf, github_projects.txt, Resume.pdf | Partial | Faithful | 3 |
| 3 | Factual | Describe the Paris Agreement climate classifier project. | github_projects.txt x3 | Yes | Faithful | 5 |
| 4 | Inference | How does this person's ML experience apply to business problems? | CV.pdf, CV.pdf, Resume.pdf | Yes | Partial | 4 |
| 5 | Inference | What type of role would suit this person best and why? | Resume.pdf, CV.pdf, SOQ.pdf | Yes | Partial | 4 |
| 6 | Out-of-scope | What is this person's salary expectation? | SOQ.pdf, CV.pdf, Resume.pdf | No | Faithful | 5 |
| 7 | Out-of-scope | Does this person have 10 years of professional experience? | Resume.pdf x3 | Partial | Faithful | 5 |
| 8 | Out-of-scope | What is this person's home address? | SOQ.pdf, CV.pdf, github_projects.txt | No | Faithful | 5 |
| 9 | Specificity | What did this person write in their statement of qualifications? | SOQ.pdf, Resume.pdf, CV.pdf | Yes | Partial | 4 |
| 10 | Specificity | What model did the BSAN6070 final project use and why? | github_projects.txt x3 | Yes | Faithful | 5 |

**Average quality score: 4.2 / 5**

---

## Chunking Strategy Comparison

| Strategy | Chunk Size | Overlap | Total Chunks | Avg Length |
|----------|-----------|---------|-------------|------------|
| Fixed-size | 400 chars | 50 chars | 64 | 377 chars |
| Paragraph-aware | 600 chars max | 80 chars | 26 | 866 chars |

**Chosen:** Paragraph-aware — preserves semantic units (resume sections, project descriptions) rather than splitting mid-sentence.

---

## Prompt Iteration Results

### Iteration 1 — Baseline
**Prompt:** *"You are a chatbot representing Sadaf Sarbazi's professional background. Your job is to answer questions about her experience, skills, education, and projects based on the documents provided."*
**Sample Output (Q: data analytics experience):** Broad, accurate but pulled from general knowledge alongside docs. No constraint on scope.
**Issue:** No grounding — model added information beyond the retrieved context.

### Iteration 2 — Add Grounding
**Prompt:** *"...Only use information from the provided context to answer — do not use outside knowledge. If the context does not contain the answer, say: 'I don't have that information in my documents.'"*
**Sample Output:** More detailed and specific — stayed closer to document content. Better out-of-scope handling.
**Improvement:** Grounding constraint reduced hallucination risk and added explicit out-of-scope fallback.

### Iteration 3 — Add Tone and Format (Final)
**Prompt:** *"You are a professional career chatbot representing Sadaf Sarbazi, designed for recruiters and hiring managers...Keep responses concise, professional, and in complete sentences."*
**Sample Output:** Concise, professional, well-structured. Appropriate for recruiter audience.
**Improvement:** Tone and format instructions produced cleaner, more recruiter-appropriate responses.

---

## Failure Analysis

### Failure Pattern 1: Retrieval Miss on Degree Information
**Query:** What degree(s) does this person hold?
**Retrieved chunks:** Resume.pdf, CV.pdf — but degree section not captured in top chunks
**LLM output:** "I don't have that information in my documents."
**Root cause:** Degree information is embedded in header/summary sections that get merged with other content in paragraph-aware chunking, reducing retrieval precision for that specific fact.
**Fix implemented:** Added `data/about.txt` — a structured career summary with a dedicated education section — which directly addresses this retrieval gap for the deployed app.

### Failure Pattern 2: Incomplete Language Coverage
**Query:** What programming languages does this person know?
**Retrieved chunks:** Resume.pdf, github_projects.txt
**LLM output:** Only mentioned Python and Jupyter — missed SQL, R, Tableau listed in CV
**Root cause:** CV chunks containing the full skills list ranked lower than Resume chunks for this query.
**Fix implemented:** `data/about.txt` consolidates all skills into a single section, reducing fragmentation. Increasing k from 3 to 5 would further improve coverage across source documents.

---

## Top-k Tuning

| k value | Notes |
|---------|-------|
| k=3 | Used for evaluation — misses some skills listed across multiple chunks |
| k=5 | Would likely improve Q2 (language coverage) and Q1 (degree retrieval) |
