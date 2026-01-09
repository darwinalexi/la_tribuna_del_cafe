import os
from fastapi import HTTPException, UploadFile
from src.database.conexion import get_connection
from datetime import date
from typing import List
from src.controller.controoler_auth import get_password_hash
from src.models.models_user import User
import aiofiles as aofiles #se usa para manejar archivos de forma asincrona

#directorios para guardar archivos e img
Upload_dir="public/docs/user"
FILE_MAXIMUN=5
MAX_FILE_SIZE = 20 * 1024 * 1024  
TYPE_FILE=["application/pdf","application/png","image/jpeg","image/jpg"]
UPLOAD_DIR="public/img/user"

def get_user():
    try:
        connect = get_connection()

        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        if len(usuarios) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron usuarios")
        return usuarios

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

#recibe el parametro user_id y pasarselo al query
def get_user_by_id_controller(user_id: int):
    try:
        #conecta a la base de datos
        connect= get_connection()
        #crear un cursor  para ejecutar consultas
        cursor= connect.cursor(dictionary=True)
        #ejecuta la consulta
        cursor.execute("SELECT * FROM usuarios WHERE identificacion=%s", (user_id,))
        #obtener el resultado
        usuario= cursor.fetchone()
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    #este es como el catch en node js y atrapa el error 
    except Exception as ex:
        print("Error al obtener el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))

def create_user(model: User, imagen: UploadFile, archivo: List[UploadFile]):
    try:
        connect = get_connection()
        cursor = connect.cursor()

        # Verificar usuario existente
        cursor.execute("SELECT * FROM usuarios WHERE identificacion=%s", (model.identificacion,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        # -----------------------------------
        # GUARDAR IMAGEN
        # -----------------------------------
        imagen_filename = None
        if imagen:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            imagen_filename = imagen.filename
            imagen_path = os.path.join(UPLOAD_DIR, imagen_filename)

            with open(imagen_path, "wb") as buffer:
                buffer.write(imagen.file.read())

            print("✅ Imagen guardada:", imagen_filename)
        else:
            print("⚠️ No se recibió ninguna imagen")

        # GUARDAR ARCHIVOS
        # Normalizar archivos (si solo viene uno)
        if not archivo:
            archivo = []
        elif not isinstance(archivo, list):
            archivo = [archivo]

        tipo_archivo = None
        name_original = None
        fecha_carga = date.today()

        if archivo:
            os.makedirs(Upload_dir, exist_ok=True)

            for f in archivo:
                if getattr(f, "content_type", None) not in TYPE_FILE:
                    raise HTTPException(
                        status_code=415,
                        detail=f"Tipo no permitido: {f.content_type}"
                    )

                name_original = f.filename
                dest_path = os.path.join(Upload_dir, name_original)

                # Guardar archivo
                total = 0
                with open(dest_path, "wb") as out:
                    while chunk := f.file.read(1024 * 64):
                        out.write(chunk)
                        total += len(chunk)

                        if total > MAX_FILE_SIZE:
                            out.close()
                            os.remove(dest_path)
                            raise HTTPException(
                                status_code=413,
                                detail=f"Archivo demasiado grande: {f.filename}"
                            )

                tipo_archivo = f.content_type
                print("📄 Archivo guardado:", name_original)

        # -----------------------------------
        # INSERTAR USUARIO
        # -----------------------------------
        clave= model.clave[:72]
        password_finish=get_password_hash(clave)
        estado_default="Activo"
        cursor.execute(
            "INSERT INTO usuarios (identificacion, nombre, correo, edad, descripcion, rol, clave, imagen, estado) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (model.identificacion, model.nombre, model.correo, model.edad, model.descripcion, model.rol, password_finish, imagen_filename, estado_default)
        )

        if name_original:
            cursor.execute(
                "INSERT INTO archivos (fecha_carga, tipo_archivo, nombre, id_usuario) "
                "VALUES (%s, %s, %s, %s)",
                (fecha_carga, tipo_archivo, name_original, model.identificacion)
            )

        connect.commit()

        return {"status": 200, "mensaje": "Usuario creado exitosamente"}

    except HTTPException:
        raise
    except Exception as ex:
        print("Error al crear el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))

    

async def update_user(user_id, user:User, imagen, archivos):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select  usuarios.identificacion, usuarios.nombre as nombre, usuarios.correo, usuarios.clave, usuarios.edad, usuarios.descripcion, usuarios.rol, usuarios.imagen, usuarios.estado, usuarios.estado, archivos.nombre as nombre_archivo, archivos.id as id_archivo from usuarios join archivos on usuarios.identificacion = archivos.id_usuario where usuarios.identificacion=%s", (user_id,)) 
        existing_user= cursor.fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar.")
           
        nombre= user.nombre if user.nombre is not None else existing_user["nombre"]
        correo= user.correo if user.correo is not None else existing_user["correo"]
        clave= user.clave if user.clave is not None else existing_user["clave"]
        edad= user.edad if user.edad is not None else existing_user["edad"]
        descripcion= user.descripcion if user.descripcion is not None else existing_user["descripcion"]
        rol= user.rol if user.rol is not None else existing_user["rol"]
        estado= user.estado if user.estado is not None else existing_user["estado"]

        if clave != existing_user["clave"]:
            clave= clave[:72]
            clave=get_password_hash(clave)

        imagen_filename = None
        if imagen:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            if existing_user["imagen"]:
                nombre_img= existing_user["imagen"]
                ruta_img=os.path.join(UPLOAD_DIR, nombre_img)
                os.remove(ruta_img)

            imagen_filename = imagen.filename
            imagen_path = os.path.join(UPLOAD_DIR, imagen_filename)
            async with aofiles.open(imagen_path, "wb") as buffer:
                buffer.write(imagen.file.read())
            print("✅ Imagen guardada:", imagen_filename)
        else:
            print("⚠️ No se recibió ninguna imagen")

        if archivos and len(archivos) > 0:
            os.makedirs(Upload_dir, exist_ok=True)

            cursor.execute("select id, nombre FROM archivos WHERE id_usuario=%s", (user_id,))
            data_file= cursor.fetchall()
            #se encarga de eliminar los archivos viejos
            for file_db in data_file:
                ruta= os.path.join(Upload_dir, file_db["nombre"])
                if os.path.exists(ruta):
                    os.remove(ruta)
                cursor.execute("DELETE FROM archivos WHERE id=%s",(file_db["id"],))
            #recibe cada archivo y lo guarda en la carpeta
            for archivo in archivos:
                nombre_file= archivo.filename   
                dest_path= os.path.join(Upload_dir, nombre_file)
                async with aofiles.open(dest_path, "wb") as buffer:
                    buffer.write(archivo.file.read())
                tipo_archivo= archivo.content_type  
                fecha_carga= date.today()
                
                cursor.execute("INSERT INTO archivos (fecha_carga, tipo_archivo, nombre, id_usuario) VALUES (%s, %s, %s, %s)",
                (fecha_carga, tipo_archivo, nombre_file, user_id))


            cursor.execute("update usuarios set nombre=%s, correo=%s, clave=%s, edad=%s, descripcion=%s, rol=%s, imagen=%s, estado=%s where identificacion=%s",
                           (nombre, correo, clave, edad, descripcion, rol, imagen_filename, estado,user_id))
            connection.commit()
            if cursor.rowcount >= 0: 
                return {"status": 200, "mensaje": "Usuario actualizado exitosamente"}
            else:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario.")
    except Exception as ex:
        print("Error al actualizar el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))


def  delete_user(user_id: int):
    try:
        
        #conecta a la base de datos
        connect= get_connection()
        #crear un cursor  para ejecutar consultas
        cursor= connect.cursor(dictionary=True)
        cursor.execute("select id, nombre FROM archivos WHERE id_usuario=%s", (user_id,))
        data_file= cursor.fetchall()
        if len(data_file)==0: 
            raise HTTPException(status_code=404, detail="Usuario no encontrado o archivo para eliminar verifica tu identificacion.")

        for file_db in data_file:
            ruta= os.path.join(Upload_dir, file_db["nombre"])
            if os.path.exists(ruta):
                os.remove(ruta)
            cursor.execute("DELETE FROM archivos WHERE id=%s",(file_db["id"],))
            if cursor.rowcount >= 0:
                cursor.execute("DELETE FROM usuarios WHERE identificacion=%s", (user_id,))
                connect.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")
                return {"status": 200, "mensaje": "Usuario eliminado exitosamente"}
             
    except Exception as ex:
        print("Error al obtener el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))