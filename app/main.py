from fastapi import FastAPI

from database.db_config import engine
from models import user as models
from routers import user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Routers
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, log_level="info", reload=True
    )
