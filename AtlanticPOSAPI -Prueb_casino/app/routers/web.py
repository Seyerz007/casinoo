# Importación de módulos y clases necesarias
from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
import aiohttp  # Cliente HTTP asíncrono para hacer peticiones a la API
from starlette.responses import RedirectResponse, Response
from app.token import verify_token  # Función para verificar el token JWT
from datetime import datetime

# Creación del router, excluido del schema de la documentación automática de FastAPI
router = APIRouter(include_in_schema=False)

# Definición del directorio donde están las plantillas HTML
templates = Jinja2Templates(directory="templates")

# URL base de la API
url = "http://localhost:8000"

# Función para obtener el usuario actual desde la cookie "access_token"
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

# Ruta principal (index)
@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta GET para mostrar el formulario de creación de usuario
@router.get("/create_user")
def create_user_get(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "msj": "",
        "type_alert": "info"
    })

# Ruta POST para procesar el formulario de creación de usuario
@router.post("/create_user")
async def create_user_post(request: Request):
    form = await request.form()

    # Validación de campos obligatorios
    required_fields = ["username", "password", "nombre", "apellido", "correo"]
    for field in required_fields:
        if not form.get(field):
            return templates.TemplateResponse("create_user.html", {
                "request": request,
                "msj": f"El campo '{field}' es obligatorio.",
                "type_alert": "danger"
            })

    # Construcción del diccionario de datos del usuario
    usuario = {
        "username": form.get('username'),
        "password": form.get('password'),
        "nombre": form.get('nombre'),
        "apellido": form.get('apellido'),
        "correo": form.get('correo'),
        "direccion": form.get('direccion'),
        "telefono": form.get('telefono'),
        "tipo_documento": form.get('tipo_documento'),
        "numero_documento": form.get('numero_documento'),
        "fecha_nacimiento": form.get('fecha_nacimiento'),
        "genero": form.get('genero'),
        "departamento": form.get('departamento'),
        "provincia": form.get('provincia'),
        "distrito": form.get('distrito'),
        "no_pep": form.get('no_pep') == 'on',
        "si_pep": form.get('si_pep') == 'on',
        "regalo": form.get('regalo'),
        "acepta_terminos": form.get('acepta_terminos') == 'on',
        "creacion_user": datetime.now().isoformat()
    }

    # URL de la API para registrar al usuario
    url_post = f"{url}/user/"

    try:
        # Se realiza la petición POST a la API para crear el usuario
        async with aiohttp.ClientSession() as session:
            response = await session.post(url_post, json=usuario)
            print(await response.text())  # Para debug
            response_json = await response.json()
    except Exception as e:
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "msj": f"Error al conectar con la API: {e}",
            "type_alert": "danger"
        })

    # Validación de la respuesta
    if "username" in response_json:
        msj = "Usuario creado satisfactoriamente."
        type_alert = "primary"
    else:
        msj = response_json.get("detail", "Usuario no fue creado.")
        type_alert = "danger"

    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "msj": msj,
        "type_alert": type_alert
    })

# Ruta para cerrar sesión (eliminar cookie del token y redirigir)
@router.get("/salir")
def salir(response: Response, request: Request):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response

# Ruta GET para mostrar el formulario de login
@router.get("/login_web")
def login_web(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "msj": ""})

# Ruta POST para procesar el login
@router.post("/login_web")
async def login_web(response: Response, request: Request):
    form = await request.form()

    rol = form.get('rol')  # Rol del usuario (admin, vendedor, etc.)
    username = form.get('username')
    password = form.get('password')

    usuario = {
        "username": username,
        "password": password
    }

    url_post = f"{url}/login/"

    try:
        # Petición POST al endpoint de login para obtener el token
        async with aiohttp.ClientSession() as session:
            response = await session.post(url_post, data=usuario)
            response_json = await response.json()
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "msj": f"Error de conexión: {e}"
        })

    # Validación de credenciales
    if 'access_token' not in response_json:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "msj": "Usuario o contraseña incorrecto"
        })

    # Si el rol es administrador o sistemas, mostrar lista de usuarios
    if rol in ["administrador", "sistemas"]:
        try:
            async with aiohttp.ClientSession() as session:
                usuarios_response = await session.get(f"{url}/user/")
                usuarios = await usuarios_response.json()
        except Exception as e:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "msj": f"Error obteniendo usuarios: {e}"
            })

        return templates.TemplateResponse("login.html", {
            "request": request,
            "usuarios": usuarios,
            "msj": f"Bienvenido, {rol.capitalize()}!",
            "type_alert": "primary"
        })

    # Si es otro rol (ej. vendedor), redirigir al index y guardar el token en una cookie
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=response_json["access_token"])
    return response

# Ruta para mostrar usuarios (solo si está autenticado)
@router.get("/mostrar_usuarios")
def mostrar_usuarios(request: Request, current_user=Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse("mostrar_usuarios.html", {
            "request": request,
            "msj": ""
        })
    return RedirectResponse("/", status_code=302)
