from fastapi  import APIRouter
from src.controller.controller_analysis import get_analysis_for_coffe, create_analysis, update_analysis, delete_analysis_for_coffe
from src.models.model_analysis import Analysis
router_analysis= APIRouter()

@router_analysis.get("/analisis/{id_coffe}")
def get_analisis_coffe(id_coffe: int):
    return get_analysis_for_coffe(id_coffe)

@router_analysis.post("/analisis")
def create_analisis(analysis: Analysis):
    return create_analysis(analysis)

@router_analysis.put("/analisis/{id}")
def update__of_analisis(id: int, analysis: Analysis):
    return update_analysis(id,analysis)

@router_analysis.delete("/analisis/{id_cafe}")
def delete_analisis(id_cafe: int):
    return delete_analysis_for_coffe(id_cafe)