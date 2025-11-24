from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import appointments, applications, caregivers, families, job_posts, messages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Caregivers Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(caregivers.router)
app.include_router(families.router)
app.include_router(job_posts.router)
app.include_router(applications.router)
app.include_router(appointments.router)
app.include_router(messages.router)


@app.get("/")
def read_root():
    return {"message": "Caregivers Platform API is running"}
