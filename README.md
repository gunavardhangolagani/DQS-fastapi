# PDF Document Processing and Querying System

This project is a FastAPI-based backend with a React frontend that allows users to upload PDFs, extract text, generate embeddings using Google Generative AI, and store them in a FAISS vector database for efficient querying.

## Features

  - Upload multiple PDF files for processing.

  - Extract text from PDFs and split it into meaningful chunks.

  - Generate vector embeddings using Google Generative AI.

  - Store embeddings in a FAISS vector database.

  - Query the stored documents using natural language questions.

  - Get AI-generated answers based on the stored document context.

## Tech Stack

### Backend (FastAPI)

- FastAPI (for API development)

- PyPDF2 (for extracting text from PDFs)

- LangChain (for text chunking and AI-powered querying)

- FAISS (for vector storage and similarity search)

- Google Generative AI (for embeddings and conversational AI)

- Uvicorn (for running the FastAPI server)

### Frontend (React)

- React.js (for the user interface)

## Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/gunavardhangolagani/DQS-fastapi.git
```

```
cd your-repo
```
### 2. Backend Setup

- Install Dependencies

```
cd backend
```

```
pip install -r requirements.txt
```

- Set Up Environment Variables
  
```
Create a .env file in the backend folder with the necessary API keys (e.g., Google Generative AI key).
```

### Run the Backend Server

```
uvicorn main:app --reload
```


### 3. Frontend Setup

- Install Dependencies
```
cd frontend/my-app
```

```
npm install
```

- Start the Frontend Server
  
```
npm start
```

### Usage Guide

- Upload one or more PDF files using the UI.

- Once processed, ask questions related to the uploaded documents.

- Receive AI-generated answers based on the document context.

### Contributing

Feel free to submit issues or pull requests. Contributions are welcome!
