from src.database.conexion import get_connection
from fastapi import HTTPException
from src.models.model_lots import Lots

def get_lots(id):
            try:
                connection=get_connection()
                cursor= connection.cursor()

                cursor.execute("select*from lotes where id_finca=%s",(id,))

                lots= cursor.fetchall()

                if len(lots) == 0:
                    raise HTTPException(status_code=404, detail="No se encontraron lotes asociados a esta finca")
                
                lotes = [
                    Lots(
                        id=row[0],
                        nombre_lote=row[1],
                        area=row[2],
                        id_finca=row[3],
                        variedad_cafe=row[4],
                        densidad_de_siembra=row[5],
                        fecha_siembra=row[6],
                        altitud=row[7],
                        cordenadas=row[8],
                        tipo_suelo=row[9],
                        ph=row[10],
                        sistema_cultivo=row[11],
                        estado_actual=row[12],
                    )
                        for row in lots
                ]
                
                return lotes
            
            except Exception as ex:
                raise HTTPException(status_code=500, detail=str(ex))
        


def create_lot(lot: Lots):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""insert into lotes(nombre_lote, area, id_finca, variedad_cafe, densidad_de_siembra, fecha_siembra, altitud, cordenadas, tipo_suelo, ph, sistema_cultivo, estado_actual)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(lot.nombre_lote,
                lot.area,
                lot.id_finca,
                lot.variedad_cafe,
                lot.densidad_de_siembra,
                lot.fecha_siembra,
                lot.altitud,
                lot.cordenadas,
                lot.tipo_suelo,
                lot.ph,
                lot.sistema_cultivo,
                lot.estado_actual))
            connection.commit()

            return {"message": "Lote creado exitosamente"}  

        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))
        


def update_lot(lot_data: Lots):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""select*from lotes where id=%s""",(lot_data.id,))
            lot_db=cursor.fetchone()

            if not lot_db : 
                  raise HTTPException(status_code=400, detail="Lo sentimos este lote no existe")
            
        
            nombre_lote_finish = lot_data.nombre_lote if lot_data.nombre_lote is not None else lot_db["nombre_lote"]
            area_finish = lot_data.area if lot_data.area is not None else lot_db["area"]
            id_finca_fininsh = lot_data.id_finca if lot_data.id_finca is not None else lot_db["id_finca"]
            variedad_cafe_finish = lot_data.variedad_cafe if lot_data.variedad_cafe is not None else lot_db["variedad_cafe"]
            densidad_de_siembra_finish = lot_data.densidad_de_siembra if lot_data.densidad_de_siembra is not None else lot_db["densidad_de_siembra"]
            fecha_siembra_finish = lot_data.fecha_siembra if lot_data.fecha_siembra is not None else lot_db["fecha_siembra"] 
            altitud_finish = lot_data.altitud if lot_data.altitud is not None else lot_db["altitud"]
            cordenadas_finish = lot_data.cordenadas if lot_data.cordenadas is not None else lot_db["cordenadas"]
            tipo_suelo_finish = lot_data.tipo_suelo if lot_data.tipo_suelo is not None else lot_db["tipo_suelo"]          
            ph_finish = lot_data.ph if lot_data.ph is not None else lot_db["ph"]
            sistema_cultivo_finish = lot_data.sistema_cultivo if lot_data.sistema_cultivo is not None else lot_db["sistema_cultivo"]
            estado_actual_finish = lot_data.estado_actual if lot_data.estado_actual is not None else lot_db["estado_actual"]


            cursor.execute(""" update lotes set nombre_lote=%s, area=%s, id_finca=%s, variedad_cafe=%s, densidad_de_siembra=%s, fecha_siembra=%s, altitud=%s, cordenadas=%s, tipo_suelo=%s, ph=%s, sistema_cultivo=%s, estado_actual=%s where id = %s""",(nombre_lote_finish,
                area_finish,
                id_finca_fininsh,
                variedad_cafe_finish,
                densidad_de_siembra_finish,
                fecha_siembra_finish,
                altitud_finish,
                cordenadas_finish,
                tipo_suelo_finish,
                ph_finish,
                sistema_cultivo_finish,
                estado_actual_finish,
                lot_db["id"]
                ))
            connection.commit()

            return {"message": "Lote Actualizado exitosamente"}  

        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))
        

def delete_lot(id:int):
    try:
       
        connection = get_connection()
        cursor= connection.cursor()

        cursor.execute("select*from lotes where id=%s",(id,))
        data= cursor.fetchone()
        if not data:
             return HTTPException(status_code=404, detatil="No encontramos este numero de lote verifica tu id")
        

        cursor.execute("delete from lotes where id=%s",(id,))
        connection.commit()

        return {"message":"Lote elimninado con exito"}

    except Exception as ex:     
        raise HTTPException(statu_code=500, detail=str(ex))