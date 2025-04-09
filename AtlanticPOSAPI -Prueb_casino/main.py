from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from pathlib import Path
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db.database import Base, engine
from app.routers import user, auth, web

# Cargar variables de entorno
load_dotenv()

# Creación de la aplicación FastAPI
app = FastAPI()

# Configuración de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de templates
templates = Jinja2Templates(directory="templates")

# Creación de tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# Incluir routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(web.router)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
# Rutas de la aplicación
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create_user", response_class=HTMLResponse)
def mostrar_registro(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "msj": "",
        "type_alert": "info"
    })

# Punto de entrada principal
if __name__ == "__main__":
    create_tables()  # Asegurar que las tablas existen antes de iniciar
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)