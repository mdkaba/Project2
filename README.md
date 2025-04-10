# Concordia AI Assistant 

![image](https://github.com/user-attachments/assets/0b228972-bc7d-4cce-85f9-a8ba148639cc)


A multi-agent chatbot system for Concordia University that provides information about admissions, AI topics, and general university information through a clean, modern UI designed with Concordia's branding.

## 📌 Project Overview

This project implements a ChatGPT-like interface for Concordia University that connects to a multi-agent backend system. The system utilizes LLMs through Ollama to provide specialized responses based on the query type, with agents for admissions information, AI expertise, and general knowledge.

The frontend is built with React and TypeScript, featuring a responsive UI that matches Concordia's brand colors (burgundy, gold, and grey/beige). The backend uses FastAPI with SQLite for conversation history persistence and FAISS for vector storage to enable retrieval-augmented generation (RAG).

## 🚀 Features

### Frontend
- Clean, responsive UI matching Concordia University's brand colors
- Animated typing indicators and loading states
- Error handling with user-friendly error messages
- Persistent conversation history
- Agent-specific message styling
- Mobile-responsive design

### Backend
- FastAPI application with CORS support
- Multi-agent system with specialized knowledge agents:
  - AdmissionsAgent: For university admission queries
  - AIExpertAgent: For AI-related technical questions
  - GeneralAgent: For general information
- Retrieval-augmented generation (RAG) using FAISS vector store
- Conversation history persistence with SQLite
- Integration with Ollama for LLM capabilities
- Knowledge integration from multiple sources:
  - Concordia University website content
  - Wikipedia
  - ArXiv
  - GitHub
  - Web search results

## 📂 Project Structure

```
📂Project2/
├── backend/                  # Backend Python code
│   ├── app/
│   │   ├── agents/           # Agent implementations
│   │   ├── api/              # FastAPI endpoints
│   │   ├── core/             # Core configuration and utilities
│   │   ├── knowledge/        # Knowledge retrieval clients
│   │   ├── models/           # SQLAlchemy models
│   │   ├── repositories/     # Database repositories
│   │   ├── scripts/          # Data ingestion scripts
│   │   ├── services/         # Business logic services
│   │   ├── vectorstores/     # Vector database implementations
│   │   └── main.py           # Application entry point
│   └── management/           # Management scripts
├── frontend/                 # Frontend React application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── assets/           # Frontend assets
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API services
│   │   ├── types/            # TypeScript type definitions
│   │   ├── utils/            # Utility functions
│   │   ├── App.tsx           # Root application component
│   │   ├── SimpleChat.tsx    # Main chat implementation
│   │   └── main.tsx          # Application entry point
│   ├── package.json          # Frontend dependencies
│   └── vite.config.ts        # Vite configuration
├── data/                     # Data files
│   ├── database/             # SQLite database
│   └── vector_store/         # FAISS vector store files
└── requirements.txt          # Python dependencies
```

## 🛠 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Ollama (for local LLM support)
- Git

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mdkaba/Project2.git
cd Project2
```

### 2️⃣ Backend Setup

#### Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Environment Variables

The project includes a `.env` file with the following configuration. Update paths as needed for your system:

```
# API Configuration
API_V1_PREFIX=/api/v1
DEBUG=True

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174

# Database Configuration (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./data/database/chat_history.db

# Ollama Configuration
OLLAMA_API_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=mistral

# Vector Store Settings
VECTOR_STORE_PATH=./data/vector_store

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=./logs/app.log
```

#### Initialize Vector Store (Optional)

To create/update the knowledge base:

```bash
cd backend
python -m app.scripts.ingest_knowledge
```

### 3️⃣ Ollama Setup

Ollama must be installed and running with the Mistral model:

#### Install Ollama

Follow the instructions at https://ollama.ai/ to install Ollama for your operating system.

#### Pull the Mistral Model

```bash
ollama pull mistral
```

#### Start Ollama

```bash
# Start the Ollama server
ollama serve
```

### 4️⃣ Frontend Setup

```bash
cd frontend
npm install
```

### 5️⃣ Running the Application

#### Start the Backend Server

In a terminal window:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### Start the Frontend Development Server

In another terminal window:

```bash
cd frontend
npm run dev
```

The application should now be running at http://localhost:5173 or http://localhost:5174

### 6️⃣ Usage

- Open the frontend URL in your browser
- Start chatting with the AI assistant


## 👨‍💻 Contributors

Mamadou Kaba 

Darian Dotchev 

Kaloyan Kirilov 

Daniel François 

Jaskirat Kaur 




## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
