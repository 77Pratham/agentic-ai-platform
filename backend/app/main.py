from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.planner.planner import generate_plan
import json
import asyncio
from app.state import init_db, save_execution
from app.executor import execute_plan

app = FastAPI(title="Agentic AI Backend")

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            user_message = await ws.receive_text()

            # Generate plan dynamically
            plan = generate_plan(user_message)

            # Execute plan
            result = execute_plan(plan)

            save_execution(
                exec_id=plan["plan_id"],
                plan=plan,
                current_step=len(plan["steps"]),
                status=result["status"]
            )

            await ws.send_text(json.dumps({
                "type": "execution_result",
                "data": result
            }))


    except Exception as e:
        await ws.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        await ws.close()
