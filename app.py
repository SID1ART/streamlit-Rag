
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_community.vectorstores import InMemoryVectorStore


# Streamlit page
st.title("RAG with Google Gemini API")
st.subheader("Ask questions about webpages")


# Initialize session state
if "web_loaded" not in st.session_state:
    st.session_state.web_loaded = False

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# Load URLs and create vector database
def process_urls(urls):
    all_docs = []

    for url in urls:
        url = url.strip()

        if not url:
            continue

        loader = WebBaseLoader(web_path=[url])
        docs = loader.load()
        all_docs.extend(docs)

    if not all_docs:
        st.error("No documents were loaded.")
        return

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_docs)

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    # Create vector database
    vector_db = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    st.session_state.vector_db = vector_db
    st.session_state.web_loaded = True


# URL input section
if not st.session_state.web_loaded:
    urls_input = st.text_area(
        "Enter webpage URLs, one URL per line"
    )

    if st.button("Process URLs"):
        urls = [
            url.strip()
            for url in urls_input.splitlines()
            if url.strip()
        ]

        if urls:
            try:
                with st.spinner("Loading webpages and creating embeddings..."):
                    process_urls(urls)

                if st.session_state.web_loaded:
                    st.success("URLs processed successfully!")
                    st.rerun()

            except Exception as e:
                st.error(f"Error processing URLs: {e}")
        else:
            st.warning("Please enter at least one URL.")


# Chat section
if (
    st.session_state.web_loaded
    and st.session_state.vector_db is not None
):
    st.success("Webpages are ready. Ask your questions!")

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    query = st.chat_input("Ask a question about the webpages")

    if query:
        # Display and save user question
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        try:
            with st.spinner("Finding relevant information..."):

                # Retrieve relevant chunks
                records = st.session_state.vector_db.similarity_search(
                    query=query,
                    k=6
                )

                # Combine retrieved text
                context = "\n\n".join(
                    record.page_content for record in records
                )

                # Initialize Gemini
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    temperature=0.2,
                    max_output_tokens=1024
                )

                # Generate answer
                response = llm.invoke(
                    f"""Answer the question using the provided context.
If the context does not contain the answer, say you do not
have enough information to answer.

Context:
{context}

Question:
{query}

Answer:"""
                )

                answer = response.content

            # Display and save assistant response
            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Error generating answer: {e}")
