# Importaciones necesarias
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, HTTPException, status
from app.db import models                  # Modelos ORM (User)
from app.db.database import get_db         # Función para obtener una sesión de base de datos
from app.hashing import Hash               # Clase para hashear contraseñas
from app.schemas import User, ShowUser, UpdateUser  # Esquemas Pydantic para validación

# Creación del router
router = APIRouter()

# Crear un nuevo usuario
@router.post("/", response_model=ShowUser)
def create_user(user: User, db: Session = Depends(get_db)):
    # Verifica si el username ya existe en la base de datos
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso."
        )

    try:
        # Crea un nuevo objeto de usuario
        nuevo_usuario = models.User(
            username=user.username,
            password=Hash.hash_password(user.password),  # Se hashea la contraseña antes de guardar
            nombre=user.nombre,
            apellido=user.apellido,
            tipo_documento=user.tipo_documento,
            numero_documento=user.numero_documento,
            fecha_nacimiento=user.fecha_nacimiento,
            genero=user.genero,
            correo=user.correo,
            direccion=user.direccion,
            departamento=user.departamento,
            provincia=user.provincia,
            distrito=user.distrito,
            telefono=user.telefono,
            no_pep=user.no_pep,
            si_pep=user.si_pep,
            regalo=user.regalo,
            acepta_terminos=user.acepta_terminos
        )
        db.add(nuevo_usuario)      # Agrega el usuario a la sesión
        db.commit()                # Confirma los cambios en la base de datos
        db.refresh(nuevo_usuario) # Actualiza el objeto con los datos persistidos (como el ID generado)
        return nuevo_usuario
    except Exception as e:
        print(f"Error al crear usuario: {e}")  # Para debug (puede reemplazarse por logs)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario. Verifica los datos ingresados."
        )

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=ShowUser)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    return usuario

# Eliminar un usuario por ID
@router.delete("/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}, por lo tanto no se elimina"
        )
    usuario.delete(synchronize_session=False)  # Elimina el usuario
    db.commit()                                # Guarda los cambios
    return {"respuesta": "Usuario eliminado correctamente."}

# Obtener todos los usuarios
@router.get("/", response_model=list[ShowUser])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Actualizar un usuario por ID
@router.put("/{user_id}")
def actualizar_user(user_id: int, updateUser: UpdateUser, db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    # Actualiza solo los campos proporcionados en la solicitud
    usuario.update(updateUser.dict(exclude_unset=True))
    db.commit()
    return {"respuesta": "Usuario actualizado correctamente."}
