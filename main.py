from fastapi import FastAPI
from pydantic import BaseModel

class Cat(BaseModel):
    name: str 
    id : int = 0
    ccc: str | None = None
    

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/first/{id}")
async def first(id : int):
    return {"id": id}

@app.get("/second")
async def second(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.post("/cat")
async def cat(cat: Cat):
    return cat