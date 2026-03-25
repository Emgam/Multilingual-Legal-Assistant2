# Project Specifications

## 1. Project Title
AI-Based Multilingual Backend System for Tunisian Startup Creation and CNSS Procedures

## 2. Project Context
In Tunisia, startup creation and CNSS procedures are distributed across legal and administrative sources (laws, decrees, guides), often written in formal legal French or Arabic. This makes information difficult to access for students and young entrepreneurs, especially when their natural interaction language is Tunisian Arabic dialect.

This project provides an academic AI backend that centralizes and simplifies these procedures, with multilingual question answering, voice query support, and integrated analytics.

## 3. Project Objectives

### Main Objective
Develop a multilingual AI-powered backend that retrieves, explains, and simplifies Tunisian startup and CNSS procedures from curated official/legal content.

### Specific Objectives
- Extract and structure startup creation procedures.
- Extract and structure CNSS employer and employee procedures.
- Support questions in English, French, and Tunisian dialect (with Arabic script treated as Darija in detection).
- Return responses in the detected/requested language.
- Use semantic retrieval over a curated dataset.
- Provide backend BI analytics on usage and procedures.

## 4. Project Scope

### Included
- Startup and SME creation procedures.
- Legal registration process details relevant to startup setup.
- CNSS employer registration.
- CNSS employee declaration/obligation content.
- Backend analytics for queries and procedure categories.

### Excluded
- Tax filing/declaration workflows.
- Accounting and financial management support.
- Legal interpretation or legal advice.
- Frontend implementation scope in this specification (frontend exists in repository but is outside backend functional scope).

## 5. Target Users
- Students.
- Young entrepreneurs (educational/informational use).
- Researchers.
- Academic supervisors.

## 6. Functional Requirements

### FR1 - Legal Document Collection
Implemented as an offline data pipeline through scripts:
- merge_dataset.py
- transform_dataset.py
- validate_rag_dataset.py

The pipeline merges selected JSON sources, transforms them into RAG format, and validates structure/quality.

### FR2 - Procedure Extraction and Structuring
Implemented through curated dataset construction and metadata tagging:
- Procedure categories are mapped in dataset entries and used in retrieval metadata.
- Startup and CNSS-related procedures are organized for API retrieval.

### FR3 - Multilingual Semantic Search
Implemented in FAISS-based retrieval:
- Embedding model: nomic-embed-text (Ollama).
- Language mapping and retrieval filtering are applied before response generation.
- Query category hints (startup vs CNSS) are used to improve relevance.

### FR4 - Procedure Simplification
Implemented at dataset and answer levels:
- Dataset contains simplified procedural text.
- LLM prompts enforce simple, grounded, context-only answers.
- Output is structured from retrieved legal/procedural context.

### FR5 - Multilingual Question Answering
Implemented via:
- POST /ask
- POST /ask/evaluate

Behavior:
- Uses only retrieved dataset context.
- Returns source metadata with each answer.
- Includes fallback messages when information is unavailable in retrieved context.

### FR6 - Speech-to-Text (STT) Support
Implemented via:
- POST /ask/voice

Behavior:
- Accepts uploaded audio files (WAV/MP3).
- Uses SpeechRecognition (Google recognizer) for transcription.
- Routes transcription to the same pipeline as text queries.

### FR7 - Business Intelligence (Backend Integrated)
Implemented with in-memory tracking and analytics endpoints:
- GET /analytics/overview
- GET /analytics/procedures
- GET /analytics/languages
- GET /analytics/keywords
- GET /analytics/queries

Tracked indicators include:
- Query volume and answer rate.
- Procedure category hits.
- Language distribution.
- Top keywords.
- Recent query history.

## 7. Non-Functional Requirements
- Clear, explainable outputs with source references.
- Modular FastAPI backend (API, core, config, analytics, utils).
- Academic-scale dataset and local indexing.
- Grounded answers with fallback behavior.
- Informational use only (no legal advice).

## 8. Technical Architecture

### Backend Framework
FastAPI (Python).

### Architecture Style
Monolithic backend with modular layers:
- Ingestion and transformation scripts.
- Vector indexing/retrieval (FAISS).
- Language detection and response cleaning.
- QA orchestration (prompting + generation + optional extractive comparison).
- Analytics tracking.
- REST API endpoints.

### Language and Speech Layer
- Language detection utility for EN/FR/Arabic-script inputs.
- Retrieval language mapping for better matching.
- Speech-to-text preprocessing in voice endpoint.

## 9. AI and NLP Techniques Used
- Text preprocessing and dataset normalization.
- Language detection heuristics.
- Multilingual embeddings via Ollama.
- Embedding-based semantic retrieval with threshold filtering.
- Prompt-constrained grounded generation.
- Optional extractive QA comparison using TunBERT-compatible pipeline.
- Query and keyword analytics.

## 10. Data Sources

### Primary Source Type
Curated public legal/administrative content represented as repository JSON sources.

### Included Source Files
Input entries are merged from datasets/entry1.json through datasets/entry11.json and datasets/metadata.json, then transformed into datasets/rag_dataset.json.

## 11. Dataset Size
- Validated transformed dataset target: 62 documents (see validate_rag_dataset.py expected count).
- Academic-scale and intentionally limited.

## 12. API Endpoints (Implemented)

### QA
- POST /ask
- POST /ask/evaluate
- POST /ask/voice

### Procedures
- GET /procedures/startup
- GET /procedures/cnss
- GET /procedures/all

### Analytics
- GET /analytics/overview
- GET /analytics/procedures
- GET /analytics/languages
- GET /analytics/keywords
- GET /analytics/queries

### Health and Debug
- GET /
- GET /debug/search
- GET /debug/index-stats
- GET /debug/json-keys

## 13. Project Deliverables
- FastAPI backend for multilingual procedural QA.
- Structured RAG dataset and FAISS index.
- API routes for procedures, QA, voice, and analytics.
- Configuration and scripts for data preparation and validation.

## 14. Constraints and Limitations
- Educational/informational purpose only.
- No official legal advice or legal liability.
- Limited dataset coverage.
- Analytics storage is in-memory (non-persistent) in current implementation.
- Voice transcription depends on external speech recognition service behavior.

## 15. Implementation Snapshot

### Core Stack
- FastAPI
- LangChain community integrations
- FAISS (CPU)
- Ollama models: nomic-embed-text and llama3.2
- SpeechRecognition for voice endpoint

### Quick Run
1. Install dependencies from rag/requirements.txt.
2. Ensure Ollama is running with required models pulled.
3. Start API with: uvicorn main:app --reload --port 8000 (from rag directory).
4. Open API docs at /docs.

---

**Built with ❤️ for Tunisian entrepreneurs and businesses**
