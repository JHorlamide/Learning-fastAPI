from fastapi import FastAPI

from storeapi.routers.post import router as posts_router

app = FastAPI()
app.include_router(posts_router)
