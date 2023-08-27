import time
import random
from config import panamericana, categorias
from product_scraper import get_product_links, get_product_details
from mongo_utils import insert_mongo_data


def main():
    for categoria in categorias:
        product_links = get_product_links(categoria['url'])
        for link in product_links:
            product_title, product_price, product_attributes, product_dimensions, product_features, product_benefits, product_brand, product_sku, product_model = get_product_details(link)
            product_info = {
                "Título del Producto": product_title,
                "Marca": product_brand,
                "SKU": product_sku,
                "Modelo": product_model,
                "Precio del Producto": product_price,
                "Atributos": product_attributes,
                "Dimensiones": product_dimensions,
                "Características": product_features,
                "Beneficios": product_benefits,
                "CategoryKey": categoria['cat_key'],  # Agregar el campo CategoryKey
            }
            insert_mongo_data(panamericana, product_info)

            random_delay = random.uniform(3, 5)
            time.sleep(random_delay)


if __name__ == "__main__":
    print("Iniciando scraping...")
    main()
    print("Scraping finalizado.")
