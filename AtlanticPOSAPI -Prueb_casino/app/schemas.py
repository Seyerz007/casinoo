from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

# ===== Usuario: Creación y Actualización =====

class User(BaseModel):
    username: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    genero: str
    correo: EmailStr
    direccion: str
    departamento: str
    provincia: str
    distrito: str
    telefono: str
    no_pep: bool = False
    si_pep: bool = False
    regalo: Optional[str] = None
    acepta_terminos: bool
    creacion_user: datetime = datetime.now()

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[int] = None
    correo: Optional[EmailStr] = None

# ===== Usuario: Respuesta mostrada =====

class ShowUser(BaseModel):
    username: str
    nombre: str
    correo: EmailStr

    class Config:
        from_attributes = True  # Reemplazo de orm_mode para Pydantic v2

# ===== Autenticación: Login y Tokens =====

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None