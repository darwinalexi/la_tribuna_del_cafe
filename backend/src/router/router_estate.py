from fastapi import APIRouter, Form, UploadFile, File, Depends, Path
from src.controller.controller_estate import read_estate_of_user, create_estate, update_estate, delete_estate
from typing import List, Annotated
from src.models.model_estate import Estate
router_estate=APIRouter()

@router_estate.get("/fincas/{id}")
def read_estate(id):
    farms = read_estate_of_user(id)
    return farms

@router_estate.post("/fincas")
def create(estate: Estate= Depends(Estate.as_form),
           archivo: List[UploadFile] = File(...),):
    return create_estate(estate, archivo)


@router_estate.put("/fincas/{id}")
def update_estate_for_user(
    id: int,
    estate: Estate= Depends(Estate.as_form),
    archivo: List[UploadFile] = File(None),   
):
    return update_estate(id, estate, archivo)

@router_estate.delete("/fincas/{id}")
def delete_farms_by_farms(id):
    Estate= delete_estate(id)
    return Estate