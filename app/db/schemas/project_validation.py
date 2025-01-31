from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ProjectStage(str, Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Task(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    stage: ProjectStage

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    tasks: List[Task] = []

# Example usage
example_task = Task(id=1, name="Design Database", stage=ProjectStage.TODO)
example_project = Project(id=1, name="New Website", tasks=[example_task])
print(example_project)