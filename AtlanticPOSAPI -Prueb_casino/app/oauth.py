# Importa las clases necesarias de FastAPI
from fastapi import Depends, HTTPException, status

# Importa los esquemas de seguridad OAuth2 para autenticación
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importa la función que se encargará de verificar el token JWT
from app.token import verify_token

# Se crea una instancia de OAuth2PasswordBearer
# Esto indica que el endpoint "/login" será utilizado para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para obtener al usuario actual autenticado usando el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Define una excepción personalizada en caso de que el token no sea válido
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # Código de error 401 (no autorizado)
        detail="Could not validate credentials",    # Mensaje de error
        headers={"WWW-Authenticate": "Bearer"},     # Cabecera requerida para autenticación Bearer
    )

    # Llama a la función verify_token pasando el token y la excepción que se lanzará si falla
    return verify_token(token, credentials_exception)
