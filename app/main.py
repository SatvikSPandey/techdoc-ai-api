import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.rate_limiter import limiter
from app.api.routes import health, summarize, ask
from app.utils.logger import logger

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info("Request", extra={
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "ms": round((time.time() - start) * 1000, 2),
    })
    return response


from app.api.routes import health, summarize, ask, metrics

app.include_router(health.router,    prefix="/api/v1")
app.include_router(summarize.router, prefix="/api/v1")
app.include_router(ask.router,       prefix="/api/v1")
app.include_router(metrics.router,   prefix="/api/v1")


@app.get("/", tags=["System"])
async def root():
    return {"name": settings.app_name, "docs": "/docs", "health": "/api/v1/health"}


@app.on_event("startup")
async def on_startup():
    logger.info("API started", extra={"backend": settings.ai_backend})