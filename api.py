from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from routers import audio_router, news_router, text_router, frontend_router

app = FastAPI(
    title="campaign-generator-api",
    version="0.0.1",
    description="General API for the campaign generator.",
    contact={
        "email": "contact@jamestwose.com",
    },
    # lifespan=lifespan,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio_router.router)
app.include_router(frontend_router.router)
app.include_router(news_router.router)
app.include_router(text_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Campaign Generator API!"}