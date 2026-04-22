from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

try:
    with open("productos.json", "r") as f:
        productos = json.load(f)
except:
    productos = []

def calcular_datos(producto):
    total = producto["valoru"] * producto["existencias"]

    if producto["existencias"] < 50:
        estado = "Bajo"
    elif 50 <= producto["existencias"] <= 100:
        estado = "Medio"
    else:
        estado = "Alto"

    producto["total"] = total
    producto["estado"] = estado
    return producto

@app.get("/")
def mostrar_tabla(request: Request):
    productos_calculados = [calcular_datos(p.copy()) for p in productos]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"productos": productos_calculados}
    )