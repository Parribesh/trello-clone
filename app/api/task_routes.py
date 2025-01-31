import json
import asyncio
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, WebSocket
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db
from app.schemas.project_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()

task_service = TaskService()


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db=db, task=task)


@router.get("/{project_id}", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), project_id: int = None):
    tasks = task_service.get_all_tasks_by_project(db=db, project_id=project_id)
    return tasks


@router.get("/", response_model=List[TaskResponse])
def read_all_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = task_service.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

# @router.get("/{task_id}", response_model=TaskResponse)
# def read_task(task_id: int, db: Session = Depends(get_db)):
#     db_task = task_service.get_task(db=db, task_id=task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_service.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_service.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/", response_model=List[TaskResponse])
def delete_all_tasks(db: Session = Depends(get_db)):
    tasks = task_service.delete_all_tasks(db=db)
    return tasks


clients = set()  # Keep track of connected WebSockets


async def consume_kafka():
    """ Continuously fetch messages from Kafka asynchronously and broadcast to WebSockets. """
    consumer = AIOKafkaConsumer(
        "task-stage-changes",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="websocket-consumer-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            task_update = message.value
            print(f"Received message from Kafka: {task_update}")
            for client in clients:
                print(f"Sending message to WebSocket: {
                      task_update}, client: {client}")
                await client.send_json(task_update)
    finally:
        await consumer.stop()


@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            # Wait for more messages
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Ensure to stop the Kafka consumer and close the WebSocket
        clients.remove(websocket)
        await websocket.close()


@router.on_event("startup")
async def startup_event():
    """ Start the Kafka consumer when the app starts. """
    asyncio.create_task(consume_kafka())
