import httpx
from selectolax.parser import HTMLParser 
import time
from urllib.parse import urljoin 
from dataclasses import asdict, dataclass, fields
import json
import csv


# ================================================


@dataclass
class item:
    name : str  | None
    item_number: str | None
    price: str | None 
    raring: float |  None


# ================================================

def export_to_jsonfile(products):
    with open("products.json","w",encoding="utf-8") as f:
        json.dump(products,f, ensure_ascii=False,indent=4)
    print(" saved json file successful")
# ================================================

def export_to_csv(products):
    field_name = [field.name for field in fields(item)]
    with open("products.csv","w") as f:
        writer = csv.DictWriter(f,field_name)
        writer.writeheader()
        writer.writerows(products)
    print(" saved csv file successful")

# ================================================

def append_to_csv(products):
    field_name = [field.name for field in fields(item)]
    with open("products.csv","a") as f:
        writer = csv.DictWriter(f,field_name)
        writer.writerow(products)
    print(" update csv file successful")

# ================================================
def get_html(url, **kwargs):
    
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    if kwargs.get("page"):
        resp = httpx.get(url + str(kwargs.get("page")), headers=headers, follow_redirects=True)
    else:
        resp = httpx.get(url, headers=headers, follow_redirects=True)

    print(resp.status_code)

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} This is Limit Pages!")
        return False
    
    html = HTMLParser(resp.text)
    return html

# ================================================

def extract_text(html, sel):
    # try:
    #     element = html.css_first(sel)
    #     if element:
    #         text = element.text()
    #         return clean_value(text)
    #     else:
    #         return "None"  
    # except ArithmeticError:
    #     return None
    try:
        text = html.css_first(sel).text()
        return clean_value(text) 
    except ArithmeticError:
        return None

# ================================================

def parse_item_page(html):
    new_item = item(
        name= extract_text(html,"h1#product-page-title"),
        item_number= extract_text(html, "span#product-item-number"),
        price= extract_text(html, "span#buy-box-product-price"),
        raring=extract_text(html, "span.cdr-rating__number_15-0-0")
    )
    return asdict(new_item)

# ================================================

def clean_value(value):
    black_list = ["Item", "#"]
    for char in black_list:
        if char in value:
            value = value.replace(char,"")
    return value.strip()

# ================================================

# print(html.css_first("title").text())

# div#id  || div.class
# products = html.css("div#search-results ul li")

# ================================================

def parse_search_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    #print all elements
    # for product in products:
    #     item ={

    #         # "name" : product.css_first(".Xpx0MUGhB7jSm5UvK2EY").text(), # call by class 
    #         # "price" : product.css_first("span[data-ui=sale-price]").text() # call by att
    #         "name" : extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"), 
    #         "price" : extract_text(product, "span[data-ui=sale-price]"),
    #         "savings" : extract_text(product, "div[data-ui=savings-percent-variant2]"),
    #     }
    #     yield item

    for product in products:
        yield urljoin("https://www.rei.com/",product.css_first("a").attributes["href"])


# ================================================

def main():
    baseUrl ="https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    products = []
    for i in range(1,2):
        print(f" Gathering Page Number: {i}")
        html=get_html(baseUrl,page = i)
        time.sleep(1)
        if html is False:
            break
        product_urls = parse_search_page(html)
        for url in product_urls:
            print(url)
            html = get_html(url)
            products.append(parse_item_page(html))
            # append_to_csv(parse_item_page(html))
            time.sleep(0.1)

    # for product in products:
    #     print(asdict(product))
    export_to_jsonfile(products)
    export_to_csv(products)

# ================================================

if __name__ == "__main__":
    main()