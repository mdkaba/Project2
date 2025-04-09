# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import settings (it will load from .env)
from app.core.config import settings
from app.core.database import init_models # Import DB init function
from app.core.logger import logger # Import logger

# Import API routers
from app.api.v1.endpoints import chat as chat_router_v1

# TODO: Import API routers later
# from app.api.v1.endpoints import chat

# Create FastAPI app instance
app = FastAPI(
    title="Multi-Agent Chatbot API",
    description="API for the COMP 474 Multi-Agent Chatbot System",
    version="0.1.0",
    # Adjust debug mode based on settings
    debug=settings.DEBUG 
)

# Set up CORS middleware
if settings.CORS_ORIGINS:
    logger.info(f"Setting up CORS middleware with origins: {settings.CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # List of allowed origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
        allow_headers=["*"],  # Allows all headers
        expose_headers=["*"],  # Expose all headers in response
        max_age=600,  # Cache preflight requests for 10 minutes
    )

# --- API Routers ---
logger.info(f"Including router with prefix: {settings.API_V1_PREFIX}/chat")
app.include_router(
    chat_router_v1.router, 
    prefix=f"{settings.API_V1_PREFIX}/chat", 
    tags=["Chat"]
)

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Multi-Agent Chatbot API!"}

# --- Placeholder for Startup/Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup...")
    # Initialize database models (create tables if they don't exist)
    await init_models()
    logger.info("Database models initialized.")
    # TODO: Add other startup logic if needed (e.g., load models)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # TODO: Add shutdown logic if needed (e.g., close DB connections)
    print("Application shutdown...")
    pass

# --- (Optional) Run with Uvicorn for local development ---
# This block allows running directly with `python backend/app/main.py`
# It's often preferred to run using `uvicorn backend.app.main:app --reload` from the project root
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "backend.app.main:app", 
#         host="0.0.0.0", 
#         port=8000, 
#         reload=settings.DEBUG # Enable reload only in debug mode
#     ) 