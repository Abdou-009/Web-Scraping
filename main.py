from bs4 import BeautifulSoup as bf
import requests

with open ('ready-files/index.html',"r") as myfile:
    doc = bf(myfile,"html.parser")

# print(doc.title.string.strip())
# print(doc.find('p'))
# print(doc.findAll('a')[2].string.strip())

url ="https://www.newegg.com/msi-geforce-rtx-4070-ti-super-rtx-4070-ti-super-16g-gaming-x-slim/p/14-137-855?Item=14-137-855"
url_result = requests.get(url)
soup = bf(url_result.text,"html.parser")

# price = soup.findAll('strong')
price = soup.findAll(class_ ='price-current')[0]
price_text = price.find('strong').string
print(price_text)





