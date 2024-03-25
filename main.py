from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfReader
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = FastAPI()

@app.post("/upload/")
async def upload_pdf(pdf_files: List[UploadFile] = File(...)):
    try:
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return {"message": "PDF files uploaded and processed successfully"}
    except Exception as e:
        logging.error("An error occurred during PDF processing: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/query/")
async def query_document(user_question: str):
    try:
        chain = get_conversational_chain()
        response = user_input(user_question, chain)
        return {"response": response}
    except Exception as e:
        logging.error("An error occurred during document query: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_pdf_text(pdf_files):
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf.file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    if embeddings is None:
        logging.error("Failed to initialize embeddings.")
        return
    try:
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as e:
        logging.error("An error occurred while creating the vector store: %s", e)

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, chain):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    try:
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        return response["output_text"]
    except BlockedPromptException as e:
        logging.error("An error occurred during user input processing: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
