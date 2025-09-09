from fastapi import FastAPI
from database import Base, engine
from routes import user_routes, instalment_routes, auth_router, payment_routers,ledger_routers
from fastapi.middleware.cors import CORSMiddleware

# ডাটাবেস টেবিল তৈরি
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS সেটআপ
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Alternative localhost format
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include
app.include_router(user_routes.router)
app.include_router(instalment_routes.router)
app.include_router(auth_router.router)
app.include_router(payment_routers.router)
app.include_router(ledger_routers.router)

@app.get("/")
def home():
    return {"message": "User API is running"}
