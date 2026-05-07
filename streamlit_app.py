"""
Assignment 5 -- Option A: "Ask My Resume" RAG Chatbot
BSAN 6200 | Spring 2026

Run with: python -m streamlit run streamlit_app.py
"""

import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import os
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ask My Resume", page_icon="📄")

# ── Config ──
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
EMBED_MODEL = "all-MiniLM-L6-v2"


# ══════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════

def load_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(filepath):
    from pypdf import PdfReader
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_all_documents(data_dir="data"):
    docs = []
    if not os.path.exists(data_dir):
        return docs
    for filename in sorted(os.listdir(data_dir)):
        filepath = os.path.join(data_dir, filename)
        if filename.endswith(".txt"):
            text = load_text_file(filepath)
        elif filename.endswith(".pdf"):
            text = load_pdf_file(filepath)
        else:
            continue
        if text.strip():
            docs.append({"text": text, "source": filename})
    return docs


def ask_llm(hf_client, prompt):
    response = hf_client.chat_completion(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.1,
    )
    answer = response.choices[0].message.content.strip()
    for cutoff in ["Context:", "Question:", "\n\n\n"]:
        if cutoff in answer:
            answer = answer[:answer.index(cutoff)].strip()
    return answer


# ══════════════════════════════════════════
# Chunking strategy (paragraph-aware)
# ══════════════════════════════════════════

def chunk_documents(documents, max_chunk=600, overlap=80):
    """Paragraph-aware chunking: split on blank lines, cap long paragraphs."""
    chunks = []
    for doc in documents:
        paragraphs = re.split(r'\n\s*\n', doc['text'])
        current = ''
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current) + len(para) + 1 <= max_chunk:
                current = (current + '\n' + para).strip()
            else:
                if current:
                    chunks.append({'text': current, 'source': doc['source']})
                current = (current[-overlap:] + '\n' + para).strip() if current else para
        if current:
            chunks.append({'text': current, 'source': doc['source']})
    return chunks


# ══════════════════════════════════════════
# System prompt (v3 — final)
# ══════════════════════════════════════════

SYSTEM_PROMPT = """You are a professional career chatbot representing Sadaf Sarbazi, designed for recruiters and hiring managers. Answer questions about her experience, skills, education, and projects using only the provided context — do not draw on outside knowledge. If the answer is not in the documents, say: 'I don't have that information in my documents.' Keep responses concise, professional, and in complete sentences."""


# ══════════════════════════════════════════
# Load resources (cached)
# ══════════════════════════════════════════

@st.cache_resource
def load_index():
    """Embed all chunks and return (chunks, embeddings matrix, embed_model, documents)."""
    documents = load_all_documents("data")
    if not documents:
        return None, None, None, []

    chunks = chunk_documents(documents)
    model = SentenceTransformer(EMBED_MODEL)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return chunks, embeddings, model, documents


@st.cache_resource
def load_llm():
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        return None
    return InferenceClient(token=token)


# ══════════════════════════════════════════
# RAG logic
# ══════════════════════════════════════════

def search(chunks, embeddings, model, query, k=3):
    """Cosine similarity search over normalized embeddings."""
    query_emb = model.encode([query], normalize_embeddings=True)
    scores = (query_emb @ embeddings.T).flatten()
    top_idx = np.argsort(scores)[::-1][:k]
    return [chunks[i]["text"] for i in top_idx], [chunks[i]["source"] for i in top_idx]


def ask_rag(chunks, embeddings, embed_model, hf_client, question, k=3):
    """Full RAG pipeline: retrieve -> build prompt -> generate."""
    docs, sources = search(chunks, embeddings, embed_model, question, k=k)
    context = "\n\n".join(docs)

    full_prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question: {question}

Answer:"""

    answer = ask_llm(hf_client, full_prompt)
    return answer, sources, docs


# ══════════════════════════════════════════
# UI
# ══════════════════════════════════════════

hf_client = load_llm()

st.title("📄 Ask My Resume")
st.caption("Ask me anything about my skills, experience, and projects.")

# ── Error checks ──
if not hf_client:
    st.error("HF_TOKEN not found. Add it to your .env file.")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    st.header("About")
    st.write("This chatbot answers questions about my professional background using RAG.")

    uploaded_files = st.file_uploader(
        "Upload career documents (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload your resume, CV, SOQ, or any other career documents.",
    )
    st.divider()
    st.write(f"**Model:** {MODEL_ID}")
    st.divider()
    st.caption("BSAN 6200 | Assignment 5 | Option A")

# ── Load documents ──
# Prefer uploaded files; fall back to local data/ folder
if uploaded_files:
    raw_docs = []
    for uf in uploaded_files:
        if uf.name.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(uf)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = uf.read().decode("utf-8")
        if text.strip():
            raw_docs.append({"text": text, "source": uf.name})

    all_chunks = chunk_documents(raw_docs)

    @st.cache_resource
    def build_index_from_uploaded(file_key):
        return None  # placeholder; real build below

    model = SentenceTransformer(EMBED_MODEL)
    texts = [c["text"] for c in all_chunks]
    embs = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    chunks, embeddings, embed_model = all_chunks, embs, model

    with st.sidebar:
        st.write(f"**Documents loaded:** {len(raw_docs)}")
        for d in raw_docs:
            st.write(f"- {d['source']}")
        st.write(f"**Chunks:** {len(chunks)}")
else:
    chunks, embeddings, embed_model, raw_docs = load_index()
    if chunks is None:
        st.info("Upload your career documents in the sidebar to get started.")
        st.stop()
    with st.sidebar:
        st.write(f"**Documents loaded:** {len(raw_docs)}")
        for d in raw_docs:
            st.write(f"- {d['source']}")
        st.write(f"**Chunks:** {len(chunks)}")

# ── Sample questions ──
st.write("**Try a sample question:**")
samples = [
    "What technical skills does this person have?",
    "Describe a project this person has worked on.",
    "What type of role is this person best suited for?",
]
cols = st.columns(len(samples))
for i, q in enumerate(samples):
    if cols[i].button(q, key=f"sample_{i}"):
        st.session_state["pending_question"] = q

# ── Chat interface ──
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            with st.expander("📎 Retrieved chunks"):
                st.markdown(msg["sources"])

user_input = st.chat_input("Ask me about my background...")

if "pending_question" in st.session_state:
    user_input = st.session_state.pop("pending_question")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            answer, sources, docs = ask_rag(chunks, embeddings, embed_model, hf_client, user_input)

            st.markdown(answer)

            source_text = ""
            for i, (doc, src) in enumerate(zip(docs, sources)):
                source_text += f"**Chunk {i+1}** ({src}):\n> {doc[:200]}...\n\n"

            with st.expander("📎 Retrieved chunks"):
                st.markdown(source_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": source_text,
            })

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
