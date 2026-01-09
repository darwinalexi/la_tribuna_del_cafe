from src.database.conexion import get_connection
from fastapi import HTTPException, Form, UploadFile
from datetime import date
from typing import List
from src.models.model_estate import Estate
import os

TYPE_FILE=["application/pdf"]
DIRECTORY_FILE="public/docs/estate"
MAX_FILE_SIZE = 1 * 1024 * 1024  

def read_estate_of_user(user_id: int):
    try:
        connection= get_connection()
        cursor=connection.cursor()
        cursor.execute("select *from fincas where id_usuario=%s",(user_id,))
        #manda todas las filas que encuentre
        user= cursor.fetchall()

        if user is None:
            raise  HTTPException(status_code=400, detail="No tienes fincas registradas con su identificacion.")
        
        #organiza los datos en un formato json
        estates = [
            Estate(
                id=row[0],
                nombre_finca=row[1],
                id_usuario=row[2],
                extencion_tierra=row[3],
                id_municipio=row[4],
                id_departamento=row[5],
                cordenadas=row[6],
                id_archivo=row[7],
                altitud=row[8],
            )
            for row in user
        ]

        return estates
        
    except Exception as e:
        print("error", e)
        raise HTTPException(status_code=500, detail=str(e))
    

def create_estate(
        estate: Estate,
        archivos: List[UploadFile] = None
):
    
    try:
        connection= get_connection()
        cursor=connection.cursor()
         # ❌ SOLO PERMITIR 1 ARCHIVO
        if len(archivos) > 1:
            raise HTTPException(
                status_code=400,
                detail="Solo se permite cargar 1 archivo"
            )

        # Si no adjuntaron archivo
        if len(archivos) == 0:
            raise HTTPException(
                status_code=400,
                detail="Debes adjuntar un archivo"
            )

        f = archivos[0]  # El único archivo permitido

        # ✔ Validar tipo MIME
        if f.content_type not in TYPE_FILE:
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no válido. Solo PDF."
            )

        archivos= archivos or []

        if archivos:
            os.makedirs(DIRECTORY_FILE, exist_ok=True)
            for f in archivos:
                if getattr(f, "content_type",None) not in TYPE_FILE:
                    raise HTTPException(status_code=400, detail="Tipo de archivo no valido se aceptan archivos con extension .pdf")
        
        ext= os.path.splitext(f.filename)[1]
        name_original= f.filename

        dest_path = os.path.join(DIRECTORY_FILE, name_original)


        total = 0
        with open(dest_path, "wb") as out:
            while chunk := f.file.read(1024 * 64):
                out.write(chunk)
                total += len(chunk)
                if total > MAX_FILE_SIZE:
                        out.close()
                        os.remove(dest_path)
                        raise HTTPException(status_code=413, detail=f"Archivo demasiado grande: {f.filename}")

                tipo_archivo = f.content_type
                fecha_carga = date.today()
                #guarda el nombre_original de archivo
                name_original=f.filename
                cursor.execute("insert into archivos (fecha_carga, tipo_archivo, nombre, id_usuario)values(%s, %s, %s, %s)",(fecha_carga, tipo_archivo, name_original, estate.id_usuario))
                id_archivo=cursor.lastrowid
                print("✅ Archivo guardado:", id_archivo)

                cursor.execute(
                    "INSERT INTO fincas (nombre_finca, id_usuario, extension_tierra, id_municipio, id_departamento, cordenadas, altitud) VALUES (%s,  %s, %s, %s, %s, %s, %s)",
                    (estate.nombre_finca, estate.id_usuario, estate.extension_tierra, estate.id_municipio, estate.id_departamento, estate.cordenadas,  estate.altitud)
                )
                connection.commit()
                return {"status":200, "mensaje":" se creo la finca con exito"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def update_estate(
        id: int,
        estate: Estate,
        archivos: List[UploadFile] =None
    ):
    try:
        connect= get_connection()
        cursor= connect.cursor()

        cursor.execute("select*from fincas where id=%s",(id,))
        #manda solo una fila que encuentre en la base de datos
        data= cursor.fetchone()



        if not data:
            return HTTPException(status_code=404, detail="Lo sentimos pero no tenemos información sobre esta finca para poder actualizar su información.")
          # ❌ SOLO PERMITIR 1 ARCHIVO
        if len(archivos) > 1:
            raise HTTPException(
                status_code=400,
                detail="Solo se permite cargar 1 archivo"
            )

        # Si no adjuntaron archivo
        if len(archivos) == 0:
            raise HTTPException(
                status_code=400,
                detail="Debes adjuntar un archivo"
            )

        f = archivos[0]  # El único archivo permitido

        # ✔ Validar tipo MIME
        if f.content_type not in TYPE_FILE:
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no válido. Solo PDF."
            )
        
        
        nombre_finca_finish= estate.nombre_finca if estate.nombre_finca is not None else data[1]
        id_usuario_finish= estate.id_usuario if estate.id_usuario is not None else data[2]
        extencion_tierra_finish= estate.extension_tierra if estate.extension_tierra is not None else data[3]
        id_municipio_finish= estate.id_municipio if estate.id_municipio is not None else data[4]
        id_departamento_finish= estate.id_departamento if estate.id_departamento is not None else data[5]
        cordenadas_finish= estate.cordenadas if estate.cordenadas is not None else data[6]
        altitud_finish= estate.altitud if estate.altitud is not None else data[7]

        if archivos:
                os.makedirs(DIRECTORY_FILE, exist_ok=True)
                for f in archivos:
                    if getattr(f,"content_type", None) not in TYPE_FILE:
                        raise HTTPException(status_code=405, detail=str("Lo sentimos pero tu archivi no es el tipo que aceptamos aseguarete que al final del nombre sea  .pd"))

                    name_original= f.filename
                    dest_path= os.path.join(DIRECTORY_FILE, name_original)
                    
                    total= 0
            
                    with open(dest_path, "wb") as out:
                        while chunck :=f.file.read(1024*64):
                            out.write(chunck)
                            total += len(chunck)

                            if total > MAX_FILE_SIZE:
                                out.close()
                                os.remove(dest_path)
                                raise HTTPException(status_code=413, detail=f"Archivo demasiado grande: {f.filename}")
                            
                            tipo_archivo= f.content_type
                            fecha_carga= date.today()
                            name_original=f.filename

                            cursor.execute(
                                "INSERT INTO archivos (fecha_carga, tipo_archivo, nombre, id_usuario) VALUES (%s, %s, %s, %s)",
                                (fecha_carga, tipo_archivo, name_original, id_usuario_finish)
                                )
                            
                            cursor.execute("update fincas set nombre_finca=%s, id_usuario=%s, extension_tierra=%s, id_municipio=%s, id_departamento=%s, cordenadas=%s, altitud=%s where id=%s",(nombre_finca_finish,id_usuario_finish, extencion_tierra_finish, id_municipio_finish, id_departamento_finish, cordenadas_finish, altitud_finish, id,))

                            print("✅ Archivo guardado:", name_original)
                            connect.commit()

        return {"status": 200, "mensaje": "Usuario Actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def delete_estate(id: int):
    try:
        connect= get_connection()
        cursor= connect.cursor()
        cursor.execute("select*from fincas where id=%s",(id,))
        data= cursor.fetchone()
        if not data:
         return HTTPException(status_code=404, detail="Lo sentimos pero no tenemos información sobre esta finca para poder eliminar su información.")
        
        id_file=data[7]
        cursor.execute("select*from archivos where id=%s",(id_file,))
        file= cursor.fetchone()
        name_file= file[3]
        file_path=os.path.join(DIRECTORY_FILE, name_file)

        if os.path.join(file_path):
            os.remove(file_path)
        else:
            return HTTPException(status_code=404, detail="No existe este archivo")
        
        cursor.execute("delete from archivos where id=%s",(id_file,))
    
        cursor.execute("delete from fincas where id=%s",(id,))
        connect.commit()
        
        return {"status": 200, "mensaje": "Finca eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))