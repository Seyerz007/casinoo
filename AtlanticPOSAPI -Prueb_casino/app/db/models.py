from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

# Modelo de tabla para el usuario
class User(Base):
    __tablename__ = "usuario"  # Nombre de la tabla en la base de datos

    # Campos de la tabla usuario
    id = Column(Integer, primary_key=True, index=True)  # ID único del usuario
    username = Column(String(50), unique=True, nullable=False)  # Nombre de usuario único
    password = Column(String(255), nullable=False)  # Contraseña (encriptada)
    nombre = Column(String(100), nullable=False)  # Nombre personal
    apellido = Column(String(100), nullable=False)  # Apellido
    tipo_documento = Column(String(20), nullable=False)  # Tipo de documento (DNI, Pasaporte, etc.)
    numero_documento = Column(String(20), unique=True, nullable=False)  # Número de documento único
    fecha_nacimiento = Column(Date, nullable=False)  # Fecha de nacimiento
    genero = Column(String(20), nullable=False)  # Género (masculino, femenino, otro)
    correo = Column(String(100), unique=True, nullable=False)  # Correo electrónico único
    direccion = Column(String(255), nullable=False)  # Dirección del usuario
    departamento = Column(String(50), nullable=False)  # Departamento geográfico
    provincia = Column(String(50), nullable=False)  # Provincia geográfica
    distrito = Column(String(50), nullable=False)  # Distrito geográfico
    telefono = Column(String(20), nullable=False)  # Número de teléfono
    no_pep = Column(Boolean, default=False)  # Declaración PEP (persona políticamente expuesta) - No
    si_pep = Column(Boolean, default=False)  # Declaración PEP - Sí
    regalo = Column(String(50), nullable=True)  # Campo opcional para regalo u oferta
    acepta_terminos = Column(Boolean, default=False)  # Indica si aceptó términos y condiciones

    # Relación con la tabla Venta (uno a muchos)
    ventas = relationship("Venta", back_populates="usuario", cascade="all, delete-orphan")
    # Si se elimina el usuario, se eliminan automáticamente sus ventas

# Modelo de tabla para las ventas
class Venta(Base):
    __tablename__ = "venta"  # Nombre de la tabla en la base de datos

    # Campos de la tabla venta
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID de la venta
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))  # FK al usuario (con eliminación en cascada)
    venta = Column(Integer)  # Cantidad total de venta (puede ser monto o unidades)
    ventas_productos = Column(Integer)  # Número de productos en la venta

    # Relación inversa con el usuario
    usuario = relationship("User", back_populates="ventas")
