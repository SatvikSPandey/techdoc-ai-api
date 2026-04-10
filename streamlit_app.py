import streamlit as st
import httpx

API_URL = "http://13.201.68.108:8000"
API_KEY = "sk-dev-key-123456789"
HEADERS = {"X-API-Key": API_KEY}

st.set_page_config(
    page_title="TechDoc AI",
    page_icon="📄",
    layout="wide",
)

st.title("📄 TechDoc AI")
st.caption("AI-powered technical document analysis — powered by Cohere and FastAPI on AWS")

tab1, tab2, tab3 = st.tabs(["Summarize", "Ask a Question", "API Status"])

# ── Tab 1: Summarize ──────────────────────────────────────────────────────────
with tab1:
    st.header("Document Summarizer")
    st.write("Paste your technical document below and get an AI-generated summary.")

    text = st.text_area("Document text", height=250, placeholder="Paste your document here...")
    max_length = st.slider("Summary length (words)", min_value=100, max_value=500, value=200)
    focus = st.text_input("Focus areas (optional, comma separated)", placeholder="e.g. requirements, risks, timeline")

    if st.button("Summarize", type="primary"):
        if not text.strip():
            st.warning("Please paste a document first.")
        else:
            with st.spinner("Analysing document..."):
                focus_areas = [f.strip() for f in focus.split(",")] if focus.strip() else None
                payload = {"text": text, "max_length": max_length}
                if focus_areas:
                    payload["focus_areas"] = focus_areas
                try:
                    response = httpx.post(
                        f"{API_URL}/api/v1/summarize",
                        json=payload,
                        headers=HEADERS,
                        timeout=60,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Summary generated successfully")
                        st.subheader("Summary")
                        st.write(data["summary"])
                        st.subheader("Key Points")
                        for point in data["key_points"]:
                            st.markdown(f"- {point}")
                        col1, col2 = st.columns(2)
                        col1.metric("Word count", data["word_count"])
                        col2.metric("Processing time", f"{data['processing_time_ms']:.0f} ms")
                        st.caption(f"Model: {data['model_used']}")
                    else:
                        st.error(f"API error: {response.status_code}")
                except Exception as e:
                    st.error(f"Could not reach the API: {e}")

# ── Tab 2: Ask ────────────────────────────────────────────────────────────────
with tab2:
    st.header("Document Q&A")
    st.write("Paste your document and ask any question about it.")

    context = st.text_area("Document text", height=200, placeholder="Paste your document here...", key="ask_context")
    question = st.text_input("Your question", placeholder="e.g. What are the main safety requirements?")

    if st.button("Get Answer", type="primary"):
        if not context.strip() or not question.strip():
            st.warning("Please provide both a document and a question.")
        else:
            with st.spinner("Finding answer..."):
                try:
                    response = httpx.post(
                        f"{API_URL}/api/v1/ask",
                        json={"question": question, "context": context},
                        headers=HEADERS,
                        timeout=60,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Answer found")
                        st.subheader("Answer")
                        st.write(data["answer"])
                        st.metric("Confidence", f"{data['confidence']:.0%}")
                        if data["sources"]:
                            st.subheader("Sources")
                            for source in data["sources"]:
                                st.markdown(f"> {source}")
                        st.caption(f"Model: {data['model_used']}")
                    else:
                        st.error(f"API error: {response.status_code}")
                except Exception as e:
                    st.error(f"Could not reach the API: {e}")

# ── Tab 3: API Status ─────────────────────────────────────────────────────────
with tab3:
    st.header("API Status")
    if st.button("Check Status"):
        try:
            health = httpx.get(f"{API_URL}/api/v1/health", timeout=10).json()
            metrics = httpx.get(f"{API_URL}/api/v1/metrics", timeout=10).json()
            st.success("API is online")
            col1, col2, col3 = st.columns(3)
            col1.metric("Status", health["status"])
            col2.metric("Version", health["version"])
            col3.metric("AI Backend", health["ai_backend"])
            st.subheader("Metrics")
            col4, col5, col6 = st.columns(3)
            col4.metric("Total requests", metrics["total_requests"])
            col5.metric("Successful", metrics["successful_requests"])
            col6.metric("Avg response time", f"{metrics['average_response_time_ms']:.0f} ms")
        except Exception as e:
            st.error(f"API is unreachable: {e}")