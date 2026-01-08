from src.database.conexion import get_connection
from src.models.model_coffe import Coffe
from fastapi import HTTPException, File, UploadFile
from datetime import date
import os

DIR_IMG="public/img"
def get_coffe_by_estate(id_estate: int):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        cursor.execute("select*from cafes where id_finca=%s",(id_estate,))
        data= cursor.fetchall()

        if len(data)==0:
           raise HTTPException(status_code=404, detail="No hay cafes registrados para subastar de la finca")
        
        data_coffe=[
            Coffe(
                id=row[0],
                nombre_cafe= row[1],
                humedad= row[2],
                peso = row[3],
                tipo_empaque= row[4],
                id_lote= row[5],
                variedad= row[6],
                id_analisis= row[7],
                id_finca=row[8],
            )
            for row in data
            ]
        return data_coffe

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    


def create_coffe(coffe: Coffe, img: UploadFile = File(None), id_usuario:int= None):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        imagen_filname= None
        if img:
            os.makedirs(DIR_IMG, exist_ok=True)
            imagen_filname= img.filename
            imagen_path= os.path.join(DIR_IMG, imagen_filname)
            with open(imagen_path, "wb") as buffer:
                buffer.write(img.file.read())
                tipo_archivo = img.content_type
                fecha_carga = date.today()
                #guarda el nombre_original de archivo
                name_original=img.filename
                cursor.execute("insert into archivos (fecha_carga, tipo_archivo, nombre, id_usuario, id_finca)values(%s, %s, %s, %s, %s)",(fecha_carga, tipo_archivo, name_original, id_usuario, coffe.id_finca))
                id_archivo=cursor.lastrowid

            print("Imagen guardada en:", imagen_filname)
        else:
            print("No se proporcionó ninguna imagen.")

        cursor.execute("insert into cafes(nombre_cafe, humedad, peso, tipo_empaque, id_lote, variedad, id_analisis, id_finca, id_archivo)values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ",( coffe.nombre_cafe, coffe.humedad,coffe.peso, coffe.tipo_empaque, coffe.id_lote, coffe.variedad, coffe.id_analisis, coffe.id_finca,id_archivo))
        connection.commit()
        return {"status":200, "message":"Cafe creado correctamente"}
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

def update_coffe(coffe: Coffe, img: UploadFile = File(None), id_coffe:int= None, id_usuario:int= None):
    try:
        connection= get_connection()
        cursor= connection.cursor(dictionary=True)

        cursor.execute("select cafes.id as id_cafe, cafes.nombre_cafe as nombre_del_cafe, archivos.nombre as nombre_archivo, archivos.id as id_archivo from cafes join archivos on cafes.id_archivo = archivos.id where cafes.id=%s",(id_coffe,))
        data= cursor.fetchone()
        
        if not data:
            HTTPException(status_code=404, detail="No se encontro el cafe para actualizar.")

        nombre_cafe= coffe.nombre_cafe if coffe.nombre_cafe is not None else data["nombre_cafe"]
        humedad= coffe.humedad if coffe.humedad is not None else data["humedad"]
        peso= coffe.peso if coffe.peso is not None else data["peso"]
        tipo_empaque= coffe.tipo_empaque if coffe.tipo_empaque is not None else data["tipo_empaque"]
        id_lote= coffe.id_lote if coffe.id_lote is not None else data["id_lote"]
        variedad= coffe.variedad if coffe.variedad is not None else data["variedad"]
        id_analisis= coffe.id_analisis if coffe.id_analisis is not None else data["id_analisis"]
        id_archivo= coffe.id_archivo if coffe.id_archivo is not None else data["id_archivo"]
        imagen_filname= None
        if img:
            os.makedirs(DIR_IMG, exist_ok=True)
            imagen_filname= img.filename
            imagen_path= os.path.join(DIR_IMG, imagen_filname)
            with open(imagen_path, "wb") as buffer:
                buffer.write(img.file.read())
                tipo_archivo = img.content_type
                fecha_carga = date.today()
                #guarda el nombre_original de archivo
                name_original=img.filename
                cursor.execute("insert into archivos (fecha_carga, tipo_archivo, nombre, id_usuario, id_finca)values(%s, %s, %s, %s, %s)",(fecha_carga, tipo_archivo, name_original, id_usuario, coffe.id_finca))
                id_archivo=cursor.lastrowid

            print("Imagen guardada en:", imagen_filname)
        else:
            print("No se proporcionó ninguna imagen.")

        cursor.execute("update cafes set nombre_cafe=%s, humedad=%s, peso=%s, tipo_empaque=%s, id_lote=%s, variedad=%s, id_analisis=%s, id_finca=%s, id_archivo=%s where id=%s", (nombre_cafe, humedad, peso, tipo_empaque, id_lote, variedad, id_analisis, coffe.id_finca, id_archivo, id_coffe))
        
        #el archivo se debe eliminar siempre despues de actualizar el registro
        if img and data:
            nombre_archivo= data["nombre_archivo"]
            id_archivo= data["id_archivo"]
            ruta_fisica= os.path.join(DIR_IMG, nombre_archivo)
            os.remove(ruta_fisica)
            print("Archivo anta" \
"erior eliminado:", nombre_archivo)

            cursor.execute("delete from archivos where id=%s",(id_archivo,))
            connection.commit()

        if cursor.rowcount >=0:
            return {"status":200, "message":"Cafe Actualizado correctamente"}
        else:
            return {"status":200, "message":"Cafe  existente pero no se pudo actualizar correctamente"}
    
    except Exception as ex:
        print("error", ex)
        raise HTTPException(status_code=500, detail=str(ex))
    


def delete_coffe(id_coffe:int):
    try:
        connection= get_connection()
        cursor= connection.cursor(dictionary=True)
        cursor.execute("select* from cafes where id=%s",(id_coffe,))
        data= cursor.fetchone()
        id_archivo= data["id_archivo"]
        if cursor.rowcount >= 0:
            cursor.execute("delete from cafes where id=%s",(id_coffe,))
            datadelete= cursor.rowcount           
            if cursor.rowcount >=0:
                cursor.execute("delete from archivos where id=%s",(id_archivo,))
                connection.commit()
                if cursor.rowcount >=0 and datadelete >=0:
                    return {"status":200, "message":"Cafe eliminado correctamente"}
                else:
                    raise HTTPException(status_code=404, detail="No se encontro el cafe para eliminar.")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
