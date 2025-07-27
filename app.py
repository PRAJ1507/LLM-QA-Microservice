import streamlit as st
import httpx
import time
import io

from PyPDF2 import PdfReader

API_URL = "http://localhost:8000"  # Adjust if hosted elsewhere

st.set_page_config(page_title="LLM Q&A over Documents", layout="centered")
st.title("📄 Upload Document and Ask Questions")

# Upload Document
st.header("1. Upload a Document")
uploaded_file = st.file_uploader("Choose a .txt, .md, or .pdf file", type=["txt", "md", "pdf"])

if uploaded_file:
    # Infer title from filename
    title = uploaded_file.name.rsplit(".", 1)[0]

    # Extract content
    if uploaded_file.type in ["text/plain", "text/markdown"]:
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        content = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
    else:
        st.warning("Unsupported file type.")
        st.stop()

    # Show extracted info
    st.subheader("Extracted Title")
    st.text_input("Title", value=title, disabled=True)

    st.subheader("Preview Content")
    st.text_area("Document Content", value=content[:1000], height=200, disabled=True)

    if st.button("Upload to Backend"):
        with st.spinner("Uploading and indexing..."):
            response = httpx.post(f"{API_URL}/documents/", json={"title": title, "content": content})
            if response.status_code == 200:
                st.success(f"Document '{title}' uploaded!")
            else:
                st.error(f"Upload failed: {response.text}")

# List documents
# Step 2: Select Document
st.header("2. Select Document to Ask a Question")
doc_response = httpx.get(f"{API_URL}/documents/")
documents = doc_response.json() if doc_response.status_code == 200 else []

if documents:
    doc_options = {f"{doc['id']}: {doc['title']}": doc["id"] for doc in documents}
    selected_label = st.selectbox("Choose a document", list(doc_options.keys()))
    selected_doc_id = doc_options[selected_label]

    # Show question history
    st.subheader("Previous Questions for This Document")
    q_response = httpx.get(f"{API_URL}/documents/{selected_doc_id}/questions")
    if q_response.status_code == 200:
        questions = q_response.json()
        if questions:
            for q in reversed(questions):  # latest first
                st.markdown(f"**Q:** {q['question']}")
                if q["status"] == "answered":
                    st.markdown(f"**A:** {q['answer']}")
                else:
                    st.markdown("⏳ *Answer pending...*")
                st.markdown("---")
        else:
            st.info("No questions asked yet.")
    else:
        st.error("Failed to fetch question history.")

    # Step 3: Ask Question
    st.header("3. Ask a Question")
    question = st.text_input("Enter your question")

    if st.button("Ask"):
        with st.spinner("Submitting question..."):
            res = httpx.post(
                f"{API_URL}/documents/{selected_doc_id}/question",
                json={"question": question}
            )
            if res.status_code == 200:
                q = res.json()
                question_id = q["id"]
                st.info("Waiting for LLM to respond...")

                # Polling loop
                for _ in range(20):
                    time.sleep(1)
                    q_check = httpx.get(f"{API_URL}/questions/{question_id}")
                    if q_check.status_code == 200:
                        status = q_check.json()["status"]
                        if status == "answered":
                            st.success("✅ Answer received:")
                            st.write(q_check.json()["answer"])
                            break
                else:
                    st.warning("LLM is still processing. Try again shortly.")
            else:
                st.error("Error submitting question.")
else:
    st.info("No documents uploaded yet.")
