from pydantic import BaseModel
from typing import Optional 

class Analysis(BaseModel):
    id : int | None = None
    id_cafe: Optional[int]= None 
    fragancia_y_aroma: Optional[str]= None
    sabor: Optional[int] =None
    sabor_residual: Optional[int] =None
    acidez: Optional[int] =None
    cuerpo: Optional[int] =None
    dulzura: Optional[int] =None
    balance: Optional[int] =None
    taza_limpia: Optional[int] =None
    uniformidad: Optional[int] =None
    impresion_global: Optional[int] =None
    defectos: Optional[int] =None
    id_usuario: Optional[int] =None

    

