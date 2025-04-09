# Importa el contexto de cifrado de la librería passlib
from passlib.context import CryptContext

# Crea un contexto de cifrado con el esquema bcrypt
# bcrypt es un algoritmo de hashing robusto utilizado para almacenar contraseñas de forma segura
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clase auxiliar para manejar el hash y la verificación de contraseñas
class Hash():
    
    # Método para hashear una contraseña en texto plano
    def hash_password(password):
        # Retorna la contraseña hasheada usando bcrypt
        return pwd_context.hash(password)
    
    # Método para verificar si una contraseña en texto plano coincide con su versión hasheada
    def verify_password(plain_password, hashed_password):
        # Compara la contraseña ingresada con la almacenada (hasheada)
        return pwd_context.verify(plain_password, hashed_password)
