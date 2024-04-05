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
    name: str | None
    disc: str | None
    price: str | None
    Mileage: str | None
    Gearbox: str | None
    First_registration: str | None
    Fuel: str | None
    Power: str | None
    Type: str | None
    Engine_size: str | None
    


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
    try:
        text = html.css_first(sel).text()
        return clean_value(text) 
    except ArithmeticError:
        return None

# ================================================
# def extract_text_by_parent(html, class_name):
#     soup = BeautifulSoup(html, 'html.parser')
#     parent_div = soup.find('span', class_=class_name).parent
#     return parent_div.find('div', class_='css-1w91pbe').get_text(strip=True)

def get_all_items(html, sel):
    try:
        text = html.css(sel)
        return text 
    except ArithmeticError:
        return None


# ================================================


def parse_item_page(html):
    itmes = get_all_items(html, "dd.DataGrid_defaultDdStyle__3IYpG.DataGrid_fontBold__RqU01")
    new_item = item(        
        name = extract_text(html,"div.StageTitle_makeModelContainer__RyjBP"),
        disc = extract_text(html, "div.StageTitle_modelVersion__Yof2Z"),
        Type = clean_value(itmes[0].text()),
        Engine_size =  clean_value( itmes[14].text()),
        price = extract_text(html, "span.PriceInfo_price__XU0aF"),
        Mileage = extract_text(html, "div.VehicleOverview_itemText__AI4dA"),
        Gearbox =  clean_value( itmes[13].text()),
        First_registration =  clean_value( itmes[9].text()),
        Fuel =  clean_value( itmes[18].text()),
        Power =  clean_value( itmes[12].text())  
    )
    return asdict(new_item)

# ================================================

def clean_value(value):
    black_list = ["Item", "#","-1","-","*"]
    for char in black_list:
        if char in value:
            value = value.replace(char," ")
    return value.strip()

# ================================================

# print(html.css_first("title").text())

# div#id  || div.class
# products = html.css("div#search-results ul li")

# ================================================

def parse_search_page(html):
    products = html.css('article.cldt-summary-full-item.listing-impressions-tracking.list-page-item.ListItem_article__qyYw7')
    for product in products:
        yield urljoin("https://www.autoscout24.com/",product.css_first("a").attributes["href"])

# ================================================

# def get_item_detail_limk(url):
#     det_link =

# ================================================

def main():
    # baseUrl ="https://carvago.com/cars?page="
    baseUrl = 'https://www.autoscout24.com/lst/audi?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&desc=0&page=1&powertype=kw&search_id=92ysjj21de&sort=standard&source=listpage_pagination&ustate=N%2CU'
    products = []
    for i in range(1,2):
        print(f" Gathering Page Number: {i}")
        html=get_html(baseUrl)
        time.sleep(1)
        if html is False:
            break
        product_urls = parse_search_page(html)
        j=0
        for url in product_urls:
            print(f"item {j} collected !")
            html = get_html(url)
            products.append(parse_item_page(html))
            # append_to_csv(parse_item_page(html))
            time.sleep(0.1)
            j+=1

    # for product in products:
    #     print(asdict(product))
    # export_to_jsonfile(products)
    export_to_csv(products)

# ================================================

if __name__ == "__main__":
    main()