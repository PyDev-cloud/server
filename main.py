from fastapi import FastAPI
from database import Base, engine
from routes import user_routes

# ডাটাবেস টেবিল তৈরি করো
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)

@app.get("/")
def home():
    return {"message": "User API is running"}