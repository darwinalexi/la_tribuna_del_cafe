from src.database.conexion import get_connection
from fastapi import HTTPException
from src.models.model_coment import Coment

def get_coment(id):
    try:
        connection= get_connection()
        cursor= connection.cursor()
        cursor.execute("select*from comentarios where id=%s", (id,))
        data=cursor.fetchall()

        if not data:
           raise HTTPException(status_code=404, detail="No se encontro comentarion con es id") 
        
        datas=[
            Coment(
                id= row[0],
                comentario=row[1],
                calificacion=row[2],
                id_usuario=row[3],
            )
            for row in data
        ]
        return datas
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

def create_comment(coment: Coment):
    try:

        connection= get_connection()
        cursor= connection.cursor()

        cursor.execute("""insert into comentarios(comentario, calificacion, id_usuario)values(%s, %s, %s)""",(coment.comentario, coment.calificacion,coment.id_usuario))
        connection.commit()

        return {"message": "Comentario creado exitosamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))