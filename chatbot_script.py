import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv('.env')

# Initialize FastAPI
app = FastAPI()

# Load and process documents
documents = []
for file in os.listdir("docs"):
    file_path = os.path.join("docs", file)
    if file.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file.endswith(".docx") or file.endswith(".doc"):
        loader = Docx2txtLoader(file_path)
    elif file.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        continue
    documents.extend(loader.load())

# Split documents
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=50)
documents = text_splitter.split_documents(documents)

# Store embeddings in ChromaDB
vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory="./data")
vectordb.persist()

# Q&A chain
pdf_qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo'),
    retriever=vectordb.as_retriever(search_kwargs={'k': 4}),  # Adjust 'k' for better focus
    return_source_documents=True
)

# Track chat history
chat_history = []

# Request model
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    global chat_history

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    response = pdf_qa.invoke({"question": request.question, "chat_history": chat_history})
    
    # Prevent hallucinations by ensuring response is based on document context
    if "I don't know" in response["answer"] or not response["answer"].strip():
        response["answer"] = "I can’t confidently answer that based on the provided documents."

    chat_history.append((request.question, response["answer"]))
    
    return {
        "answer": response["answer"],
        "sources": [doc.metadata["source"] for doc in response["source_documents"]]
    }

# Run with: uvicorn app:app --reload
