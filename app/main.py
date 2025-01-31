from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.ws_routes import router as ws_router
from app.api.user_routes import router as user_router
from app.api.project_routes import router as project_router
from app.api.task_routes import router as task_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()
# Define the allowed origins (you can use '*' to allow all origins, but it's recommended to be specific)
origins = [
    "*",  # Allow all origins
    "http://localhost:3000",  # Allow React frontend (or any other domain)
    "https://example.com",    # Allow another example domain (for production)
]

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specified origins
    allow_credentials=True,  # Allow cookies and authentication
    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers
)


# Include the WebSocket routes and other API routes
app.include_router(ws_router, prefix="/api")

# Include websocket routes
app.include_router(user_router, prefix="/api/auth")
# Optional: Serve static files (e.g., if you want to serve a frontend)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# You can define other routes here, for example:
app.include_router(project_router, prefix="/api/projects")
app.include_router(task_router, prefix="/api/tasks")


@app.get("/")
async def root():
    return {"message": "Welcome to the Trello-like application API!"}

# Start the app by running this file:
# uvicorn main:app --reload
