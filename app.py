from fastapi import FastAPI
from pydantic import BaseModel  
from typing import Optional
import uvicorn
from pymongo import MongoClient
from fastapi_utils.openapi import get_swagger_ui_html, get_openapi

app = FastAPI()

client = MongoClient(
    host="192.168.5.92",
    port=27017,
)
db = client["ejercicio_db"]
collection = db["personal_informacion"]


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


# Rutas para servir la documentación de Swagger
@app.get("/docs", include_in_schema=False)
async def get_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json")


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return get_openapi(app)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)