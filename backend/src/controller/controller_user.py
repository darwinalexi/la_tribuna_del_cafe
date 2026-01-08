import os
from fastapi import HTTPException, UploadFile
from src.database.conexion import get_connection
from datetime import date
from typing import List
from src.controller.controoler_auth import get_password_hash
from src.models.models_user import User

#directorios para guardar archivos e img
Upload_dir="public/docs"
FILE_MAXIMUN=5
MAX_FILE_SIZE = 20 * 1024 * 1024  
TYPE_FILE=["application/pdf","application/png","image/jpeg","image/jpg"]
UPLOAD_DIR="public/img"

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

        # -----------------------------------
        # GUARDAR ARCHIVOS
        # -----------------------------------
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
        cursor.execute(
            "INSERT INTO usuarios (identificacion, nombre, correo, edad, descripcion, rol, clave, imagen) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (model.identificacion, model.nombre, model.correo, model.edad, model.descripcion, model.rol, password_finish, imagen_filename)
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

    
#falta  quee encripte la clave al atcualizar
def update_user(user_id, user, imagen, archivos):
    try:
        connection = get_connection()
        # Usa dictionary=True aquí si quieres acceder por nombre, si no, usa índices como ya hacías
        cursor = connection.cursor(dictionary=False) 
        cursor.execute("SELECT * FROM usuarios WHERE identificacion=%s", (user_id,))
        existing_user = cursor.fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Mapear valores actuales / nuevos, manejando strings vacíos si es necesario
        nombre_final = user.nombre if user.nombre is not None and user.nombre.strip() != "" else existing_user[1]
        correo_final = user.correo if user.correo is not None and user.correo.strip() != "" else existing_user[2]
        
        # --- Lógica de Encriptación ---
        if clave not in [None, "", " "]:
            clave_final = get_password_hash(user.clave[:72])
            print("🔒 Nueva clave encriptada:", clave_final)
        else:
            print("ℹ️ Clave no enviada, se mantiene la existente")


        edad_final = user.edad if user.edad is not None else existing_user[4]
        descripcion_final = user.descripcion if user.descripcion is not None else existing_user[5]
        rol_final = user.rol if user.rol is not None else existing_user[6]
        imagen_final = existing_user[7]

        # Si hay imagen nueva
        if imagen:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            imagen_filename = imagen.filename
            imagen_path = os.path.join(UPLOAD_DIR, imagen_filename)
            with open(imagen_path, "wb") as buffer:
                buffer.write(imagen.file.read())
            print("✅ Imagen guardada:", imagen_filename)
            imagen_final = imagen_filename

        # Ejecutar UPDATE
        cursor.execute(
            """
            UPDATE usuarios
            SET nombre=%s, correo=%s, clave=%s, edad=%s, descripcion=%s, rol=%s, imagen=%s
            WHERE identificacion=%s
            """,
            (nombre_final, correo_final, clave_final, edad_final, descripcion_final, rol_final, imagen_final, user_id)
        )

        # Guardar archivos si vienen
        if archivos:
            os.makedirs(Upload_dir, exist_ok=True)
            for f in archivos:
                if getattr(f, "content_type", None) not in TYPE_FILE:
                    raise HTTPException(status_code=415, detail=f"Tipo no permitido: {f.content_type}")

                name_original = f.filename
                dest_path = os.path.join(Upload_dir, name_original)

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

                cursor.execute(
                    "INSERT INTO archivos (fecha_carga, tipo_archivo, nombre, id_usuario, id_finca) VALUES (%s, %s, %s, %s)",
                    (fecha_carga, tipo_archivo, name_original, user_id)
                )

                print("✅ Archivo guardado:", name_original)

        connection.commit()
        return {"status": 200, "mensaje": "Usuario actualizado exitosamente"}

    except Exception as ex:
        print("Error al actualizar el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))


def  delete_user(user_id: int):
    try:
        #conecta a la base de datos
        connect= get_connection()
        #crear un cursor  para ejecutar consultas
        cursor= connect.cursor(dictionary=True)
        #ejecuta la consulta
        cursor.execute("DELETE FROM usuarios WHERE identificacion=%s", (user_id,))
        #obtener el resultado y no se puede quedar sin esto si no no borra
        connect.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"status": 200, "mensaje": "Usuario eliminado exitosamente"}
    #este es como el catch en node js y atrapa el error 
    except Exception as ex:
        print("Error al obtener el usuario:", ex)
        raise HTTPException(status_code=500, detail=str(ex))