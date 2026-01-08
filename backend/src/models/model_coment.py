from pydantic import BaseModel

class Coment(BaseModel):
    id : int | None = None
    comentario:str
    calificacion: int
    id_usuario:int
