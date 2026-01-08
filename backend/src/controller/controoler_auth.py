from  passlib.context import CryptContext
from src.database.conexion import get_connection
from fastapi import HTTPException
import os
from jose import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta

#carga el .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

#crea un contexto para poder tomar la clave en texto plano y poder encriptar mas abajo
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False
)
#trae la clave en texto plano
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#verifica la clave para encriptarla
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)





#crea el token para el login rrecibe el correo y id
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def login(correo: str, clave: str):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        cursor.execute("select*from usuarios where correo=%s",(correo,))
        data= cursor.fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail="USER NO ENCONTRADO")
        
        paswoord=data[3]

        if not verify_password(clave, paswoord):
            raise HTTPException(status_code=404, detail="Credenciales incorrectas")
        #si no ingresan lass credenciales correctas cierra el proceso
        cursor.close()
        connection.close()
        #se crea el token paera cad user si ingresa las credenciales correctas
        token = create_access_token({"correo": correo, "id": data[0]})
        return {
            "mensaje": "Exitoso",
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
