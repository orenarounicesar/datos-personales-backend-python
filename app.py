from fastapi import FastAPI
from pydantic import BaseModel  
from typing import Optional
import uvicorn
from pymongo import MongoClient

app = FastAPI()

client = MongoClient(
    host="mongodb",
    port=27017,
    username='root',
    password='pass', 
    authSource="admin"
)
db = client["testdb"]
collection = db["users"]


class User(BaseModel):
    id: Optional[int]
    tipoDocumento: str
    documento: str
    nombre1: str
    nombre2: str
    apellido1: str
    apellido2: str
    fechaNacimiento: str
    sexo: str

@app.get("/documents/", response_model=list[User])
def get_all_documents():
    documents = collection.find()
    return documents


@app.get("/documents/{tipo_documento}", response_model=User)
def get_document_by_tipo(tipo_documento: str):
    document = collection.find_one({"tipoDocumento": tipo_documento})
    return document


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)