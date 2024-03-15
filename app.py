import json
from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from fastapi.openapi.utils import get_openapi
from bson import ObjectId, json_util
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

load_dotenv()

HOST_MongoDB = os.getenv('HOST_MongoDB')
PORT_MongoDB = os.getenv('PORT_MongoDB')

client = MongoClient(host=HOST_MongoDB, port=int(PORT_MongoDB))

db = client["ejercicio_db"]
collection = db["PersonalInformation"]

@app.get("/documents")
async def get_all_documents():
    documents = collection.find({})
    serialized_documents = json_util.dumps(documents)
    json_legible = json.loads(serialized_documents)
    return json_legible

@app.get("/documents/byid/")
def get_document_by_id(id: str):
    document = collection.find_one({"_id": ObjectId(id)})
    serialized_document = json_util.dumps(document)
    json_legible = json.loads(serialized_document)
    return json_legible

@app.get("/documents/{tipo_documento}")
def get_document_by_tipo(tipo_documento: str):
    document = collection.find({"tipoDocumento": tipo_documento})
    serialized_document = json_util.dumps(document)
    json_legible = json.loads(serialized_document)
    return json_legible

# Rutas para servir la documentación de Swagger
@app.get("/docs", include_in_schema=False)
async def get_swagger_html():
    return app.swagger_ui_html

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(app)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
