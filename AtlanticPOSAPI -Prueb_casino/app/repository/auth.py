# Importaciones necesarias
from sqlalchemy.orm import Session 
from app.db import models                        # Modelos de base de datos
from fastapi import HTTPException, status       # Manejo de errores HTTP
from app.hashing import Hash                    # Utilidad para verificar contraseñas
from app.token import create_access_token       # Función para generar token JWT

# Función de autenticación de usuario
def auth_user(usuario, db: Session):
    # Buscar usuario en la base de datos por username
    user = db.query(models.User).filter(models.User.username == usuario.username).first()

    # Si no existe el usuario, lanzar una excepción
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""No existe el usuario con el username {usuario.username} por lo tanto no se realiza el login"""
        )
    
    # Verificar si la contraseña ingresada es válida comparada con la almacenada (hasheada)
    if not Hash.verify_password(usuario.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""¡Contraseña incorrecta!"""
        )

    # Si la autenticación es exitosa, generar un token JWT
    access_token = create_access_token(
        data={"sub": usuario.username}  # El "sub" suele representar al sujeto del token (el usuario)
    )

    # Retornar el token y el tipo (Bearer es estándar para OAuth2)
    return {"access_token": access_token, "token_type": "bearer"}
