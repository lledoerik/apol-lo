from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import Base, engine

from .common.apiResponse import APIResponse
from fastapi.responses import JSONResponse

from .api.routers.authRoutes import router as authRouter
from .api.routers.analyzeRoutes import router as analyzrouter
from .api.routers.userRoutes import router as userRouter
from .api.routers.feedbackRoutes import router as feedbackRouter
from .api.routers.moodEntryRoutes import router as moodEntryRouter
from .database.dbInitializer import initialize_database

# Importar entitats per crear taules
from .models.entities.userEntity import User
from .models.entities.feedbackEntity import SentimentFeedback
from .models.entities.moodEntryEntity import MoodEntry

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(title="Apol·lo - Diari Emocional", lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse.error(
            message=exc.detail,
            code=exc.status_code
        ).model_dump()
    )

from .config import settings

# CORS: permet localhost per dev i la URL de producció
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if settings.FRONTEND_URL:
    allowed_origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(authRouter)
app.include_router(analyzrouter)
app.include_router(userRouter)
app.include_router(feedbackRouter)
app.include_router(moodEntryRouter)

# create tables for dev
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status": "ok", "app": "Apol·lo API"}
