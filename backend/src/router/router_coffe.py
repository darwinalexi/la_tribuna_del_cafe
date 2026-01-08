from fastapi import APIRouter, UploadFile, File, Depends
from src.controller.controller_coffe import get_coffe_by_estate, create_coffe, update_coffe, delete_coffe
from src.models.model_coffe import Coffe

router_coffe= APIRouter()

@router_coffe.get("/cafe/{id_estate}")
def get_coffe(id_estate):
    return get_coffe_by_estate(id_estate)


@router_coffe.post("/cafe")
def create_coffes(
    id_usuario: int= None,
    # Esto le dice a FastAPI que busque los campos de Coffe en el Form-Data
    coffe :Coffe = Depends(Coffe.create_coffe), 
    img: UploadFile = File(None)
):
    return create_coffe(coffe, img, id_usuario)


@router_coffe.put("/cafe/{id}")
def update_coffes(
    id: int= None,
    id_usuario: int= None,
    coffe :Coffe = Depends(Coffe.update_coffe), 
    img: UploadFile = File(None)
):
    return update_coffe(coffe, img, id, id_usuario)

@router_coffe.delete("/cafe/{id_coffe}")
def delete_coffes(id_coffe: int):
    return delete_coffe(id_coffe)