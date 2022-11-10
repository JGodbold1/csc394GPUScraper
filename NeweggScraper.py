from bs4 import BeautifulSoup
import requests
import re


search_term = input("Which graphics card do you want to search for? ")
#search_term = "Graphics Cards"

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
	url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
	page = requests.get(url).text
	doc = BeautifulSoup(page, "html.parser")

	div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
	items = div.find_all(text=re.compile(search_term))

	for item in items:
		parent = item.parent
		if parent.name != "a":
			continue

		link = parent['href']
		next_parent = item.find_parent(class_="item-container")
		try:
			price = next_parent.find(class_="price-current").find("strong").string
			items_found[item] = {"price": int(price.replace(",", "")), "link": link}
		except:
			pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])


for gpu in search_term:
   
    for brand in gpu[0]:
        if brand == 'Nvidia' or 'AMD' or 'Intel':
            brand_name = 'Nvidia'
        


#counter = 0
Gpu_Master_List = []


for item in sorted_items:
    # counter += 1
    # GpuID = counter
    manufacturer = brand_name 
    store = "Newegg"
    name = item[0]
    price = f"${item[1]['price']}"
    memory = "Gigabytes"
    link = item[1]['link']
    list_of_Gpus = (store,name,manufacturer,memory,price,link)
    Gpu_Master_List.append(list_of_Gpus)
    #print(list_of_Gpus)
    
print(Gpu_Master_List)
