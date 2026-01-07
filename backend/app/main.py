from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.planner.planner import generate_plan
import json
import asyncio
from app.executor import execute_step

app = FastAPI(title="Agentic AI Backend")

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

            # Stream steps one by one
            # Stream + execute steps
            for step in plan["steps"]:
                await ws.send_text(json.dumps({
                    "type": "step_started",
                    "data": step
                }))

                execution = execute_step(step)

                await ws.send_text(json.dumps({
                    "type": "step_result",
                    "data": execution
                }))

                if not execution["verified"]:
                    await ws.send_text(json.dumps({
                        "type": "execution_paused",
                        "reason": "verification_failed",
                        "step": step
                    }))
                    return


    except Exception as e:
        await ws.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        await ws.close()
