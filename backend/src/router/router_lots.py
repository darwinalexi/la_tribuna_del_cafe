from fastapi import APIRouter
from src.controller.controller_lots import get_lots, create_lot, update_lot, delete_lot
from src.models.model_lots import Lots

router_lots=APIRouter()

@router_lots.get("/lotes/{id}")
def get_lot_by_id(id):
    lot = get_lots(id)
    return lot

@router_lots.post("/lotes")
def create_lots(lot: Lots):
    return create_lot(lot)

@router_lots.put("/lotes/{id}")
def update_lots(lot: Lots, id: int):
    lot.id = id # Asigna el id de la URL al modelo del body
    return update_lot(lot)


@router_lots.delete("/lotes/{id}")
def delete_lots(id:int):
    return delete_lot(id)
