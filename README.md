# RAG Chatbot - UET Peshawar Admission Assistant

A comprehensive RAG (Retrieval-Augmented Generation) chatbot application built with Python, FastAPI, and Docker. This project serves as an educational resource to understand core technologies including **RAG systems**, **FastAPI**, and **Docker containerization**.

## 📚 Course Information

**Subject**: Computational Intelligence  
**Semester**: 7th  
**Project Type**: Semester Project  
**Lecturer**: [Hamas Ur Rehman](https://github.com/Hamas-ur-Rehman)

## 📋 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot system designed to answer questions about UET Peshawar admissions. The chatbot is specifically trained on the **UET Peshawar Undergraduate Prospectus 2022-23** and provides accurate answers to students from batch 2022-26 regarding admission requirements, programs, procedures, and university information.

### Core Purpose

This project was developed to understand and demonstrate:

- **RAG (Retrieval-Augmented Generation)**: Implementing a RAG pipeline using vector databases (ChromaDB) and embedding models to retrieve relevant context from documents before generating responses
- **FastAPI**: Building modern, high-performance REST APIs with automatic documentation
- **Docker**: Containerizing applications for consistent deployment across different environments

## 🎯 Key Features

- **RAG-based Q&A System**: Answers questions using context retrieved from the UET Peshawar Prospectus 2022-23
- **Vector Database**: Uses ChromaDB with HuggingFace embeddings for semantic search
- **Modern Web Interface**: Clean, ChatGPT-like UI built with vanilla HTML, CSS, and JavaScript
- **Chat History**: MongoDB integration for persistent conversation history
- **Document Ingestion**: API endpoint to add new PDF documents to the knowledge base
- **Docker Support**: Fully containerized application ready for deployment

## 🏛️ About the Knowledge Base

The chatbot's knowledge base is built from the **UET Peshawar Undergraduate Prospectus 2022-23** (PROPECTUS 2022-23.pdf). This document contains comprehensive information about:

- Admission requirements and procedures
- Academic programs and departments
- Campus facilities and locations
- University policies and regulations
- Contact information for various departments
- Hostel and accommodation details

The system is specifically designed to assist **students from batch 2022-26** with questions related to UET Peshawar admissions and university information.

## 🛠️ Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for building LLM applications
- **ChromaDB**: Vector database for storing and retrieving document embeddings
- **HuggingFace**: Sentence transformers for generating embeddings
- **OpenAI GPT-4o-mini**: LLM for generating responses
- **MongoDB (Motor)**: Database for storing chat history
- **PyPDF**: PDF document processing

### Frontend
- **Vanilla HTML/CSS/JavaScript**: Modern, responsive chat interface
- **ChatGPT-inspired UI**: Professional, elegant design

### DevOps
- **Docker**: Containerization for deployment
- **Uvicorn**: ASGI server for FastAPI

## 📁 Project Structure

```
rag-chat-bot/
├── main.py                 # FastAPI application and API endpoints
├── chat_bot.py            # ChatBot class with OpenAI integration
├── vector_db.py           # VectorDatabase class for ChromaDB operations
├── pdf_handler.py         # PDFHandler for extracting and chunking PDFs
├── database.py            # MongoDB handler for chat history
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore          # Files to exclude from Docker build
├── DEPLOYMENT.md          # Detailed Docker deployment guide
├── frontend/              # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── vector_db/             # ChromaDB persistent storage
└── PROPECTUS 2022-23.pdf  # Source document for RAG
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MongoDB (for chat history)
- OpenAI API Key
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/malikmajeed/rag_chat_bot.git
   cd rag-chat-bot
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv virtual
   source virtual/bin/activate  # On Windows: virtual\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=mongodb://localhost:27017
   ```

5. **Initialize the vector database** (if not already done)
   ```bash
   python first_run.py
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

7. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🐳 Docker Deployment

For detailed Docker deployment instructions, including build commands, container management, and production deployment, please refer to **[DEPLOYMENT.md](DEPLOYMENT.md)**.

### Quick Docker Commands

```bash
# Build the image
docker build -t rag-chatbot:latest .

# Run the container
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e MONGODB_URI=mongodb://your_mongo_uri \
  -v $(pwd)/vector_db:/app/vector_db \
  --restart unless-stopped \
  rag-chatbot:latest
```

## 📚 Understanding the Core Technologies

### RAG (Retrieval-Augmented Generation)

This project demonstrates RAG by:
1. **Document Processing**: Extracting and chunking PDF documents
2. **Embedding Generation**: Converting text chunks into vector embeddings using HuggingFace models
3. **Vector Storage**: Storing embeddings in ChromaDB for efficient similarity search
4. **Context Retrieval**: Finding relevant document chunks based on user queries
5. **Response Generation**: Using retrieved context to generate accurate answers via OpenAI

### FastAPI

FastAPI is used to:
- Create RESTful API endpoints (`/api/chat`, `/api/ingest`, `/api/clear-chat`)
- Serve static frontend files
- Handle CORS for frontend-backend communication
- Provide automatic API documentation at `/docs`

### Docker

Docker implementation includes:
- Multi-stage builds for optimization
- Non-root user for security
- Health checks for monitoring
- Volume mounts for data persistence
- Environment variable configuration

## 🔌 API Endpoints

- `GET /` - Serve frontend interface
- `POST /api/chat` - Send a message and get AI response
- `POST /api/ingest` - Add a new PDF document to the knowledge base
- `POST /api/clear-chat` - Clear chat history for a user
- `GET /health` - Health check endpoint

## 📖 Usage Example

1. Start the application (locally or via Docker)
2. Open http://localhost:8000 in your browser
3. Ask questions like:
   - "What are the admission requirements for undergraduate programs?"
   - "Tell me about the Computer Science department"
   - "What are the hostel facilities available?"
   - "How can I contact the admissions office?"

The chatbot will retrieve relevant information from the UET Peshawar Prospectus 2022-23 and provide accurate answers.

## 🎓 Educational Value

This project serves as a comprehensive learning resource for:

- **RAG Architecture**: Understanding how to combine retrieval systems with language models
- **Vector Databases**: Working with embeddings and similarity search
- **API Development**: Building production-ready REST APIs with FastAPI
- **Containerization**: Dockerizing Python applications for deployment
- **Full-Stack Development**: Integrating frontend and backend systems

## 📝 Notes

- The vector database (`vector_db/`) should be persisted using Docker volumes in production
- Ensure MongoDB is running and accessible for chat history functionality
- The system requires an OpenAI API key for LLM responses
- PDF documents are processed and chunked before being added to the vector database

## 🤝 Contributing

This is an educational project. Feel free to fork, modify, and learn from it!

## 📄 License

This project is for educational purposes.

## 📧 Contact

For questions about UET Peshawar admissions, please contact:
- **Directorate of Admissions**: admission@uetpeshawar.edu.pk
- **Website**: www.uetpeshawar.edu.pk

## 🙏 Acknowledgments

This project was developed as part of the **Computational Intelligence** course (7th Semester) at UET Peshawar under the guidance of **Hamas Ur Rehman**.

- **Course**: Computational Intelligence
- **Semester**: 7th
- **Project Type**: Semester Project
- **Instructor**: [Hamas Ur Rehman](https://github.com/Hamas-ur-Rehman) - AI/ML Enthusiast and Lecturer at UET Peshawar

---

**Note**: This chatbot is based on the UET Peshawar Undergraduate Prospectus 2022-23 and is designed to assist students from batch 2022-26 with admission-related queries.
