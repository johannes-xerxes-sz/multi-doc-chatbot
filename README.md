# Multi Document Reader and Chatbot using LangChain and OpenAI

[Updated March 2025 to work with LangChain v0.1.0 and FastAPI Integration]

## Summary
This repository provides Python scripts to help build a multi-document reader and chatbot using **LangChain** and **OpenAI**. It now supports **FastAPI**, allowing interaction through a web API.

The scripts increase in complexity and features:

- `single-doc.py`: Handles a **single PDF**. Sends the entire document content to the LLM prompt.
- `single-long-doc.py`: Handles a **long single PDF**. Uses embeddings and a vector store to send only relevant content to the LLM.
- `multi-doc-chatbot.py`: Handles **multiple documents** (`.pdf`, `.docx`, `.txt`). Remembers chat history and recent conversations. Uses embeddings and vector stores to provide context-aware responses.
- `app.py`: **API version** of the chatbot, built with FastAPI. Allows interaction via HTTP requests, making it suitable for deployment and integration.

I wrote an article exploring these concepts, including a walkthrough for building each script:  
[Read it here](https://medium.com/@ssmaameri/building-a-multi-document-reader-and-chatbot-with-langchain-and-chatgpt-d1864d47e339)

---

## Getting Started

### 1. Clone the Repository
```sh
git clone git@github.com:smaameri/multi-doc-chatbot.git
cd multi-doc-chatbot
```

### 2. Set Up the Virtual Environment
```sh
python3 -m venv .venv
source .venv/bin/activate  # (Linux/macOS)
# OR
.venv\Scripts\activate  # (Windows)
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Store Your OpenAI API Key
Copy the example `.env` file:
```sh
cp .env.example .env
```
Then, open `.env` and paste your **OpenAI API key**:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## Using the Chatbot

### **Run the CLI Version**
To use the chatbot via the terminal, place your documents inside the `/docs` folder and run:
```sh
python3 multi-doc-chatbot.py
```
- Enter questions about your documents.
- Press `q` to exit.

### **Run the API Version**
To use the chatbot as an API, run the FastAPI server:
```sh
uvicorn app:app --reload
```
This starts the server at:
```
http://127.0.0.1:8000
```

#### **Interact with the API (Postman, cURL, or Swagger UI)**
Send a **POST** request to:
```
http://127.0.0.1:8000/ask
```
With the following JSON body:
```json
{
  "question": "What is this document about?"
}
```
##### Example cURL Request:
```sh
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "What is the document about?"}'
```
##### Swagger UI:
Visit:
```
http://127.0.0.1:8000/docs
```
Click `POST /ask`, then enter a question in the request body.

---

## Future Enhancements
✅ **Optimize Retrieval**: Fine-tune chunking strategies for better accuracy.
✅ **Improve Response Quality**: Use context filtering to prevent hallucinations.
✅ **Enhance Security**: Implement rate-limiting and input validation.
✅ **Deploy API**: Run on AWS/GCP/Docker for scalability.

![App Screenshot](./img/app-screenshot.png)

---

This project provides a solid foundation for building **document-aware chatbots**. While the current setup works, there is always room for improvement by exploring **advanced prompt engineering**, **custom embeddings**, and **hybrid retrieval methods**. 🚀

