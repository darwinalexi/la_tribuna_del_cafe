from fastapi import APIRouter
from src.controller.controller_file import delete_file
router_file=APIRouter()

@router_file.delete("/files/{id}")
def delete_files(id:int):
    file= delete_file(id)
    return file
