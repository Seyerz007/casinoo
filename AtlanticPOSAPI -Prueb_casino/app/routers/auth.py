# Importaciones necesarias
from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session 
from typing import List
from app.db.database import get_db                 # Función para obtener una sesión de base de datos
from app.schemas import Login                      # (Podría no ser usada aquí directamente, revisar)
from app.repository import auth                    # Lógica de autenticación en un archivo externo
from fastapi.security import OAuth2PasswordRequestForm  # Clase para manejar login estilo OAuth2

# Se crea un router con el prefijo "/login" y una etiqueta "Login"
router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

# Ruta POST para iniciar sesión
@router.post('/', status_code=status.HTTP_200_OK)
def login(usuario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Se llama a la función `auth_user` dentro del repositorio `auth`, la cual maneja la validación del usuario
    auth_token = auth.auth_user(usuario, db)
    
    # Devuelve el token generado si las credenciales son válidas
    return auth_token
