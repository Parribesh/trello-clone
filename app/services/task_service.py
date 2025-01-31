from sqlalchemy.orm import Session
from app.models.Task import Task
from datetime import datetime
from app.schemas.project_schema import TaskCreate, TaskUpdate
from app.utils.kafka_producer import send_message


class TaskService:
    def __init__(self):
        pass

    def create_task(self, db: Session, task: TaskCreate):
        new_task = Task(
            title=task.title,
            description=task.description,
            stage=task.stage,
            project_id=task.project_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def get_task(self, db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    def update_task(self, db: Session, task_id: int, task: TaskUpdate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if (db_task.stage != task.stage):
            # Publish message to Kafka topic
            send_message("task-stage-changes", {
                "project_id": db_task.project_id,
                "new_stage": task.stage,
            })
        if not db_task:
            return None
        if task.title:
            db_task.title = task.title
        if task.description:
            db_task.description = task.description
        if task.stage:
            db_task.stage = task.stage
        db.commit()
        db.refresh(db_task)
        return db_task

    def delete_task(self, db: Session, task_id: int):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        db.delete(db_task)
        db.commit()
        return db_task

    def get_tasks(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Task).offset(skip).limit(limit).all()

    def get_all_tasks_by_project(self, db: Session, project_id: int):
        return db.query(Task).filter(Task.project_id == project_id).all()

    def delete_all_tasks(self, db: Session):
        tasks = db.query(Task).all()
        for task in tasks:
            db.delete(task)
        db.commit()
        return tasks
