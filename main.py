from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

class ResponseDTO(BaseModel):
    code: int 
    message : str 
    data: object 
    
class Cat(BaseModel):
    name: str 
    id : int = 0
    aaa : str | None = None

class RequestInsertRegionDTO(BaseModel):
    regionName: str
    
class RequestUpdateRegionDTO(BaseModel):
    regionName: str
    

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database("sqlite:C:\programming\sqllit\hr")



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

@app.post("/files/")
async def check_file(
    uploadFile: UploadFile = File(), token: str = Form()
):
    return{
        "token": token,
        # "uploadFileSize": len(await upload_file.read()),
        "uploadFileName": uploadFile.filename,
        "uploadFileContentType": uploadFile.content_type
    }

@app.get("/findall")
async def fetch_data():

    await database.connect()

    query = "SELECT * FROM REGIONS"
    results = await database.fetch_all(query=query)

    await database.disconnect()

    return results

@app.post("/insert")
async def insert_data(requestInsertRegionDTO: RequestInsertRegionDTO):

    await database.connect()
    error = False
     
    try:
        query = f"""INSERT INTO REGIONS
                      (region_name)
                    values
                      ('{requestInsertRegionDTO.regionName}')"""
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"
    return results

@app.put("/update/{id}")
async def update_data(id : int, requestUpdateRegionDTO: RequestUpdateRegionDTO):

    await database.connect()
    error = False
    
    try:
        query = f"""UPDATE REGIONS  SET REGION_NAME =
                        "{requestUpdateRegionDTO.regionName}" 
                    WHERE REGION_ID = "{id}" """
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"
    return results

@app.delete("/delete/{id}")
async def update_data(id : int):

    await database.connect()
    error = False
    
    try:
        query = f"""DELETE FROM REGIONS WHERE REGION_ID = "{id}" """
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"
    return results