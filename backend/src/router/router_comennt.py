from fastapi import  APIRouter
from src.controller.controller_coment import get_coment, create_comment
from src.models.model_coment import Coment

router_coment= APIRouter()

@router_coment.get("/comentarios/{id}")
def get_coment_by_id(id:int):
    return get_coment(id)

@router_coment.post("/comentarios")
def create_coments(coment: Coment):
    return create_comment(coment)
