import os
import sys
from pathlib import Path

# Add Backend and Frontend folders to sys.path
api_dir = Path(__file__).parent
project_root = api_dir.parent
backend_dir = project_root / "Backend"
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import traceback
import requests

# Import Backend RAG components
from main import setup_pipeline
from rag.utils.config import RAGConfig

app = FastAPI(title="AgroChat API", description="API bridging Streamlit frontend with backend RAG pipeline")

# Global pipeline instance
pipeline = None

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    global pipeline
    print("Initializing RAG Pipeline...")
    # Change current working directory to backend so that paths like 'data/' work properly
    os.chdir(str(backend_dir))
    
    config = RAGConfig()
    try:
        pipeline = setup_pipeline(config)
        print("RAG Pipeline initialized successfully.")
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        traceback.print_exc()

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=503, detail="RAG Pipeline is not available.")
    
    try:
        config = RAGConfig()
        
        # 1. Retrieve relevant documents using the pipeline's retriever
        retrieved_docs = pipeline.retriever.retrieve(
            query=request.message,
            top_k=config.retrieval.top_k
        )
        
        # 2. Extract text from the retrieved documents to form the context
        context_texts = [doc["document"].get("text", "") for doc in retrieved_docs]
        context_string = "\n\n".join(context_texts)
        
        # 3. Construct the RAG prompt
        prompt = f"Context: {context_string}\n\nQuestion: {request.message}\n\nAnswer:"
        
        # 4. Prepare the payload for Ollama
        ollama_url = f"{config.llm.base_url}/api/generate"
        payload = {
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
        
        # 5. Call Ollama API using requests
        print(f"Sending request to Ollama with model: {payload['model']}")
        ollama_response = requests.post(ollama_url, json=payload, timeout=60)
        ollama_response.raise_for_status()
        
        # 6. Extract the generated response text
        response_data = ollama_response.json()
        generated_text = response_data.get("response", "No answer generated.")
        
        # Format the response in a way the frontend expects
        return {
            "text": generated_text,
            "message_type": "text",
            "sources": str(retrieved_docs)
        }
    except Exception as e:
        print("Error during chat query:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
