from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class ResponseDTO(BaseModel):
    code: int 
    message : str 
    data: object 
    
class Cat(BaseModel):
    name: str 
    id : int = 0
    aaa : str | None = None
    

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

@app.get("/error")
async def error():
    dto = ResponseDTO(
        code=0,
        message="페이지가 없습니다.",
        data=None
    )
    return JSONResponse(status_code=404, content=jsonable_encoder(dto))

@app.get("/error1")
async def error1():
    return HTTPException(status_code=404, detail={"message": "Item not found"})