# Importaciones necesarias
from sqlalchemy.orm import Session 
from app.db import models                      # Modelos ORM
from fastapi import HTTPException, status 
from app.hashing import Hash                   # Utilidad para hashear/verificar contraseñas
from fastapi import APIRouter, Depends
from app.db.database import get_db             # Sesión de base de datos
from app.schemas import User, UpdateUser, ShowUser  # Esquemas de entrada/salida

# Función para crear un nuevo usuario
def crear_usuario(usuario, db: Session):
    usuario = usuario.dict()  # Convierte el objeto Pydantic a diccionario

    # Validaciones para evitar duplicados en campos clave
    if db.query(models.User).filter(models.User.username == usuario["username"]).first():
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe.")

    if db.query(models.User).filter(models.User.correo == usuario["correo"]).first():
        raise HTTPException(status_code=409, detail="El correo ya está registrado.")

    if db.query(models.User).filter(models.User.numero_documento == usuario["numero_documento"]).first():
        raise HTTPException(status_code=409, detail="El número de documento ya está registrado.")

    try:
        # Se crea una nueva instancia del modelo con los datos del usuario
        nuevo_usuario = models.User(
            username=usuario["username"],
            password=Hash.hash_password(usuario["password"]),  # Se encripta la contraseña
            nombre=usuario["nombre"],
            apellido=usuario["apellido"],
            tipo_documento=usuario["tipo_documento"],
            numero_documento=usuario["numero_documento"],
            fecha_nacimiento=usuario["fecha_nacimiento"],
            genero=usuario["genero"],
            correo=usuario["correo"],
            direccion=usuario["direccion"],
            departamento=usuario["departamento"],
            provincia=usuario["provincia"],
            distrito=usuario["distrito"],
            telefono=usuario["telefono"],
            no_pep=usuario.get("no_pep", False),  # Por defecto False si no se envía
            si_pep=usuario.get("si_pep", False),
            regalo=usuario.get("regalo"),
            acepta_terminos=usuario.get("acepta_terminos", False)
        )
        db.add(nuevo_usuario)       # Se agrega el usuario a la sesión
        db.commit()                 # Se guarda en la base de datos
        db.refresh(nuevo_usuario)  # Se refresca para obtener el ID generado, etc.
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear el usuario: {e}"
        )

# Definición de router (aunque no se usa explícitamente aquí)
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Obtener usuario por ID
def obtener_usuario(user_id, db: Session):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    return usuario

# Eliminar usuario por ID
def eliminar_usuario(user_id, db: Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}, por lo tanto no se elimina"
        )
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Usuario eliminado correctamente!"}

# Obtener todos los usuarios
def obtener_usuarios(db: Session):
    data = db.query(models.User).all()
    return data

# Actualizar información de un usuario
def actualizar_user(user_id, updateUser, db: Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    usuario.update(updateUser.dict(exclude_unset=True))  # Solo actualiza campos enviados
    db.commit()
    return {"respuesta": "Usuario actualizado correctamente!"}
