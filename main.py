import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

response = requests.get("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
soup = BeautifulSoup(response.text , "html.parser")

file_name = soup.find("div" , attrs={"class":"page-header action"}).get_text().strip()
file_name +=".csv"

books = soup.find_all("li",attrs={"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
def get_number(number):
    if number == 'One' :
        return 1
    if number == 'Two':
        return 2
    if number == 'Three':
        return 3
    if number == 'Four':
        return 4
    if number == 'Five':
        return 5

books_names = []
books_prices = []
books_rating = []

for book in books :
    books_names.append(book.find("img").get("alt"))
    books_prices.append(float(book.find("p" , attrs={"class":"price_color"}).get_text().split("Â£")[1]))
    books_rating.append(get_number(book.find("article" , attrs={"class":"product_pod"}).find("p").get("class")[1]))

lists = [books_names,books_prices,books_rating]
exported = zip_longest(*lists)
with open(file_name , "w" , encoding="utf-8") as csv_file :

    wr = csv.writer(csv_file)
    wr.writerow(["book Name" , "Price","rating"])
    wr.writerows(exported)

    wr.writerow(["******" ,"******" ])
    wr.writerow(["Price Average" ,"Rating Average" ])
    Price_Average = sum(books_prices) / len(books_prices)
    Price_Rating = sum(books_rating) / len(books_rating)
    wr.writerow([Price_Average, Price_Rating])

