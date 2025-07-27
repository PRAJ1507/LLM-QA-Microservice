from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
import logging
import time

from app.routes import documents, questions

# ------------------------
# Logging Configuration
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ------------------------
# FastAPI App
# ------------------------
app = FastAPI()

# Add routers
app.include_router(documents.router)
app.include_router(questions.router)

logger.info("🚀 FastAPI application initialized")

# ------------------------
# Middleware: Log All Requests
# ------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} [{duration:.2f}s]")
    return response

# ------------------------
# Middleware: Catch & Log Unhandled Exceptions
# ------------------------
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled exception: {exc}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(exc)},
        )

# ------------------------
# Startup & Shutdown Events
# ------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("✅ App startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 App shutdown")
