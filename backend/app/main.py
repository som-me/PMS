from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routers import auth, projects, tasks
from app import models
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PMS API", docs_url="/docs", redoc_url="/redoc")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pmsfront.netlify.app",  # ✅ fixed
        "http://localhost:3000"          # for local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is live!"}

@app.get("/api/auth/test")
def test():
    return {"message": "Backend connection successful!"}
