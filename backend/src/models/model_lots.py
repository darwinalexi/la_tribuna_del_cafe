from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Lots(BaseModel):
    id: int | None = None
    nombre_lote: Optional[str] = None 
    area: Optional[float]=None
    id_finca: Optional[int]=None
    variedad_cafe: Optional[str]=None
    densidad_de_siembra: Optional[int]=None
    fecha_siembra: Optional[datetime]=None
    altitud: Optional[int]=None
    cordenadas: Optional[str]=None
    tipo_suelo: Optional[str]=None
    ph: Optional[float]=None
    sistema_cultivo: Optional[str]=None
    estado_actual: Optional[str]=None