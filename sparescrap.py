import xlwt
import requests
from bs4 import BeautifulSoup
import urllib
                                                                                                                                                                                                                                                                                                                                                                                    

head = []
itemslist = []

url = requests.get("http://spareshub.com")

soup = BeautifulSoup(url.text)

a = soup.find("div", {"class":"page-banners grid-container-spaced"})

b = a.find_all("div", {"class" : "grid12-2 banner"})

for x in b:
    head.append(x.find("a")["href"])

for y in head:
    i = 1
    while True:
        editedurl = str(y) + "?p=" + str(i)
        # print str(editedurl)
        suburl = requests.get(str(editedurl))
        subsoup = BeautifulSoup(suburl.text)
        check = subsoup.find("ol")
        # print check
        checkvalue = check.find("li", {"class":"current"})
        if int(checkvalue.string) != int(i):
            break
        d = subsoup.find("ul", {"class" : "category-products-grid"})
        e = d.find_all("h2")
        for z in e:
            if z.find("a")["href"] not in itemslist:
                itemslist.append(z.find("a")["href"])
        i = i + 1


data = []
itemdetailhead = {}
itemdetailhead['Product Name'] = 'Product Name'
itemdetailhead['Product Image'] = 'Product Image'
for w in itemslist:
    itemdetail = {}
    itempage = requests.get(w)
    itemsoup = BeautifulSoup(itempage.text)
    productname = itemsoup.find("div", {"class":"product-name"})
    productname = productname.find("h1").string
    itemdetail['Product Name'] = productname
    productimage = itemsoup.find("p", {"class": "product-image"})
    productimage = productimage.find("img")["src"]
    itemdetail['Product Image'] = productimage
    table = itemsoup.find("table", {"id":"product-attribute-specs-table"})
    rowlist = table.find_all("tr")
    for x in rowlist:
        heading = x.find("th").string
        datae = x.find("td").string
        itemdetailhead[heading] = heading
        itemdetail[heading] = datae
    data.append(itemdetail)
    print itemdetail

data.insert(0, itemdetailhead)
w = xlwt.Workbook()
ws = w.add_sheet('sheet1')
columns = list(data[0].keys()) 
for i, row in enumerate(data):
    for j, col in enumerate(columns):
        ws.write(i, j, row[col])

w.save('data.xls')
