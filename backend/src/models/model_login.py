from pydantic  import BaseModel

class Loginuse(BaseModel):
    correo: str
    clave: str