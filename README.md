# Domain Specific AI Agent

## Overview

Domain Specific AI Agent is a Retrieval-Augmented Generation (RAG) application that allows admin to upload documents only and both admin and user can ask questions based on the content which is uploaded by admin.

The system extracts text from uploaded documents, generates embeddings using OpenAI, stores vectors in ChromaDB, retrieves relevant context for user queries, and generates answers using an LLM. And also admin can delete the uploaded documents anytime and upload an updated document.

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control (Admin/User)

### Document Management

* Upload PDF and TXT documents(Admin)
* List uploaded documents(Admin)
* Delete documents(Admin)
* Automatic document ingestion pipeline

### Knowledge Retrieval

* Text extraction
* Document chunking
* OpenAI embeddings
* ChromaDB vector storage
* Semantic search

### Question Answering

* Retrieval-Augmented Generation (RAG)
* Source document references
* Chat history tracking
* Last 10 conversations retained per user

### Frontend

* Streamlit-based user interface
* Admin document management panel
* Question-answer interface
* Chat history display

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication

### AI / RAG

* OpenAI API
* ChromaDB
* Embeddings
* Retrieval-Augmented Generation

### Frontend

* Streamlit

## Project Structure

Domain-Knowledge-Copilot/
│
├── backend/
│   ├── auth/
│   ├── database/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── ingestion/
│   ├── vectorstore/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── uploads/
├── chroma_db/
├── sample_data/
│
├── requirements.txt
├── .env.example
└── README.md


## Prerequisites

* Python 3.11+
* OpenAI API Key



## Installation

### 1. Clone the Repository

git clone <GITHUB_REPOSITORY_URL>
cd Domain-Knowledge-Copilot

### 2. Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux / macOS:

python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

## Environment Variables

Create a `.env` file in the project root.

Example:

OPENAI_API_KEY=your_openai_api_key

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

## Running the Application

### Start FastAPI Backend

From the project root:

uvicorn backend.main:app --reload

Backend URL:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs

### Start Streamlit Frontend

Open a new terminal and activate the virtual environment.

Run:
streamlit run frontend/app.py


Frontend URL:

http://localhost:8501

Frontend Screenshots:
screenshots/frontend_ui


## Usage

### Admin Workflow

1. Register an account 
2. Assign admin role 
3. Login
4. Upload PDF/TXT documents
5. View uploaded documents
6. Delete documents when required

### User Workflow

1. Login
2. Ask questions about uploaded documents
3. View generated answers
4. Review source references
5. Access recent chat history

## Database

The application uses SQLite with SQLAlchemy ORM.

Core Models
1. User - id, username, email, hashed_password, role
2. Document - id, filename, filepath, uploaded_at, owner_id
3. ChatHistory - id, user_id, question, answer, created_at

Relationships
User
 ├── Documents (1:N)
 └── ChatHistory (1:N)

## Model Source

backend/database/models.py

screenshots/database_schema

## Database File

knowledge_agent.db

## RAG Workflow

Upload Document
        ↓
Extract Text
        ↓
Chunk Text
        ↓
Generate Embeddings
        ↓
Store in ChromaDB
        ↓
User Question
        ↓
Retrieve Relevant Chunks
        ↓
Generate Answer
        ↓
Return Answer + Sources

## Future Enhancements

* Docker Support
* Cloud Deployment
* LangGraph Workflow Integration
* Streaming Responses
* User Management Dashboard

## Author

Chaitra Acharya

Domain Specific AI Agent – RAG-based AI Assistant using FastAPI, Streamlit, OpenAI, and ChromaDB.
