from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from enum import Enum
from jose import jwt
from typing import Optional

app = FastAPI()

items =[ 
        {"name": "pc", "preis": 1000, "typ": "hardware"},
        {"name": "montior", "preis": 200, "typ": "hardware"},
        {"name": "tastatur", "preis": 70, "typ": "hardware"},
        {"name": "cod", "preis": 90, "typ": "software"},
]

class Type(Enum):
    hardware = "hardware"
    software = "software"

class Item(BaseModel):
    name: str
    preis: int = Field(100, gt=0, lt=10000)
    typ: Type

class ResponseItem(BaseModel):
    name: str
    typ: Type

schema = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login/")
async def login(data: OAuth2PasswordRequestForm=Depends()):
    if data.username and data.password == "test":
        acces_token = jwt.encode({"user": data.username}, key="secret")
        return {"acces_token": acces_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/items/")
async def hello(q: Optional[str]=None):
    if q:
        data = []
        for item in items:
            if item.get("typ") == q:
                data.append(item)
        return data

@app.get("/items/{item_id}",  dependencies=[Depends(schema)])
async def get_item(item_id: int):
    return items[item_id]

@app.post("/create_item", response_model=ResponseItem,  dependencies=[Depends(schema)])
async def create_item(data: Item):
    items.append(data)
    return data

@app.put("/items/{item_id}",  dependencies=[Depends(schema)])
async def change_item(item_id: int, item: Item):
    items[item_id] = item
    return item

@app.delete("/items/{item_id}",  dependencies=[Depends(schema)])
async def delete_item(item_id: int):
    item = items[item_id]
    items.pop(item_id)
    return {"deleted": item}

