import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = "http://localhost:8000"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Enterprise Q&A Assistant",
    page_icon="🏢",
    layout="wide"
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Header
# ============================================================

st.title("🏢 Enterprise Q&A Assistant")

st.caption(
    "Ask questions from your uploaded enterprise documents "
    "and get answers with source citations."
)


# ============================================================
# Sidebar - Document Upload
# ============================================================

with st.sidebar:

    st.header("📄 Documents")

    st.write(
        "Upload enterprise PDF documents to make them "
        "available for question answering."
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        st.caption(
            f"Selected: **{uploaded_file.name}**"
        )

        if st.button(
            "Upload & Index",
            use_container_width=True
        ):

            with st.spinner(
                "Processing document..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=300
                    )

                    if response.status_code == 200:

                        result = response.json()

                        if result.get("success"):

                            st.success(
                                "Document indexed successfully."
                            )

                            st.write(
                                f"**Document:** "
                                f"{result.get('document_name')}"
                            )

                            st.write(
                                f"**Pages:** "
                                f"{result.get('pages')}"
                            )

                            st.write(
                                f"**Chunks:** "
                                f"{result.get('chunks')}"
                            )

                        else:

                            st.warning(
                                result.get(
                                    "message",
                                    "Document already exists."
                                )
                            )

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "FastAPI server is not running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Document processing timed out."
                    )

                except Exception as exc:

                    st.error(
                        f"Unexpected error: {str(exc)}"
                    )

    st.divider()

    # Clear conversation
    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("Backend")
    st.caption("FastAPI + PostgreSQL + pgvector")

    st.caption("AI")
    st.caption("Embeddings + Gemini")


# ============================================================
# Main Question Area
# ============================================================

st.header("💬 Ask Your Documents")


# ============================================================
# Display Previous Conversation
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        # Display sources for assistant messages
        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown("**📚 Sources**")

            for source in message["sources"]:

                document = source["document"]
                page = source["page"]

                with st.expander(
                    f"📄 {document} — Page {page}"
                ):

                    st.write(
                        f"Source document: **{document}**"
                    )

                    st.write(
                        f"Page: **{page}**"
                    )


# ============================================================
# Question Input
# ============================================================

question = st.chat_input(
    "Ask a question about your enterprise documents..."
)


if question:

    # --------------------------------------------------------
    # Display user question
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Call FastAPI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/query",
                    params={
                        "question": question
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    answer = result.get(
                        "answer",
                        "No answer was generated."
                    )

                    sources = result.get(
                        "sources",
                        []
                    )

                    # ----------------------------------------
                    # Display answer
                    # ----------------------------------------

                    st.markdown(answer)

                    # ----------------------------------------
                    # Display sources
                    # ----------------------------------------

                    if sources:

                        st.markdown(
                            "### 📚 Sources"
                        )

                        for source in sources:

                            document = source["document"]
                            page = source["page"]

                            with st.expander(
                                f"📄 {document} — Page {page}"
                            ):

                                st.write(
                                    f"Source document: "
                                    f"**{document}**"
                                )

                                st.write(
                                    f"Page: **{page}**"
                                )

                    else:

                        st.info(
                            "No source citations were returned."
                        )


                    # ----------------------------------------
                    # Save assistant response
                    # ----------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )


                else:

                    error_message = (
                        f"Query failed: {response.text}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                            "sources": []
                        }
                    )


            except requests.exceptions.ConnectionError:

                error_message = (
                    "❌ Could not connect to the FastAPI server. "
                    "Please make sure the backend is running."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )


            except requests.exceptions.Timeout:

                error_message = (
                    "⏳ The request took too long. "
                    "Please try again."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )


            except Exception as exc:

                error_message = (
                    f"Unexpected error: {str(exc)}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )
