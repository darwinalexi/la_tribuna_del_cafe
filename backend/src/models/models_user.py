from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Form

class User(BaseModel):
    identificacion: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=50)
    correo: Optional[str]=None
    clave: Optional[str]=None
    edad: Optional [int]= None
    descripcion: Optional[str]=None
    rol: Optional[str]=None
   #debe ir para poder ver archivos en caso de que se quieran agregar archivos 
    @classmethod
    def as_form(
        cls,
        identificacion: int = Form(...),
        nombre: Optional [str] = Form(None),
        correo: Optional[str] = Form(None),
        clave: Optional[str] = Form(None),
        edad: Optional[int] = Form(None),
        descripcion: Optional[str] = Form(None),
        rol: Optional[str] = Form(None)
    ):
        return cls(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
            clave=clave,
            edad=edad,
            descripcion=descripcion,
            rol=rol
        )