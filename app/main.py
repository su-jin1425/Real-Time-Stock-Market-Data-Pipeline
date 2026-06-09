from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.stocks import router as stocks_router
from app.api.analytics import router as analytics_router
from app.api.monitoring import router as monitoring_router
from app.api.pipelines import router as pipelines_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(stocks_router, prefix=f"{settings.API_V1_STR}/stocks", tags=["stocks"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(monitoring_router, prefix=f"{settings.API_V1_STR}/monitoring", tags=["monitoring"])
app.include_router(pipelines_router, prefix=f"{settings.API_V1_STR}/pipelines", tags=["pipelines"])


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/monitoring/health")
def health_check():
    return {"status": "ok"}
