"""
Assignment 5 -- Option A: "Ask My Resume" RAG Chatbot
BSAN 6200 | Spring 2026

Run with: python -m streamlit run streamlit_app.py

YOUR TASKS (search for TODO):
1. Load your documents from the data/ folder
2. Implement your chunking strategy
3. Write your system prompt (3+ iterations in notebook first)
4. Add at least 3 sample questions relevant to YOUR documents
"""

import streamlit as st
import chromadb
from huggingface_hub import InferenceClient
import os
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ask My Resume", page_icon="📄")

# ── Config ──
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"


# ══════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════

def load_text_file(filepath):
    """Load a .txt file and return its content."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(filepath):
    """Load a .pdf file and return its text content."""
    from pypdf import PdfReader
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_all_documents(data_dir="data"):
    """Load all .txt and .pdf files from the data directory."""
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
    """Send a prompt to the LLM and return the response."""
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
# TODO 1: Chunking strategy
# Implement your chosen chunking function.
# You should have compared 2+ strategies
# in your notebook and justified your choice.
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
# TODO 2: System prompt
# Design your prompt. Must have 3+ iterations
# documented in your notebook.
# ══════════════════════════════════════════

SYSTEM_PROMPT = """TODO: Write your system prompt here.

Consider:
- Grounding (answer only from context)
- Tone (professional, career-appropriate)
- Edge cases (what to say when answer is not in documents)
- Format (how long, how detailed)

Delete this placeholder and write your own."""


# ══════════════════════════════════════════
# Load resources (cached)
# ══════════════════════════════════════════

@st.cache_resource
def load_vectorstore():
    documents = load_all_documents("data")
    if not documents:
        return None, []

    chunks = chunk_documents(documents)
    client = chromadb.Client()
    collection = client.create_collection("resume_rag")
    collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    return collection, documents


@st.cache_resource
def load_llm():
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        return None
    return InferenceClient(token=token)


# ══════════════════════════════════════════
# RAG logic
# ══════════════════════════════════════════

def search(collection, query, k=3):
    """Retrieve top-k chunks from the vector store."""
    results = collection.query(query_texts=[query], n_results=k)
    return results["documents"][0], [m["source"] for m in results["metadatas"][0]]


def ask_rag(collection, hf_client, question, k=3):
    """Full RAG pipeline: retrieve -> build prompt -> generate."""
    docs, sources = search(collection, question, k=k)
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

collection, raw_docs = load_vectorstore()
hf_client = load_llm()

st.title("📄 Ask My Resume")
st.caption("Ask me anything about my skills, experience, and projects.")

# ── Error checks ──
if not hf_client:
    st.error("HF_TOKEN not found. Add it to your .env file.")
    st.stop()

if collection is None:
    st.error("No documents found in data/ folder. Add your resume and other files there.")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    st.header("About")
    st.write("This chatbot answers questions about my professional background using RAG.")
    st.write(f"**Documents loaded:** {len(raw_docs)}")
    for d in raw_docs:
        st.write(f"- {d['source']}")
    st.divider()
    st.write(f"**Chunks in vector store:** {collection.count()}")
    st.write(f"**Model:** {MODEL_ID}")
    st.divider()
    st.caption("BSAN 6200 | Assignment 5 | Option A")

# ── TODO 3: Sample questions ──
# Replace these with questions relevant to YOUR documents
st.write("**Try a sample question:**")
samples = [
    "TODO: Add sample question 1",
    "TODO: Add sample question 2",
    "TODO: Add sample question 3",
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
            answer, sources, docs = ask_rag(collection, hf_client, user_input)

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
