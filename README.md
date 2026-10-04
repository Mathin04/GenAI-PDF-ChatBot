GenAI PDF ChatBot

### AI-Powered Document Intelligence with Retrieval-Augmented Generation
Live Demo:http://localhost:8502/
> **Upload a PDF. Ask questions. Get context-aware answers.**

**GenAI PDF ChatBot** is an AI-powered document question-answering application that enables users to interact with PDF documents using natural language. The application combines **Retrieval-Augmented Generation (RAG)**, **semantic embeddings**, **FAISS vector search**, **LangChain**, and **Google Gemini** to retrieve relevant document context and generate meaningful responses.

Built with **Python and Streamlit**, this project demonstrates an end-to-end implementation of a modern **Generative AI application**, from document ingestion and text processing to semantic retrieval and LLM-powered response generation.

 Why This Project?

Traditional PDF readers require users to manually search through large documents to find relevant information.

This project transforms that experience into an **interactive AI-powered document assistant**.

Instead of searching for keywords manually, users can ask questions such as:

> "What are the main findings of this document?"**

> "Explain the methodology used in this research paper."**

> "Summarize the important points from this PDF."**

The system retrieves relevant information from the uploaded document and uses the retrieved context to generate an answer.

 Key Features

 **PDF Document Processing** — Extract text from uploaded PDF documents.
 **Natural Language Q&A** — Ask questions conversationally instead of manually searching documents.
 **Retrieval-Augmented Generation (RAG)** — Ground responses using relevant information retrieved from the document.
 **Semantic Search** — Retrieve relevant content based on contextual meaning rather than exact keyword matching.
 **Text Chunking** — Break large documents into manageable sections for efficient retrieval.
 **Vector Embeddings** — Convert document content into numerical representations for similarity search.
 **FAISS Vector Store** — Perform efficient similarity-based document retrieval.
 **Google Gemini Integration** — Generate natural-language responses using a modern LLM.
 **LangChain Pipeline** — Orchestrate document processing, retrieval, and LLM interaction.
 **Streamlit UI** — Provide a simple and interactive web interface.
 **Environment-Based Secrets** — Keep API credentials outside the source code.
 **Deployment Ready** — Structured for cloud deployment with dependency and runtime configuration.

 System Architecture


                    ┌──────────────────────┐
                    │     Upload PDF       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PDF Text Extraction│
                    │        (PyPDF)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Text Chunking     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Hugging Face         │
                    │ Text Embeddings      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FAISS Vector Store │
                    └──────────┬───────────┘
                               │
                               │
                ┌──────────────▼──────────────┐
                │        User Question        │
                └──────────────┬──────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Query Embedding     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Semantic Similarity  │
                    │      Retrieval       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant PDF Context │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Google Gemini     │
                    │         LLM          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Context-Aware Answer│
                    └──────────────────────┘

 RAG Workflow

The application follows a **Retrieval-Augmented Generation** workflow:

 1. Document Ingestion

The user uploads a PDF through the Streamlit interface.

 2. Text Extraction

The PDF content is extracted using **PyPDF**.

 3. Text Chunking

Large amounts of extracted text are divided into smaller chunks to make retrieval more effective.

 4. Embedding Generation

The text chunks are converted into vector representations using **Hugging Face embeddings**.

 5. Vector Storage

The generated embeddings are stored in a **FAISS vector store**.

 6. Query Processing

When a user asks a question, the question is converted into an embedding.

 7. Semantic Retrieval

FAISS performs similarity search to identify the most relevant sections of the uploaded document.

 8. Context-Aware Generation

The retrieved document context is passed to **Google Gemini**, which generates the final response.

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS
 ↓
User Query
 ↓
Semantic Retrieval
 ↓
Relevant Context
 ↓
Google Gemini
 ↓
Generated Answer

 Technology Stack

| Technology        | Role                         |
| ----------------- | ---------------------------- |
| **Python**        | Core application development |
| **Streamlit**     | Interactive web application  |
| **LangChain**     | RAG and LLM orchestration    |
| **Google Gemini** | Large Language Model         |
| **Hugging Face**  | Text embedding generation    |
| **FAISS**         | Vector similarity search     |
| **PyPDF**         | PDF text extraction          |
| **python-dotenv** | Environment configuration    |
| **NumPy**         | Numerical operations         |
| **Pandas**        | Data processing              |


 Project Structure


GenAI-PDF-ChatBot/
│
├── app.py
│
├── utils/
│   ├── pdf_loader.py
│   └── vector_store.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── runtime.txt
├── test_gemini.py
└── README.md


 Main Components

**`app.py`**

Main Streamlit application responsible for the user interface and chatbot workflow.

**`utils/pdf_loader.py`**

Handles PDF document loading and text extraction.

**`utils/vector_store.py`**

Handles embedding generation and vector-store operations.

**`test_gemini.py`**

Used to verify Gemini API connectivity/configuration.

**`requirements.txt`**

Contains the Python dependencies required to run the application.

**`runtime.txt`**

Specifies the Python runtime for deployment.

**`.env.example`**

Provides the expected environment-variable structure without exposing the actual API key.

 Getting Started
 1. Clone the Repository

```bash
git clone https://github.com/Mathin04/GenAI-PDF-ChatBot.git
```

```bash
cd GenAI-PDF-ChatBot
```

---

 2. Create a Virtual Environment

 Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

 macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never commit the `.env` file to GitHub.

---

 5. Run the Application

```bash
streamlit run app.py
```

The application will start locally and can be accessed through the Streamlit URL shown in the terminal.

---

 Security

API credentials should never be hard-coded into the application or committed to GitHub.

This project uses environment-based configuration for sensitive credentials.

Recommended `.gitignore`:

```gitignore
venv/
.env
__pycache__/
*.pyc
```

The repository includes an `.env.example` file so that developers can understand the required configuration without exposing private credentials.

---

 Example Questions

After uploading a PDF, users can ask:

```text
What is the main objective of this document?

Summarize the key points.

What are the major findings?

Explain the methodology used.

What conclusions are presented?

What challenges are discussed?

What are the important recommendations?

Explain this section in simple terms.
```



 Potential Use Cases

The application can be useful for:

 **Students** — Interact with textbooks, notes, and study materials.
 **Researchers** — Explore research papers and technical documents.
 **Business Users** — Query reports and business documents.
 **Knowledge Workers** — Quickly retrieve information from lengthy PDFs.
 **Technical Teams** — Interact with technical documentation.
 **Readers** — Ask questions about books and other PDF content.


 Engineering Concepts Demonstrated

This project provides practical implementation experience with:

 Generative AI

* Large Language Models
* Google Gemini API
* Prompt-based generation

 Retrieval-Augmented Generation

* Document ingestion
* Text chunking
* Context retrieval
* Retrieval + generation pipeline

 Vector Search

* Text embeddings
* Semantic similarity
* FAISS vector database

 AI Application Development

* LangChain
* Streamlit
* Python
* Environment configuration
* API integration

 Deployment

* Dependency management
* Runtime configuration
* Environment secrets
* Cloud deployment preparation


 Project Highlights

| Area                    | Implementation                 |
| ----------------------- | ------------------------------ |
| **AI Architecture**     | Retrieval-Augmented Generation |
| **LLM**                 | Google Gemini                  |
| **Embeddings**          | Hugging Face                   |
| **Vector Database**     | FAISS                          |
| **Framework**           | LangChain                      |
| **Frontend**            | Streamlit                      |
| **Document Processing** | PyPDF                          |
| **Language**            | Python                         |
| **Configuration**       | Environment Variables          |
| **Deployment**          | Streamlit-ready                |


 Future Enhancements

The project can be extended with:

* [ ] Multi-PDF conversations
* [ ] Chat history and conversational memory
* [ ] Page-level source citations
* [ ] Document summarization mode
* [ ] Multiple document formats
* [ ] Advanced retrieval and reranking
* [ ] Persistent vector databases
* [ ] User authentication
* [ ] Conversation export
* [ ] Improved document preprocessing
* [ ] Production monitoring and evaluation


 What This Project Demonstrates

This project goes beyond simply connecting an LLM to a user interface.

It demonstrates the complete lifecycle of a **RAG-based Generative AI application**:

```text
Document Ingestion
       ↓
Information Extraction
       ↓
Text Processing
       ↓
Embedding Generation
       ↓
Vector Indexing
       ↓
Semantic Retrieval
       ↓
Context Construction
       ↓
LLM Generation
       ↓
User-Facing Response
```

The architecture separates **knowledge retrieval** from **language generation**, allowing the LLM to generate responses using information retrieved from the user's document.


 Resume-Ready Project Summary

> **GenAI PDF ChatBot** — Developed a RAG-based document intelligence application using **Python, LangChain, Google Gemini, Hugging Face embeddings, and FAISS** to enable semantic PDF search and context-aware question answering through an interactive **Streamlit** interface.


 Author

 Mathin Shaik

Aspiring AI / ML & Generative AI Developer**

Interested in:

* Generative AI
* Large Language Models
* Retrieval-Augmented Generation
* Machine Learning
* Python Development
* AI Application Development


 Show Your Support

If you found this project useful or interesting, consider giving the repository a ⭐.

GitHub:
https://github.com/Mathin04/GenAI-PDF-ChatBot


 License

This project is intended for educational, learning, and portfolio purposes.
