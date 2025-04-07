# Multi-Agent Chatbot System

A collaborative project for Concordia University implementing a multi-agent chatbot system using modern AI technologies.

## Project Structure

```
.
├── backend/              # Python FastAPI backend
│   ├── app/             # Application code
│   │   ├── agents/      # Agent implementations
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── tests/       # Test files
│   └── requirements.txt # Python dependencies
├── frontend/            # React TypeScript frontend
│   ├── src/            # Source code
│   │   ├── components/ # React components
│   │   ├── context/    # React context
│   │   ├── hooks/      # Custom hooks
│   │   ├── services/   # API services
│   │   ├── types/      # TypeScript types
│   │   └── utils/      # Utility functions
│   └── package.json    # Node.js dependencies
└── data/               # Data storage
    └── vectorstore/    # FAISS vector store data
```

## Setup Instructions

### Prerequisites

1. **Python 3.9+**
   - Download and install from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Node.js and npm**
   - Download and install from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

3. **Ollama**
   - Download and install from [ollama.ai](https://ollama.ai/)
   - Start Ollama service: `ollama serve`
   - Pull Mistral model: `ollama pull mistral`

### Backend Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update variables as needed

4. Run tests to verify setup:
   ```bash
   python backend/app/tests/test_ollama.py
   python backend/app/tests/test_langchain.py
   python backend/app/tests/test_vectorstore.py
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Access the application at `http://localhost:5173`

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing

- Backend tests: Run `python -m pytest backend/app/tests`
- Frontend tests: Run `npm test` in the frontend directory

## Current Status

- [x] Project structure set up
- [x] Backend dependencies installed
- [x] Frontend dependencies installed
- [x] Basic tests passing
- [ ] Chatbot implementation
- [ ] Multi-agent system
- [ ] User interface
- [ ] Deployment configuration

## Team Members

- Mamadou
- Kaloyan
- Darian
- Daniel
- Jaskirat

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.