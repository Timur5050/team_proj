import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from auth.utils import get_password_hash
from database import SessionLocal
from user import router as user_router
from shelter import router as shelter_router
from animal import router as animal_router
from user.models import User
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 👇 CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_superuser():
    db: Session = SessionLocal()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    user = db.query(User).filter_by(email=admin_email).first()
    if not user:
        superuser = User(
            email=admin_email,
            password=get_password_hash(admin_password),
            is_superuser=True,
        )
        db.add(superuser)
        db.commit()
        print("Superuser created")
    else:
        print("Superuser already exists")

    db.close()

app.include_router(user_router.router)
app.include_router(shelter_router.router)
app.include_router(animal_router.router)
