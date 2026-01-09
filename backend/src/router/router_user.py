from fastapi import APIRouter, Form, File,UploadFile, Depends
from src.controller.controller_user import get_user , get_user_by_id_controller, create_user, delete_user, update_user as update_user
from src.models.models_user import User
from typing import List, Optional
import aiofiles

router_user= APIRouter()

@router_user.get("/users", response_model=List[User])
def list_users():
    return get_user()

@router_user.get("/get_user_for_id/{user_id}", response_model=User)
def get_user_id(user_id: int):
    user = get_user_by_id_controller(user_id)
    return user

@router_user.post("/create_user")
def create_users(
    user: User = Depends(User.create_form),
    archivo: List[UploadFile] = File(None),
    imagen: UploadFile = File(None)
):
    # Pasar los archivos en el orden esperado por el controlador: imagen, archivo
    return create_user(user,imagen, archivo)


@router_user.put("/update_user/{user_id}")
async def update_users(
                user_id: int,   
                user: User = Depends(User.update_form),
                archivos: Optional[List[UploadFile]] = File(None),
                imagen: Optional[UploadFile] = File(None)):
    return  await update_user(user_id, user, imagen, archivos)

@router_user.delete("/delete_user/{user_id}")
def delete_users(user_id: int):
     return  delete_user(user_id) 