from fastapi import APIRouter
from src.controller.controoler_auth import login
from src.models.model_login import Loginuse

router_auth = APIRouter()

@router_auth.post("/login")
def login_route(data: Loginuse):
    return login(data.correo, data.clave)
