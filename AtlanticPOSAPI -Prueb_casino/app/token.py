from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import TokenData

# Clave secreta para firmar y verificar el token JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Algoritmo utilizado para la codificación del token
ALGORITHM = "HS256"
# Duración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Función para crear un token de acceso JWT
def create_access_token(data: dict):
    # Creamos una copia del diccionario original
    to_encode = data.copy()
    
    # Añadimos la expiración al token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Codificamos el token con la clave secreta y el algoritmo especificado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar un token JWT
def verify_token(token: str, credentials_exception):
    try:
        # Decodificamos el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Obtenemos el nombre de usuario del campo "sub"
        username: str = payload.get("sub")
        if username is None:
            # Si no hay usuario, lanzamos la excepción definida por el sistema
            raise credentials_exception
        
        # Creamos una instancia de TokenData (posiblemente para validaciones futuras)
        token_data = TokenData(username=username)
        return True
    
    # Si hay un error con el token (formato, expiración, firma inválida, etc.)
    except JWTError:
        raise credentials_exception
