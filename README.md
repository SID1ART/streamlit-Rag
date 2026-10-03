# Streamlit RAG with Google Gemini

A Retrieval Augmented Generation (RAG) application built with Streamlit, LangChain, and Google Gemini. The app loads content from webpages, converts the content into embeddings, stores the embeddings in a vector database, and answers user questions based on the retrieved information.

## Features

* Load content from one or more webpage URLs.
* Split webpage content into smaller text chunks.
* Generate embeddings using Google Gemini.
* Store and search document embeddings using an in memory vector store.
* Retrieve relevant content using similarity search.
* Generate context based answers using Gemini 2.5 Flash.
* Maintain chat history during the Streamlit session.

## Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini API
* Google Generative AI Embeddings
* InMemoryVectorStore
* Beautiful Soup
* Python Dotenv

## Project Structure

```text
streamlit-Rag/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

The `.env` file stores your API key locally and should never be committed to GitHub.

## Prerequisites

* Python 3.10 or a compatible version.
* A Google AI Studio API key.
* Git and VS Code.

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SID1ART/streamlit-Rag.git
cd streamlit-Rag
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv env
```

Activate it:

```powershell
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, install the dependencies:

```bash
python -m pip install streamlit python-dotenv langchain-community langchain-text-splitters langchain-google-genai beautifulsoup4
```

### 4. Configure environment variables

Create a `.env` file in the project root and add:

```env
GOOGLE_API_KEY=your_google_api_key_here
USER_AGENT=RAGProject/1.0
```

Replace the placeholder with your Google AI Studio API key.

Do not upload `.env` to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in your terminal, usually `http://localhost:8501`.

## How to Use

1. Open the Streamlit application.
2. Enter one or more webpage URLs, one URL per line.
3. Click **Process URLs**.
4. Wait for the application to load the pages and generate embeddings.
5. Enter a question about the webpage content in the chat input.
6. Read the answer generated from the retrieved context.

## How It Works

1. Document loading. LangChain fetches the content from the supplied webpages.
2. Text splitting. The application splits documents into chunks of 1,000 characters with 200 characters of overlap.
3. Embedding generation. Google Gemini converts the chunks into numerical vectors.
4. Vector storage. The vectors and their associated text are stored in an in memory vector database.
5. Similarity search. The app retrieves up to six relevant chunks for each question.
6. Answer generation. Gemini 2.5 Flash uses the retrieved context to generate an answer.

## Security

* Keep your Google API key in `.env`.
* Add `.env` and your virtual environment folder to `.gitignore`.
* Never commit API keys, passwords, or other secrets.
* If an API key is accidentally published, revoke it and create a replacement.

## Limitations

* The vector database is stored in memory and is rebuilt when the application starts again.
* Results depend on the content accessible from the supplied webpages.
* Some websites block automated requests or restrict access.
* Answers depend on the relevance and quality of the retrieved chunks.
* Google Gemini API usage is subject to the applicable quotas and pricing.

## Future Improvements

* Add PDF and document uploads.
* Support persistent vector storage.
* Add source citations to generated answers.
* Add document deletion and reprocessing options.
* Improve retrieval with metadata filtering and reranking.

## Author

**Siddharth**

GitHub: [SID1ART](https://github.com/SID1ART)

## License

Add a license file if you intend to distribute or allow others to reuse this project. Without a specified license, others do not automatically receive permission to reuse your code.
