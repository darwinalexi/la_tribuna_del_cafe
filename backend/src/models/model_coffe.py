from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class Coffe(BaseModel):
    id: int | None=None
    nombre_cafe:Optional[str] = None
    humedad : Optional[str] = None
    peso : Optional[int]= None
    tipo_empaque: Optional[str]= None
    id_lote: Optional[int]= None
    variedad: Optional[str]= None
    id_analisis: Optional[int]= None
    id_finca: Optional[int]= None
    id_archivo: Optional[int]= None
    @classmethod
    def create_coffe(
        cls,
        id: int = None,
        nombre_cafe: str = Form(...),
        humedad: str = Form(...),
        peso :int= Form(...),
        tipo_empaque:str= Form(...),
        id_lote:  int= Form(...),
        variedad: str= Form(...),
        id_analisis: int = Form(...),
        id_finca: int = Form(...)   
    ):
        return cls(
            id=id,
            nombre_cafe=nombre_cafe,
            humedad=humedad,
            peso=peso,
            tipo_empaque=tipo_empaque,
            id_lote=id_lote,
            variedad=variedad,
            id_analisis=id_analisis,
            id_finca=id_finca
        )

    @classmethod
    def update_coffe(
        cls,
        id: int = None,
        nombre_cafe:Optional[str] = None,
        humedad : Optional[str] = None,
        peso : Optional[int]= None,
        tipo_empaque: Optional[str]= None,
        id_lote: Optional[int]= None,
        variedad: Optional[str]= None,
        id_analisis: Optional[int]= None,
        id_finca: Optional[int]= None
    ):
       
      return cls(
            id=id,
            nombre_cafe=nombre_cafe,
            humedad=humedad,
            peso=peso,
            tipo_empaque=tipo_empaque,
            id_lote=id_lote,
            variedad=variedad,
            id_analisis=id_analisis,
            id_finca=id_finca
        )
