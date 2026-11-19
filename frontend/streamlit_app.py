import hashlib
import html
import time
import uuid

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
UPLOAD_URL = f"{API_URL}/documents/upload"
ASK_URL = f"{API_URL}/documents/ask"
HEALTH_URL = f"{API_URL}/health"  # existing endpoint in your main.py
HEALTH_TTL = 10  # seconds between automatic connection checks

EXAMPLES = [
    ("✨", "Quick summary", "Get the gist in seconds.", "Give me a quick summary of this document."),
    ("🎯", "Key points", "See what matters most.", "What are the most important points?"),
    ("🔎", "Find details", "Pull out specific facts.", "Find specific information for me."),
    ("💬", "Plain English", "Simple words, no jargon.", "Explain this document in simple words."),
]
STEPS = [
    ("⬆️", "Upload", "Add one or more PDFs"),
    ("💬", "Ask", "Type in plain language"),
    ("📌", "Get cited answers", "Every answer shows file and page"),
]

st.set_page_config(page_title="Cognivault", page_icon="📚", layout="wide")

# ---------------------------------------------------------------- styling
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');
:root{--bg:#101014;--s1:#191922;--s2:#22222D;--violet:#9B7BFF;--lime:#C4F36B;
--lav:#C8B9FF;--text:#F5F3FA;--muted:#9895A6;--line:rgba(200,185,255,.14);--bad:#FF7A8A;}
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif;color:var(--text);}
.stApp{background:var(--bg);}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
.block-container{max-width:860px;padding-top:3.5rem;padding-bottom:8rem;}
h1,h2,h3,.hero h1{font-family:'Space Grotesk',sans-serif;letter-spacing:-.02em;}
section[data-testid="stSidebar"]{background:var(--s1);border-right:1px solid var(--line);}
.logo{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.5rem;}
.logo span{color:var(--lime);}
.side-label{color:var(--muted);font-size:.8rem;margin:1.2rem 0 .4rem;}
.status{display:inline-flex;align-items:center;gap:8px;background:var(--s2);border:1px solid var(--line);
border-radius:999px;padding:4px 12px;font-size:.8rem;margin:.6rem 0 .2rem;}
.status i{width:8px;height:8px;border-radius:50%;display:inline-block;}
.status.on i{background:var(--lime);box-shadow:0 0 8px var(--lime);}
.status.off i{background:var(--bad);}
.status.on{border-color:rgba(196,243,107,.45);color:var(--lime);}
.tagline{color:var(--muted);font-size:.74rem;line-height:1.4;text-wrap:balance;margin:.2rem 0 .8rem;}
[class*="st-key-chat_on_"] button{border-color:var(--lime)!important;color:var(--lime)!important;}
.doc-pill{display:flex;justify-content:space-between;align-items:center;gap:8px;
background:var(--s2);border:1px solid var(--line);border-radius:12px;padding:8px 12px;
margin-bottom:6px;font-size:.85rem;}
.doc-pill b{font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.dot{color:var(--lime);font-size:.75rem;white-space:nowrap;}
.hero{position:relative;isolation:isolate;padding:1rem 0 1.2rem;}
.hero::before{content:'';position:absolute;inset:-70px -50px auto -50px;height:280px;z-index:-1;pointer-events:none;background:radial-gradient(ellipse at 30% 45%,rgba(155,123,255,.30),transparent 65%);filter:blur(12px);}
.hero h1{font-size:clamp(1.9rem,4.6vw,2.6rem);line-height:1.1;margin:0 0 .7rem;text-wrap:balance;
background:linear-gradient(120deg,var(--text) 40%,var(--violet));
-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{color:var(--muted);font-size:clamp(1rem,2.5vw,1.1rem);margin:0;}
.card{background:var(--s1);border:1px solid var(--line);border-radius:18px;padding:1.2rem 1.4rem;
box-shadow:0 8px 30px rgba(0,0,0,.25);}
.card h3{margin:0 0 .2rem;font-size:1.1rem;overflow-wrap:anywhere;}
.empty{text-align:center;border-style:dashed;margin:1rem 0;}
.empty .big{font-size:2rem;}
.muted{color:var(--muted);font-size:.9rem;}
.badge{display:inline-block;background:rgba(196,243,107,.12);color:var(--lime);
border-radius:999px;padding:2px 10px;font-size:.78rem;margin-top:.4rem;}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-top:.8rem;}
.stat{background:var(--s2);border-radius:12px;padding:.7rem .9rem;}
.stat b{display:block;font-family:'Space Grotesk',sans-serif;font-size:1.3rem;color:var(--lav);}
.stat span{color:var(--muted);font-size:.78rem;}
[data-testid="stFileUploader"] section{background:var(--s2);border:1.5px dashed var(--violet);
border-radius:16px;transition:border-color .2s,background .2s;}
[data-testid="stFileUploader"] section:hover{border-color:var(--lime);background:#272734;}
.stButton>button{background:var(--s2);color:var(--text);border:1px solid var(--line);
border-radius:12px;transition:all .15s;}
.stButton>button:hover:not(:disabled){border-color:var(--violet);color:var(--lav);}
.stButton>button[kind="primary"]{background:var(--violet);color:#101014;border:none;font-weight:600;}
.stButton>button[kind="primary"]:hover:not(:disabled){background:var(--lav);color:#101014;}
.stButton>button:disabled{opacity:.4;}
[data-testid="stChatMessage"]{background:var(--s1);border:1px solid var(--line);
border-radius:18px;padding:1rem 1.2rem;overflow-wrap:anywhere;}
[data-testid="stChatMessage"] pre,[data-testid="stChatMessage"] table{max-width:100%;overflow-x:auto;display:block;}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){
background:var(--s2);border-color:rgba(155,123,255,.35);}
[data-testid="stBottom"],[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"]{background:var(--bg)!important;}
[data-testid="stChatInput"],[data-testid="stChatInput"]>div{background:var(--s1)!important;border-radius:16px;}
[data-testid="stChatInput"]{border:1px solid var(--line);}
[data-testid="stChatInput"] textarea{color:var(--text)!important;}
[data-testid="stChatInput"]:focus-within{border-color:var(--lime);}
.src-title{color:var(--muted);font-size:.8rem;margin:.9rem 0 .4rem;}
.chip{display:inline-block;background:rgba(155,123,255,.12);border:1px solid rgba(155,123,255,.4);
color:var(--lav);border-radius:999px;padding:4px 12px;font-size:.82rem;margin:0 6px 6px 0;
max-width:100%;overflow-wrap:anywhere;}
.chip i{font-style:normal;color:var(--lime);margin-left:6px;}
.st-key-upload_card{background:var(--s1);border:1px solid var(--line);border-radius:20px;
padding:1.2rem 1.4rem;box-shadow:0 8px 30px rgba(0,0,0,.25);}
.up-title{margin:0 0 .2rem;font-size:1.15rem;}
.docstat{display:inline-flex;align-items:center;gap:8px;color:var(--muted);font-size:.82rem;margin-top:.7rem;}
.docstat i{width:8px;height:8px;border-radius:50%;background:var(--muted);display:inline-block;flex:none;}
.docstat.on{color:var(--lime);}.docstat.on i{background:var(--lime);}
.steps{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:center;gap:12px;margin:.2rem 0 1.4rem;}
.step{background:var(--s1);border:1px solid var(--line);border-radius:14px;padding:.7rem .9rem;}
.step b{display:block;font-family:'Space Grotesk',sans-serif;font-size:.95rem;}
.step span{color:var(--muted);font-size:.8rem;}
.arrow{color:var(--lime);}
.st-key-examples .stButton>button{min-height:92px;text-align:left;justify-content:flex-start;
padding:.9rem 1rem;white-space:normal;}
.st-key-examples .stButton>button p{text-align:left;margin:0;font-size:.84rem;color:var(--muted);line-height:1.4;}
.st-key-examples .stButton>button p strong{display:block;color:var(--text);font-size:.98rem;
font-family:'Space Grotesk',sans-serif;margin-bottom:.2rem;}
.st-key-examples .stButton>button:hover:not(:disabled){border-color:var(--lime);transform:translateY(-2px);}
@media (max-width:640px){.steps{grid-template-columns:1fr;}.arrow{display:none;}
.st-key-upload_card{padding:1rem;border-radius:14px;}}
:focus-visible{outline:2px solid var(--lime)!important;outline-offset:2px;}
@media (max-width:640px){
 .block-container{padding:1rem .8rem 6rem;}
 .card{padding:1rem;border-radius:14px;}
 .stats{grid-template-columns:repeat(2,1fr);}
 [data-testid="stChatMessage"]{padding:.7rem .8rem;border-radius:14px;}
 .stButton>button{min-height:46px;}
 .chip{font-size:.78rem;}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;}}
</style>
"""


# ---------------------------------------------------------- session state
def new_chat_id():
    return uuid.uuid4().hex[:8]


def init_state():
    ss = st.session_state
    ss.setdefault("chats", {})
    ss.setdefault("docs", [])
    ss.setdefault("hashes", {})  # sha256 -> filename for this session
    ss.setdefault("pending", None)
    ss.setdefault("last_upload", None)
    ss.setdefault("backend", None)
    if ss.get("current") not in ss.chats:
        start_new_chat()


def prune_empty(keep=None):
    chats = st.session_state.chats
    for cid in [c for c, v in chats.items() if not v["messages"] and c != keep]:
        del chats[cid]


def start_new_chat():
    """Always creates a brand-new conversation and makes it active."""
    prune_empty()
    cid = new_chat_id()
    st.session_state.chats[cid] = {"title": "New chat", "messages": []}
    st.session_state.current = cid
    st.session_state.pending = None


def switch_chat(cid):
    if cid in st.session_state.chats:
        prune_empty(keep=cid)
        st.session_state.current = cid
        st.session_state.pending = None


def current_chat():
    return st.session_state.chats[st.session_state.current]


def clear_chat():
    chat = current_chat()
    chat["messages"] = []
    chat["title"] = "New chat"
    st.session_state.pending = None


def add_user_message(text):
    chat = current_chat()
    if not chat["messages"]:
        chat["title"] = text[:28] + ("…" if len(text) > 28 else "")
    chat["messages"].append({"role": "user", "content": text})


# ------------------------------------------------------------ API layer
def set_backend(ok):
    st.session_state.backend = {"ok": ok, "at": time.time()}


def check_backend(force=False):
    state = st.session_state.backend
    if not force and state and time.time() - state["at"] < HEALTH_TTL:
        return state["ok"]
    try:
        r = requests.get(HEALTH_URL, timeout=2)
        body = r.json() if r.status_code == 200 else {}
        ok = isinstance(body, dict) and body.get("status") == "healthy"
    except (requests.exceptions.RequestException, ValueError):
        ok = False
    set_backend(ok)
    return ok


def format_detail(detail):
    """FastAPI 'detail' can be a string or a list of validation errors."""
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts = [str(d.get("msg", d)) if isinstance(d, dict) else str(d) for d in detail]
        return "; ".join(parts)
    return str(detail)


def api_call(method, url, **kwargs):
    """Returns (json_dict, None) on success or (None, readable_error)."""
    try:
        response = requests.request(method, url, **kwargs)
    except requests.exceptions.ConnectionError:
        set_backend(False)
        return None, ("Could not connect to the Cognivault API. Start the backend with "
                      "`uvicorn app.main:app --reload` and check that it runs on port 8000.")
    except requests.exceptions.Timeout:
        return None, "The request timed out. The server may be busy; please try again."
    except requests.exceptions.RequestException as exc:
        return None, f"Network error: {exc}"

    set_backend(True)
    try:
        body = response.json()
    except ValueError:
        body = None

    if response.status_code != 200:
        if isinstance(body, dict) and body.get("detail"):
            return None, format_detail(body["detail"])
        snippet = (response.text or "").strip()[:200] or "no details"
        return None, f"The API returned status {response.status_code} ({snippet})."
    if not isinstance(body, dict):
        return None, "The API sent an unexpected response (expected a JSON object)."
    return body, None


def upload_pdf(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    data, err = api_call("POST", UPLOAD_URL, files=files, timeout=300)
    if err:
        return None, err
    data.setdefault("filename", uploaded_file.name)  # tolerate a missing field
    return data, None


def clean_sources(raw):
    sources = []
    for item in raw if isinstance(raw, list) else []:
        if isinstance(item, dict) and item.get("filename") is not None:
            src = {"filename": str(item["filename"]), "page": item.get("page", "?")}
            if src not in sources:
                sources.append(src)
    return sources


def ask_question(question):
    data, err = api_call("POST", ASK_URL, json={
    "question": question,
    "document_name": st.session_state.get("selected_document")}, timeout=120)
    if err:
        return None, err
    answer = data.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        return None, "The API responded, but did not include an answer. Please try again."
    return {"answer": answer, "sources": clean_sources(data.get("sources"))}, None


# -------------------------------------------------------------- rendering
def render_sources(sources):
    if not sources:
        return
    chips = "".join(
        f'<span class="chip">📄 {html.escape(str(s.get("filename", "?")))}'
        f'<i>Page {html.escape(str(s.get("page", "?")))}</i></span>'
        for s in sources
    )
    st.markdown(f'<div class="src-title">Sources</div>{chips}', unsafe_allow_html=True)


def render_chat(messages):
    for msg in messages:
        with st.chat_message(msg["role"]):
            if msg.get("error"):
                st.error(msg["content"])
            else:
                st.markdown(msg["content"])
            if msg["role"] == "assistant":
                render_sources(msg.get("sources"))


def render_stats(info):
    items = [("Pages", "total_pages"), ("Characters", "total_characters"),
             ("Chunks", "total_chunks"), ("Vectors", "total_vectors"),
             ("Stored records", "total_stored")]
    cells = "".join(
        f'<div class="stat"><b>{html.escape(str(info.get(k, "-")))}</b><span>{label}</span></div>'
        for label, k in items
    )
    st.markdown(
        f'<div class="card"><h3>📄 {html.escape(str(info.get("filename", "")))}</h3>'
        f'<span class="badge">● Ready to answer questions</span>'
        f'<div class="stats">{cells}</div></div>',
        unsafe_allow_html=True,
    )


def keyed(name):
    """Container with a CSS hook; falls back on older Streamlit versions."""
    try:
        return st.container(key=name)
    except TypeError:
        return st.container()


def render_doc_status():
    n = len(st.session_state.docs)
    if n:
        st.markdown(f'<div class="docstat on"><i></i>{n} document{"s" if n != 1 else ""} ready to question</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="docstat"><i></i>No document uploaded yet. '
                    'PDFs from earlier sessions may still be searchable.</div>', unsafe_allow_html=True)


def render_upload():
    with keyed("upload_card"):
        st.markdown(
            '<h3 class="up-title">⬆️ Upload a document</h3>'
            '<div class="muted">Drag and drop a PDF, then press Upload. '
            '<span class="badge">PDF only</span></div>',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader("PDF file", type=["pdf"], label_visibility="collapsed")

        digest, duplicate = None, False
        if uploaded is not None:
            digest = hashlib.sha256(uploaded.getvalue()).hexdigest()
            duplicate = digest in st.session_state.hashes
            if duplicate:
                st.info(f"“{st.session_state.hashes[digest]}” is already uploaded in this session. "
                        "Choose a different PDF to add more.")
            elif uploaded.name in st.session_state.hashes.values():
                st.warning(f"A different file named “{uploaded.name}” was uploaded earlier. "
                           "Uploading this one may add overlapping content.")

        clicked = st.button("Upload PDF", type="primary", disabled=uploaded is None or duplicate)
        if clicked and uploaded is not None and not duplicate:
            with st.status(f"Processing {uploaded.name}…", expanded=True) as status:
                st.write("Uploading, extracting text and building embeddings. Large PDFs can take a minute.")
                data, err = upload_pdf(uploaded)
                if err:
                    status.update(label="Upload failed", state="error")
                else:
                    status.update(label="Document ready", state="complete", expanded=False)
            if err:
                st.error(err)
            else:
                st.session_state.hashes[digest] = data["filename"]
                st.session_state.last_upload = data
                st.session_state.docs.append(data)
                st.toast("PDF uploaded and processed.", icon="✅")
        render_doc_status()
    if st.session_state.last_upload:
        render_stats(st.session_state.last_upload)


def render_sidebar():
    online = check_backend()
    with st.sidebar:
        st.markdown('<div class="logo">📚 Cogni<span>vault</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Your documents. Your intelligence. Zero digging.</div>', unsafe_allow_html=True)
        if st.button("＋ New chat", type="primary", use_container_width=True):
            start_new_chat()
            st.rerun()

        label, cls = ("API connected", "on") if online else ("API offline", "off")
        st.markdown(f'<div class="status {cls}"><i></i>{label}</div>', unsafe_allow_html=True)
        if not online and st.button("↻ Recheck connection", use_container_width=True):
            check_backend(force=True)
            st.rerun()

        st.markdown('<div class="side-label">Recent chats</div>', unsafe_allow_html=True)
        used = [(cid, c) for cid, c in st.session_state.chats.items() if c["messages"]]
        if not used:
            st.caption("Your conversations will appear here.")
        for cid, chat in reversed(used):
            is_active = cid == st.session_state.current
            active = "▸ " if is_active else ""
            if st.button(f"{active}💬 {chat['title']}", key=f"chat_{'on_' if is_active else ''}{cid}", use_container_width=True):
                switch_chat(cid)
                st.rerun()

        st.markdown('<div class="side-label">Documents (this session)</div>', unsafe_allow_html=True)
        if not st.session_state.docs:
            st.caption("No uploads yet.")
        for d in st.session_state.docs:
            st.markdown(
                f'<div class="doc-pill"><b>📄 {html.escape(str(d["filename"]))}</b>'
                f'<span class="dot">● Ready</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="side-label">Ask questions about</div>', unsafe_allow_html=True)

        document_names = list(dict.fromkeys(
            d["filename"] for d in st.session_state.docs
        ))

        if document_names:
            previous = st.session_state.get("selected_document")

            default_index = (
                document_names.index(previous)
                if previous in document_names
                else len(document_names) - 1
            )

            st.selectbox(
                "Select a document",
                options=document_names,
                index=default_index,
                key="selected_document"
            )
        else:
            st.session_state["selected_document"] = None
            st.caption("Upload a PDF to select it.")

        with st.expander("Settings & about"):
            st.write("Cognivault answers questions using the PDFs stored in your backend and shows the pages it used.")
            st.caption(f"API: {API_URL}")
        st.markdown('<div class="side-label">Powered by Gemini ✦</div>', unsafe_allow_html=True)


def render_welcome():
    st.markdown(
        '<div class="hero"><h1>Your documents have a lot to say.</h1>'
        '<p>Upload your PDFs. Ask anything. Get answers backed by your documents.</p></div>',
        unsafe_allow_html=True,
    )
    parts = [f'<div class="step"><b>{i} {t}</b><span>{d}</span></div>' for i, t, d in STEPS]
    st.markdown('<div class="steps">' + '<span class="arrow">→</span>'.join(parts) + "</div>",
                unsafe_allow_html=True)
    render_upload()
    st.markdown("##### Try asking")
    with keyed("examples"):
        cols = st.columns(2)
        for i, (icon, title, desc, prompt) in enumerate(EXAMPLES):
            if cols[i % 2].button(f"**{icon} {title}** {desc}", key=f"ex_{i}", use_container_width=True):
                st.session_state.pending = prompt
                st.rerun()


def answer_last_question(chat):
    """If the chat ends with an unanswered user message, ask the backend."""
    with st.chat_message("assistant"):
        with st.spinner("Cognivault is reading your documents..."):
            data, err = ask_question(chat["messages"][-1]["content"])
    if err:
        chat["messages"].append({"role": "assistant", "content": err, "error": True})
    else:
        chat["messages"].append({
    "role": "assistant",
    "content": data["answer"],
    "sources": data.get("sources", [])
})
    st.rerun()


# ------------------------------------------------------------------- main
init_state()
st.markdown(CSS, unsafe_allow_html=True)
render_sidebar()

typed = st.chat_input("Ask a question about your documents...")
question = st.session_state.pending or typed
st.session_state.pending = None
if question and question.strip():
    add_user_message(question.strip())
    st.rerun()

chat = current_chat()
messages = chat["messages"]
if messages:
    top = st.columns([5, 1])
    top[0].markdown("### Chat")
    if top[1].button("Clear chat"):
        clear_chat()
        st.rerun()
    with st.expander("Add another PDF"):
        render_upload()
    render_chat(messages)
    if messages[-1]["role"] == "user":
        answer_last_question(chat)
    elif messages[-1].get("error") and st.button("Retry last question"):
        messages.pop()  # drop the error; the user question is answered again
        st.rerun()
else:
    render_welcome()
