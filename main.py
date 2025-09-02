from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from routers.bed_alot import router as bed_router
from dotenv import load_dotenv
import os
from starlette.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
Front_URL = os.getenv("Front_URL")


if not API_KEY:
    raise RuntimeError("API_KEY not set in .env file")

# Define API key security scheme for OpenAPI (Swagger UI)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

app = FastAPI(
    title="KK Hospital Backend API",
    description="Backend API for KK Hospital",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Key validation function
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: Invalid API Key"
        )
    return api_key


# Root endpoint (no authentication required)
@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to the KK Hospital Backend API. For documentation, please refer to /docs."})


# Include routers with API key dependency
app.include_router(bed_router, dependencies=[Depends(get_api_key)])



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway sets PORT env
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)