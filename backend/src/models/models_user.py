from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class User(BaseModel):
    identificacion:int | None=None
    nombre: str | None=None
    correo: str | None=None
    clave: str | None=None
    edad: int | None=None
    descripcion: str | None=None
    rol: str | None=None
    estado: str | None=None
   #debe ir para poder ver archivos en caso de que se quieran agregar archivos 
    @classmethod
    def create_form(
        cls,
        identificacion: int = Form(...),
        nombre: str = Form(...),
        correo: str = Form(...),
        clave: str  = Form(...),
        edad: int = Form(...),
        descripcion: str = Form(...),
        rol: str = Form(...),
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
    
    @classmethod
    def update_form(
        cls,
        nombre: Optional [str] = None,
        correo: Optional[str] = None,
        clave: Optional[str] = None,
        edad: Optional[int] = None,
        descripcion: Optional[str] =None,
        rol: Optional[str] = None,
        estado: Optional[str] = None
    ):
        return cls(
            nombre=nombre,
            correo=correo,
            clave=clave,
            edad=edad,
            descripcion=descripcion,
            rol=rol,
            estado=estado
        )