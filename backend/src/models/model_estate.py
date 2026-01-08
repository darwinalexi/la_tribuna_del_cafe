from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class Estate(BaseModel):
    id: int | None = None
    nombre_finca: Optional[str]=None
    id_usuario: Optional[int]= None
    extension_tierra: Optional[float]=None
    id_municipio: Optional[int]=None
    id_departamento:Optional[int]= None
    cordenadas: Optional[str]= None
    altitud: Optional[int]= None

    @classmethod
    def as_form(
        cls,
        nombre_finca: str =Form(...),
        id_usuario: int= Form(...),
        extension_tierra:float= Form(...),
        id_municipio:int=Form(...),
        id_departamento: int = Form(...),
        cordenadas: str= Form(...),
        altitud: int= Form(...)
    ):
        return cls(
            nombre_finca=nombre_finca,
            id_usuario=id_usuario,
            extension_tierra=extension_tierra,
            id_municipio=id_municipio,
            id_departamento=id_departamento,
            cordenadas=cordenadas,
            altitud=altitud
        )
