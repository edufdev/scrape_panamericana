from datetime import datetime


def insert_mongo_data(collection, product_info):
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar si el modelo ya existe en la base de datos
    existing_doc = collection.find_one({"Modelo": product_info["Modelo"]})
    
    # Si el modelo no existe, se inserta un nuevo documento
    if not existing_doc:
        product_info["CreatedDate"] = date  # Agregar la fecha de creación
        product_info["LastUpdatedDate"] = date  # Agregar la fecha de última actualización
        collection.insert_one(product_info)
        print(f"Nuevo documento insertado para el modelo {product_info['Modelo']}")
    else:
        # Si el modelo existe, se actualiza el documento
        product_info["LastUpdatedDate"] = date  # Agregar la fecha de última actualización
        # Eliminar el campo CreatedDate si se está actualizando el documento
        product_info.pop("CreatedDate", None)
        collection.update_one({"Modelo": product_info["Modelo"]}, {"$set": product_info})
        print(f"Documento actualizado para el modelo {product_info['Modelo']}")