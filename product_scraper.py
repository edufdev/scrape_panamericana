import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = []

    product_elements = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
    for product_element in product_elements:
        link = product_element.get('href')
        product_links.append(link)

    return product_links


def extract_attribute_value(value_element):
    if value_element.name == 'ul':
        return [item.get_text(strip=True) for item in value_element.find_all('li')]
    elif value_element.name == 'p':
        return value_element.get_text(strip=True)
    else:
        return value_element.text.strip()
    
    
# def extract_dimension_values_format1(value_element):
#     values = re.findall(r"([\w\s]+)\s+\(([c\w]+)\)\s+([\d.]+)", value_element.text)
#     dimension_dict = {name.strip(): value for name, _, value in values}
#     return dimension_dict


# def extract_dimension_values_format2_3(ul_element):
#     dimension_dict = {}
#     ul_items = ul_element.find_all('li', class_='col-md-6 key')
#     for ul_item in ul_items:
#         parts = ul_item.text.split(':')
#         if len(parts) == 2:
#             name = parts[0].strip()
#             value = parts[1].strip()
#             dimension_dict[name] = value
#     return dimension_dict


# def extract_dimension_values(value_element):
#     div_with_ul = value_element.find('div', {'class': 'row'})
#     ul_element = value_element.find('ul')

#     if div_with_ul and ul_element:
#         return extract_dimension_values_format2_3(ul_element)
#     elif ul_element:
#         if ul_element.find('li', class_='col-md-6 key'):
#             return extract_dimension_values_format2_3(ul_element)
#         else:
#             return extract_dimension_values_format1(value_element)
#     else:
#         return extract_dimension_values_format1(value_element)


# def extract_feature_value(value_element):
#     if value_element.name == 'ul':
#         return [item.get_text(strip=True) for item in value_element.find_all('li')]
#     else:
#         return value_element.text.strip()
    
    
def extract_features(value_element):
    features = []
    ul_element = value_element.find('ul', role='table')
    if ul_element:
        li_elements = ul_element.find_all('li', role='rowgroup')
        for li_element in li_elements:
            dl_elements = li_element.find_all('div', class_='flix-dl', role='row')
            feature = {}
            for dl_element in dl_elements:
                dt_element = dl_element.find('div', class_='flix-dt', role='cell')
                dd_element = dl_element.find('div', class_='flix-dd', role='cell')
                if dt_element and dd_element:
                    feature_name = dt_element.text.strip()
                    feature_value = dd_element.text.strip()
                    feature[feature_name] = feature_value
            features.append(feature)
    return features


def format_attribute(attribute_name, attribute_value):
    return {"name": attribute_name, "value": attribute_value}



def get_product_details(product_link):
    response = requests.get(product_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_title_element = soup.find('h1', class_='product_title entry-title')
    product_title = product_title_element.text.strip() if product_title_element else None
    
    product_description_elemnt = soup.find('div', class_='woocommerce-product-details__short-description')
    product_description = product_description_elemnt.text.strip() if product_description_elemnt else None
    
    product_price_element = soup.find('p', class_='price')
    product_price = product_price_element.find('span', class_='woocommerce-Price-amount amount').text.strip() if product_price_element else None
    
    product_attributes = []
    product_brand = ""  # Initialize the brand
    product_sku = ""  # Initialize the SKU
    
    # Find the brand element and extract the "title" attribute
    brand_container = soup.find('div', class_='pwb-single-product-brands')
    if brand_container:
        brand_links = brand_container.find_all('a')
        for brand_link in brand_links:
            brand_title = brand_link.get('title', "")
            if brand_title != "OFERTA" and brand_title != "Nuevo":
                product_brand = brand_title
                break
    
    # Find the SKU element and extract the SKU text
    sku_element = soup.find('span', class_='sku')
    if sku_element:
        product_sku = sku_element.text.strip()  # Get the text of the <span> element
    
    # Find the model using a regular expression
    model_pattern = r'[A-Z0-9/-]+'
    model_matches = re.findall(model_pattern, product_title)
    valid_models = [match for match in model_matches if re.search(r'[A-Z]', match) and re.search(r'\d', match)]
    product_model = valid_models[-1] if valid_models else None
    
    
    description_element = soup.find('div', class_='woocommerce-Tabs-panel--description')
    if description_element:
        attribute_table = description_element.find('table')
        if attribute_table:
            attribute_rows = attribute_table.find_all('tr')
            for row in attribute_rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    attribute_name = columns[0].text.strip()
                    attribute_value_element = columns[1]
                    attribute_value = extract_attribute_value(attribute_value_element)
                    formatted_attribute = format_attribute(attribute_name, attribute_value)
                    product_attributes.append(formatted_attribute)
    
    return product_title, product_price, product_attributes, product_brand, product_sku, product_model, product_description