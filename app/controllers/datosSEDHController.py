from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_datos_sedh(db: Session):
    try:
        # Obtener tipos de contrataciones
        tipos_contrataciones_result = db.execute(text("SELECT * FROM TIPOS_CONTRATACIONES")).mappings().all()
        datos_tipos_contrataciones = [
            {"id": row["IdTipoContratacion"], "descripcion": row["Nombre"]} 
            for row in tipos_contrataciones_result
        ]
        
        # Obtener dependencias
        dependencias_result = db.execute(text("SELECT * FROM DEPENDENCIAS")).mappings().all()
        datos_dependencias = [
            {"id": row["IdDependencia"], "descripcion": row["NomDependencia"]} 
            for row in dependencias_result
        ]
        
        # Obtener cargos
        cargos_result = db.execute(text("SELECT * FROM CARGOS")).mappings().all()
        datos_cargos = [
            {
                "id": row["IdCargo"], 
                "descripcion": row["NomCargo"], 
                "id_dependencia": row["IdDependencia"]
            } 
            for row in cargos_result
        ]
        
        # Obtener sexos
        sexos_result = db.execute(text("SELECT * FROM SEXOS")).mappings().all()
        datos_sexos = [
            {"id": row["IdSexo"], "descripcion": row["NomSexo"]} 
            for row in sexos_result
        ]
        
        # Obtener estados civiles
        estados_civiles_result = db.execute(text("SELECT * FROM ESTADOS_CIVILES")).mappings().all()
        datos_estados_civiles = [
            {"id": row["IdEstadoCivil"], "descripcion": row["NomEstadoCivil"]} 
            for row in estados_civiles_result
        ]
        
        # Obtener departamentos
        departamentos_result = db.execute(text("SELECT * FROM DEPARTAMENTOS")).mappings().all()
        datos_departamentos = [
            {"id": row["IdDepartamento"], "descripcion": row["NomDepartamento"]} 
            for row in departamentos_result
        ]
        
        # Obtener municipios
        municipios_result = db.execute(text("SELECT * FROM MUNICIPIOS")).mappings().all()
        datos_municipios = [
            {
                "id": row["IdMunicipio"], 
                "descripcion": row["NomMunicipio"], 
                "id_departamento": row["IdDepartamento"]
            } 
            for row in municipios_result
        ]
        
        # Obtener roles
        roles_result = db.execute(text("SELECT * FROM ROLES")).mappings().all()
        datos_roles = [
            {"id": row["IdRol"], "descripcion": row["NomRol"]} 
            for row in roles_result
        ]
        
        # Juntar todos los datos en un diccionario
        datos = {
            "tipos_contrataciones": datos_tipos_contrataciones,
            "dependencias": datos_dependencias,
            "cargos": datos_cargos,
            "sexos": datos_sexos,
            "estados_civiles": datos_estados_civiles,
            "departamentos": datos_departamentos,
            "municipios": datos_municipios,
            "roles": datos_roles
        }
        
        return datos
    except Exception as e:
        raise e