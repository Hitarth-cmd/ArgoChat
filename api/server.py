# import os
# import sys
# from pathlib import Path

# # Add Backend and Frontend folders to sys.path
# api_dir = Path(__file__).parent
# project_root = api_dir.parent
# backend_dir = project_root / "Backend"
# sys.path.insert(0, str(backend_dir))

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import uvicorn
# import traceback
# import requests

# # Import Backend RAG components
# from main import setup_pipeline
# from rag.utils.config import RAGConfig

# app = FastAPI(title="AgroChat API", description="API bridging Streamlit frontend with backend RAG pipeline")

# # Global pipeline instance
# pipeline = None

# class ChatRequest(BaseModel):
#     message: str

# @app.on_event("startup")
# async def startup_event():
#     global pipeline
#     print("Initializing RAG Pipeline...")
#     # Change current working directory to backend so that paths like 'data/' work properly
#     os.chdir(str(backend_dir))
    
#     config = RAGConfig()
#     try:
#         pipeline = setup_pipeline(config)
#         print("RAG Pipeline initialized successfully.")
#     except Exception as e:
#         print(f"Error initializing pipeline: {e}")
#         traceback.print_exc()

# @app.post("/chat")
# def chat_endpoint(request: ChatRequest):
#     global pipeline
#     if not pipeline:
#         raise HTTPException(status_code=503, detail="RAG Pipeline is not available.")
    
#     try:
#         config = RAGConfig()
        
#         # 1. Retrieve relevant documents using the pipeline's retriever
#         retrieved_docs = pipeline.retriever.retrieve(
#             query=request.message,
#             top_k=config.retrieval.top_k
#         )
        
#         # 2. Extract text from the retrieved documents to form the context
#         context_texts = [doc["document"].get("text", "") for doc in retrieved_docs]
#         context_string = "\n\n".join(context_texts)
        
#         # 3. Construct the RAG prompt
#         prompt = f"Context: {context_string}\n\nQuestion: {request.message}\n\nAnswer:"
        
#         # 4. Prepare the payload for Ollama
#         ollama_url = f"{config.llm.base_url}/api/generate"
#         payload = {
#             "model": "phi3",
#             "prompt": prompt,
#             "stream": False,
#             "options": {
#                 "num_ctx": 2048
#             }
#         }
        
#         # 5. Call Ollama API using requests
#         print(f"Sending request to Ollama with model: {payload['model']}")
#         ollama_response = requests.post(ollama_url, json=payload, timeout=180)
#         ollama_response.raise_for_status()
        
#         # 6. Extract the generated response text
#         response_data = ollama_response.json()
#         generated_text = response_data.get("response", "No answer generated.")
        
#         # Format the response in a way the frontend expects
#         return {
#             "text": generated_text,
#             "message_type": "text",
#             "sources": str(retrieved_docs)
#         }
#     except Exception as e:
#         print("Error during chat query:", e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(
#         app, 
#         host="0.0.0.0",
#         port=8000,
#         timeout_keep_alive=300
#     )


import os
import sys
from pathlib import Path
import traceback

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx

# -----------------------------
# Setup Paths
# -----------------------------
api_dir = Path(__file__).parent
project_root = api_dir.parent
backend_dir = project_root / "Backend"
sys.path.insert(0, str(backend_dir))

# -----------------------------
# Import Backend
# -----------------------------
from main import setup_pipeline
from rag.utils.config import RAGConfig
from ocean.ocean_processor import OceanProcessor

# -----------------------------
# App Init
# -----------------------------
app = FastAPI(
    title="AgroChat API",
    description="API bridging Streamlit frontend with backend RAG pipeline"
)

pipeline = None
ocean_processor = None


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
async def startup_event():
    global pipeline, ocean_processor
    print("Initializing RAG Pipeline & Ocean Processor...")

    os.chdir(str(backend_dir))

    config = RAGConfig()

    try:
        pipeline = setup_pipeline(config)
        ocean_processor = OceanProcessor()
        print("Services initialized successfully.")
    except Exception as e:
        print(f"Error initializing services: {e}")
        traceback.print_exc()


# -----------------------------
# Chat Endpoint (ASYNC)
# -----------------------------
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global pipeline, ocean_processor

    if not pipeline:
        raise HTTPException(status_code=503, detail="RAG Pipeline is not available.")

    try:
        system_prompt = """Role: You are an AI Data Analyst for the "Antigravity" project. Your goal is to assist users with data queries by providing both textual insights and visual representations within the same response.

Task Logic:
Analyze the Query: Determine if the user's request involves trends, comparisons, distributions, or specific data points that benefit from a visual format.
Textual Response: Always provide a concise, professional explanation of the data or the answer to the query.
Conditional Visualization: If (and only if) the data can be better represented visually, generate a JSON block following this structure:

```json
{
  "render_chart": true,
  "chart_type": "bar | line | pie | scatter",
  "data": [ {"label": "X", "value": Y} ],
  "options": { "title": "...", "xAxis": "...", "yAxis": "..." }
}
```

IMPORTANT RULES FOR JSON:
- DO NOT truncate the data array (e.g., using "// ..."). You MUST output every single data point provided in the Context.
- NEVER use null values unless explicitly provided.
- Do not suggest a separate page. Deliver the text and the JSON block together. The frontend will handle the dual rendering.
Constraint: If the query is a simple factual question (e.g., "What is the total count?"), do not generate a chart. Only visualize when there is a meaningful relationship or trend to show.
"""

        context_string = ""
        sources = []
        intent = "rag"
        params = {}

        # -----------------------------
        # 0. Intelligent Routing via LLM
        # -----------------------------
        if ocean_processor:
            print(f"🧠 Analyzing Intent for: {request.message}")
            params = await ocean_processor.extract_query_json(request.message)
            intent = params.get("intent", "rag").lower()
            
            if intent == "data":
                print(f"🌊 Routing to Ocean Data -> Extracted: {params}")
                chart_data, _ = ocean_processor.process_data(params)
                
                # Format to a readable string context
                context_string = f"Ocean Data Extract:\nVariable: {chart_data.get('variable')}\nOperation: {chart_data.get('operation')}\nRegion: {params.get('region', 'Indian Ocean')}\nYears: {params.get('start_year')} - {params.get('end_year')}\nData Points:\n"
                times = chart_data.get("times", [])
                values = chart_data.get("values", [])
                
                # Group data by year to drastically reduce context load for phi3
                yearly_data: dict[str, list] = {}
                for t, v in zip(times, values):
                    # time strings are usually "YYYY-MM-DD", taking first 4 chars
                    year = t[:4]
                    if year not in yearly_data:
                        yearly_data[year] = []
                    yearly_data[year].append(v)
                
                for year, vals in yearly_data.items():
                    avg_val = sum(vals) / len(vals)
                    context_string += f"- {year}: {avg_val:.2f}\n"

        if intent != "data" or not context_string:
            print("📚 Routing to Knowledge RAG")
            config = RAGConfig()

            # -----------------------------
            # 1. Retrieve Documents
            # -----------------------------
            retrieved_docs = pipeline.retriever.retrieve(
                query=request.message,
                top_k=config.retrieval.top_k
            )

            context_texts = [
                doc["document"].get("text", "")
                for doc in retrieved_docs
            ]

            context_string = "\n\n".join(context_texts)
            sources = retrieved_docs

        # -----------------------------
        # 2. Create Prompt
        # -----------------------------
        prompt = f"""{system_prompt}

Context:
{context_string}

Question:
{request.message}

Answer:
"""

        # -----------------------------
        # 3. Prepare Ollama Request
        # -----------------------------
        config = RAGConfig()
        ollama_url = f"{config.llm.base_url}/api/generate"

        payload = {
            "model": "phi3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 2048,   # Updated from 1024
                "temperature": 0.7
            }
        }

        print("Sending request to Ollama...")

        # -----------------------------
        # 4. Async HTTP Call
        # -----------------------------
        async with httpx.AsyncClient(timeout=300.0) as client:
            ollama_response = await client.post(
                ollama_url,
                json=payload
            )

        ollama_response.raise_for_status()

        response_data = ollama_response.json()
        generated_text = response_data.get("response", "No answer generated.")

        import re
        import json
        
        # Extract markdown JSON blocks to fulfill frontend chart UI Schema
        frontend_charts = []
        cleaned_text = generated_text
        
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', generated_text, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1))
                if parsed.get("render_chart"):
                    frontend_charts.append({
                        "type": parsed.get("chart_type", "line").strip().lower(),
                        "title": parsed.get("options", {}).get("title", "Ocean Analysis"),
                        "data": {
                            "x": [str(item.get("label", "")) for item in parsed.get("data", [])],
                            "y": [item.get("value") for item in parsed.get("data", [])]
                        }
                    })
                # Remove the extracted json block so it's visually hidden in the chat log
                cleaned_text = generated_text.replace(json_match.group(0), "").strip()
            except Exception as e:
                print(f"Error parsing generated chart JSON: {e}")

        # -----------------------------
        # 5. Return Unified Response
        # -----------------------------
        return {
            "text": cleaned_text,
            "message_type": "chart" if frontend_charts else "text",
            "charts": frontend_charts,
            "sources": sources,
            "params": params
        }

    except httpx.ReadTimeout:
        print("Timeout: Ollama took too long.")
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond."
        )

    except Exception as e:
        print("Error during chat query:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Ocean Chat Endpoint
# -----------------------------
@app.post("/ocean_chat")
async def ocean_chat_endpoint(request: ChatRequest):
    global ocean_processor

    if ocean_processor is None:
        raise HTTPException(status_code=503, detail="Ocean Processor is not available.")

    try:
        # Step 1: Use LLM to extract JSON query parameters
        params = await ocean_processor.extract_query_json(request.message)
        print(f"Extracted Ocean Params: {params}")

        # Step 2: Process Xarray Data
        chart_data, text_response = ocean_processor.process_data(params)
        
        return {
            "text": text_response,
            "chart_data": chart_data,
            "params": params
        }
    except Exception as e:
        print("Error during ocean chat query:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "server:app",   # 👈 IMPORTANT (file_name:app)
        host="0.0.0.0",
        port=8000,
        reload=True,
        timeout_keep_alive=300,
        limit_concurrency=10
    )
