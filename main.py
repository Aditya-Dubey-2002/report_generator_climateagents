# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from langgraph_sdk import get_client
# import json
# import asyncio
# import os

# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# # Initialize langgraph client
# url_for_cli_deployment = "https://iscc-eu-report-image-817520027812.us-central1.run.app"
# client = get_client(url=url_for_cli_deployment)

# class UserInput(BaseModel):
#     message: str
#     thread_id: str = None

# @app.get("/")
# async def read_root():
#     return FileResponse("app/static/index.html")

# @app.post("/create_thread")
# async def create_thread():
#     thread = await client.threads.create()
#     return {"thread_id": thread["thread_id"]}

# @app.websocket("/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
    
#     try:
#         while True:
#             # Receive message from client
#             data = await websocket.receive_text()
#             data = json.loads(data)
            
#             thread_id = data.get("thread_id")
#             message = data.get("message")
            
#             config = {"configurable": {"user_id": "Test"}}
#             graph_name = "retrieval_graph"

#             if message == ".":
#                 # Initial run
#                 async for chunk in client.runs.stream(
#                     thread_id,
#                     graph_name,
#                     input={"input_data": "."},
#                     config=config,
#                     interrupt_before=["human_edit"],
#                     stream_mode="messages-tuple"
#                 ):
#                     if chunk.event == "messages":
#                         response = "".join(data_item['content'] for data_item in chunk.data if 'content' in data_item)
#                         await websocket.send_text(response)
#             else:
#                 # Get current thread state
#                 thread_state = await client.threads.get_state(thread_id)
#                 current_human_messages = thread_state['values'].get('human_messages', [])
                
#                 # Create new human message
#                 new_human_message = {
#                     "content": message,
#                     "role": "human"
#                 }
                
#                 # Update messages
#                 updated_human_messages = current_human_messages + [new_human_message]
                
#                 # Update thread state
#                 forked_config = await client.threads.update_state(
#                     thread_id,
#                     {"human_messages": updated_human_messages}
#                 )
                
#                 # Continue the run
#                 async for chunk in client.runs.stream(
#                     thread_id,
#                     graph_name,
#                     input=None,
#                     config=config,
#                     checkpoint_id=forked_config['checkpoint_id'],
#                     interrupt_before=["human_edit"],
#                     stream_mode="messages-tuple"
#                 ):
#                     if chunk.event == "messages":
#                         response = "".join(data_item['content'] for data_item in chunk.data if 'content' in data_item)
#                         await websocket.send_text(response)
                        
#     except Exception as e:
#         print(f"Error: {e}")
#         await websocket.close()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langgraph_sdk import get_client
import json
import asyncio
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize langgraph client
url_for_cli_deployment = "https://iscc-eu-report-image-817520027812.us-central1.run.app"
client = get_client(url=url_for_cli_deployment)

class UserInput(BaseModel):
    message: str
    thread_id: str = None

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

@app.post("/create_thread")
async def create_thread():
    thread = await client.threads.create()
    return {"thread_id": thread["thread_id"]}

async def handle_initial_message(websocket: WebSocket, thread_id: str):
    config = {"configurable": {"user_id": "Test"}}
    graph_name = "retrieval_graph"
    
    async for chunk in client.runs.stream(
        thread_id,
        graph_name,
        input={"input_data": "."},
        config=config,
        interrupt_before=["human_edit"],
        stream_mode="messages-tuple"
    ):
        if chunk.event == "messages":
            response = "".join(data_item['content'] for data_item in chunk.data if 'content' in data_item)
            await websocket.send_text(response)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    initial_message_handled = False
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            data = json.loads(data)
            
            thread_id = data.get("thread_id")
            message = data.get("message")
            
            config = {"configurable": {"user_id": "Test"}}
            graph_name = "retrieval_graph"

            if message == "." and not initial_message_handled:
                # Handle initial message outside the main loop
                await handle_initial_message(websocket, thread_id)
                initial_message_handled = True
                continue

            # Get current thread state
            thread_state = await client.threads.get_state(thread_id)
            current_human_messages = thread_state['values'].get('human_messages', [])
            
            # Create new human message
            new_human_message = {
                "content": message,
                "role": "human"
            }
            
            # Update messages
            updated_human_messages = current_human_messages + [new_human_message]
            
            # Update thread state
            forked_config = await client.threads.update_state(
                thread_id,
                {"human_messages": updated_human_messages}
            )
            
            # Continue the run
            async for chunk in client.runs.stream(
                thread_id,
                graph_name,
                input=None,
                config=config,
                checkpoint_id=forked_config['checkpoint_id'],
                interrupt_before=["human_edit"],
                stream_mode="messages-tuple"
            ):
                if chunk.event == "messages":
                    response = "".join(data_item['content'] for data_item in chunk.data if 'content' in data_item)
                    await websocket.send_text(response)
                    
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)