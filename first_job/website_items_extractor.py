import httpx
from selectolax.parser import HTMLParser 
import time
from urllib.parse import urljoin 
from dataclasses import asdict, dataclass, fields
import json
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# ================================================

@dataclass
class item:
    Overview: str | None
    ListingName: str | None
    ListingIcon: str | None
    ListingSellerName: str | None
    Built_By: str | None
    ListingRank: str | None
    ListingScrapeDate: str | None
    ListingURL: str | None
    Side_Description: str | None
    pic_urls: str | None
    video_urls: str | None
    


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
        selected_element = html.css_first(sel)
        if selected_element:
            return selected_element.text(deep=True).strip()
        else:
            print("No element found matching the CSS selector:", sel)
            return None
    except Exception as e:
        print("Error extracting text:", e)
        return None


# ================================================

def get_all_items(html, sel):
    try:
        text = html.css(sel)
        return text 
    except ArithmeticError:
        return None


# ================================================


def parse_item_page(html):
    listing_name = extract_text(html, "h1")
    new_item = item(        
        Overview = extract_text(html,'p.text-zinc-600'),
        ListingName = listing_name,
        ListingIcon = get_img_link(html, "Listing logo icon"),
        ListingSellerName = extract_text(html, "p.text-2xl > a"),
        Built_By = extract_text(html, "p.text-2xl > a"),
        ListingRank = get_order(listing_name), 
        ListingScrapeDate = get_current_date(), 
        ListingURL ='Null', # url
        Side_Description ='Null', # def func
        pic_urls ='Null', # def fuc
        video_urls ='Null '# Non
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
def clean_link(value):
    black_list = ["//"]
    for char in black_list:
        if char in value:
            value = value.replace(char," ")
    return value.strip()
# ================================================

def get_img_link(html_content, alt_pic):
    img_tags = html_content.tags('img')

    for img_tag in img_tags:
        if img_tag.attributes.get('alt') == alt_pic:
            image_url = img_tag.attributes.get('src')
            return clean_link(image_url)

    print(f"Image with alt='{alt_pic}' not found")
    return None
# ================================================

def parse_search_page(html):
    products = html.css('div.h-full')
    for product in products:
        a_tag = product.css_first("a")
        if a_tag:
            yield urljoin("https://marketplace.crowdstrike.com/", a_tag.attributes["href"])

# ================================================
def get_order(name_wanted):
    url = 'https://marketplace.crowdstrike.com/listings?categories=cloud-security'
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    list_items = html.select('div.h-full')

    list_names = []
    for item in list_items:
        name_element = item.select('h4')
        for h4 in name_element:
            list_names.append(h4.text.strip())  

    order = 1
    for name in list_names:
        if name.lower() == name_wanted.lower():  
            order_message = f' order on list {order}'
            return order_message
        order += 1
    print(f"Item '{name_wanted}' does not exist ")
    return None



def get_current_date():
    return datetime.now().date()
# ================================================

def main():
    baseUrl ="https://marketplace.crowdstrike.com/"
    products = []
    
    
    html=get_html(baseUrl)
    time.sleep(0.1)
    
    product_urls = parse_search_page(html)
    j=0
    for url in product_urls:
        html = get_html(url)
        products.append(parse_item_page(html))
        print(f"item {j} collected !")
        # append_to_csv(parse_item_page(html))
        time.sleep(0.01)
        j+=1

    # for product in products:
    #     print(asdict(product))
    # export_to_jsonfile(products)
    export_to_csv(products)

# ================================================

if __name__ == "__main__":
    main()