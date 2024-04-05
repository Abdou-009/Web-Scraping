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



# ================================================


def parse_item_page(html):
    new_item = item(        
        Overview = extract_text(html,'p.text-zinc-600'),
        ListingName =extract_text(html, "h1"),
        ListingIcon =extract_text(html, 'img[src]'),
        ListingSellerName =extract_text(html, "p.text-2xl > a"),
        Built_By =extract_text(html, "p.text-2xl > a"),
        ListingRank ='extract_text(html, "")', # def fun
        ListingScrapeDate ='extract_text(html, "")', # current date
        ListingURL ='extract_text(html, "")', # url
        Side_Description ='extract_text(html, "")', # def func
        pic_urls ='extract_text(html, "")', # def fuc
        video_urls ='extract_text(html, "")' # Non
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


# ================================================

# def parse_search_page(html):
#     products = html.css('div.h-full')
#     for product in products:
#         a_tag = product.css_first("a")
#         if a_tag:
#             yield urljoin("https://marketplace.crowdstrike.com/", a_tag.attributes["href"])

# ================================================


# ================================================

def main():
    baseUrl ="https://marketplace.crowdstrike.com/listings/abnormal-cloud-email-security"
    products = []
    
    
    html=get_html(baseUrl)
    
    
    products.append(parse_item_page(html))
    # append_to_csv(parse_item_page(html))

    # for product in products:
    #     print(asdict(product))
    export_to_jsonfile(products)
    export_to_csv(products)

# ================================================

if __name__ == "__main__":
    main()