from bs4 import BeautifulSoup
import requests

with open ("index.html","r") as f:
    doc =BeautifulSoup(f,"html.parser")

#print(doc.prettify()) # print all file

# print(doc.title) # print title tag 

# print(doc.title.string) # print title string 
# print(doc.title.string.strip()) # print title string wihtout white space 

# doc.title.string= "first try" # create on title on object not on file 

# print(doc.title.string.strip()) 

# print(doc.find('p')) # find just the first tag 'p' 

#print(doc.find_all('p')) # find by all tag 'p' 
    
#print(len(doc.find_all('p'))) # print the lengh

#doc2 = doc.find_all('p')

#doc3 = doc.find_all('a')

#print(doc2)

#print(doc3)
    
# find the second p and the first a 

# print(doc.find_all('p')[1].find_all('a')[0])

url = "https://www.newegg.com/p/N82E16824012015?Item=N82E16824012015&recaptcha=pass"

result = requests.get(url)

#print(result.status_code)
print("The status is: " + str(result.status_code))


doc = BeautifulSoup(result.text,"html.parser")

#print(doc.prettify())

# we can search by id, attributes, calss_, ...
price_current_label = doc.find_all(class_ = 'price-current')[1]
price_current_text = price_current_label.find('strong').string.strip()


print(price_current_text)