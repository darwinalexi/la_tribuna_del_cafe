from src.database.conexion import get_connection
from fastapi import HTTPException
from src.models.model_analysis import Analysis

def get_analysis_for_coffe(id_coffe: int):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        print("id", id_coffe)

        cursor.execute("select*from analisis where id_cafe=%s",(id_coffe,))
        data = cursor.fetchall()
        if len(data)==0:
            raise HTTPException(status_code=404, detail="No hay analisis de este cafe")
        
        analisis=[
            Analysis(
                id=row[0],
                id_cafe= row[1],
                fragancia_y_aroma=row[2],
                sabor=row[3],
                sabor_residual= row[4],
                acidez= row[5],
                cuerpo= row[6] ,
                dulzura= row[7],
                balance= row[8],
                taza_limpia= row[9],
                uniformidad= row[10],
                imporesion_global= row[11],
                defectos= row[12],
                id_usuario= row[13],
            )
            for row in data
        ]
        return analisis


    except Exception as ex:   
        raise HTTPException(status_code=500, detail=str(ex))
    

def create_analysis(analysis: Analysis):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        cursor.execute("select*from analisis where id_cafe=%s",(analysis.id_cafe,))
        check= cursor.fetchall()

        if len(check) > 0:
            raise HTTPException(status_code=400, detail="Ya existe un analisis para este cafe, te sugiero actualizarlo o eliminarlo para crear un nuevo analisis.")

        cursor.execute(
            "insert into analisis(id_cafe, fragancia_y_aroma, sabor, sabor_residual, acidez, cuerpo, dulzura, balance, taza_limpia, uniformidad,impresion_global, defectos, id_usuario)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (analysis.id_cafe,analysis.fragancia_y_aroma, analysis.sabor, analysis.sabor_residual, analysis.acidez, analysis.cuerpo, analysis.dulzura, analysis.balance, analysis.taza_limpia, analysis.uniformidad, analysis.impresion_global, analysis.defectos, analysis.id_usuario)
        )
        connection.commit()
        return{"message":"Se Creo tu analisis de cafe correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) 
    

def update_analysis(id: int, analysis: Analysis):
    try:
        connection= get_connection()
        cursor= connection.cursor(dictionary=True)

        cursor.execute("select*from analisis where id=%s",(id,))
        check= cursor.fetchall()

        if len(check) == 0:
            raise HTTPException(status_code=400, detail="No existe este analisis para actualizar.")


        id_cafe = analysis.id_cafe if analysis.id_cafe is not None else check["id_cafe"]
        fragancia_y_aroma = analysis.fragancia_y_aroma if analysis.fragancia_y_aroma is not None else check["fragancia_y_aroma"]
        sabor = analysis.sabor if analysis.sabor is not None else check["sabor"]    
        sabor_residual = analysis.sabor_residual if analysis.sabor_residual is not None else check["sabor_residual"]
        acidez = analysis.acidez if analysis.acidez is not None else check["acidez"]
        cuerpo = analysis.cuerpo if analysis.cuerpo is not None else check["cuerpo"]
        dulzura = analysis.dulzura if analysis.dulzura is not None else check["dulzura"]
        balance = analysis.balance if analysis.balance is not None else check["balance"]
        taza_limpia = analysis.taza_limpia if analysis.taza_limpia is not None else check["taza_limpia"]
        uniformidad = analysis.uniformidad if analysis.uniformidad is not None else check["uniformidad"]
        impresion_global = analysis.impresion_global if analysis.impresion_global is not None else check["impresion_global"]
        defectos = analysis.defectos if analysis.defectos is not None else check["defectos"]
        id_usuario = analysis.id_usuario if analysis.id_usuario is not None else check["id_usuario"]
        cursor.execute(
            "update analisis set id_cafe=%s, fragancia_y_aroma=%s, sabor=%s, sabor_residual=%s, acidez=%s, cuerpo=%s, dulzura=%s, balance=%s, taza_limpia=%s, uniformidad=%s,impresion_global=%s, defectos=%s, id_usuario=%s where id=%s", 
            (id_cafe,fragancia_y_aroma, sabor,sabor_residual,acidez,cuerpo, dulzura,balance, taza_limpia,uniformidad,impresion_global,defectos,id_usuario, id)
        )
        connection.commit()
        return{"message":"Se Actualizo tu analisis de cafe correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) 
    

def delete_analysis_for_coffe(id_coffe: int):
    try:
        connection= get_connection()
        cursor= connection.cursor()

        cursor.execute("select*from analisis where id_cafe=%s",(id_coffe,))
        data = cursor.fetchone()
        if not data:
            raise HTTPException(status_code=404, detail="No hay analisis de este cafe para eliminar")
        
        cursor.execute("delete from analisis where id_cafe=%s",(id_coffe,))
        connection.commit()

        return {"message":"Analisis eliminado correctamente"}

    except Exception as ex:   
        raise HTTPException(status_code=500, detail=str(ex))