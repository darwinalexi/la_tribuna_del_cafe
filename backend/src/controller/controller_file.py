from src.database.conexion import get_connection
from fastapi import HTTPException
import os

FILE_DIRECTORY="public/docs"

def delete_file(id: int):
    try:
        connection=get_connection()
        cursor=connection.cursor()

        cursor.execute("select* from archivos WHERE id=%s", (id,))
        data=cursor.fetchone()

        if not data:
            return {"status":405,"mensaje":"No hay ningun archivo con ese id"}
        #se borra de nuestro server
        file_name=data[3]
        file_path=os.path.join(FILE_DIRECTORY, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("No existe este archivo")
        
        cursor.execute("delete from archivos where id=%s",(id,))
        connection.commit()

        return {"status":200,"mensaje":"Archivo eliminado correctamente"}

        
    except Exception as e:
        print("error", e)
        raise HTTPException(status_code=500, detail=str(e))
