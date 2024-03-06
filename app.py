from fastapi import FastAPI
from pydantic import BaseModel  
from typing import Optional
import uvicorn
from pymongo import MongoClient

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.json'  


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mi Aplicación Flask con Swagger"
    }
)
app = FastAPI()

client = MongoClient(
    host="192.168.5.92",
    port=27017,
)
db = client["ejercicio_db"]
collection = db["personal_informacion"]

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


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