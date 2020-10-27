#Required imports for program
import requests
from bs4 import BeautifulSoup
import csv

#Function that gets date and time for csv file
def getDateTime():
    from datetime import datetime

    now = datetime.now()
    #When using time for file name change ":" into ";" without quotes
    #the ":" character cannot be used for file names
    dateTimeF = now.strftime("%m-%d-%Y_%H;%M;%S")

    return dateTimeF

#Web scraper function
def webScraper(URL, fileName):

    #Gets Date And Time For File Name
    dateTime = getDateTime()

    #Creates csv file
    with open(dateTime + fileName + ".csv", "w", newline = "") as f:
        thewriter = csv.writer(f)

        #Creates headers for csv file
        thewriter.writerow(["Sale?", "Name", "Prices, Shipping, and Deals"])

        #Code that gets product elements, name and price
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_= "list-wrap")
        neweggProductElements = results.findAll("div", class_= "item-cell")

        #Gets info for each individual product
        for neweggProductElements in neweggProductElements:

            #The try/except allows program to skip ads in results
            try:
                neweggProductTitle = neweggProductElements.find("a", class_= "item-title")
                product = neweggProductTitle.text.strip()
            except AttributeError:
                continue

            #Gets price, shipping, and sale info
            neweggProductPrice = neweggProductElements.find("ul", class_= "price")
            price = neweggProductPrice.text.strip()

            #Tells you if product is on sale or not
            #If a product is on sale the word "SALE" will appear before the product name
            #Otherwise the cell will be blank
            if "Sale Ends in" in price:
                thewriter.writerow(["SALE", product, price])
            else:
                    thewriter.writerow(["", product, price])

print("Scanning Newegg For Deals Please Wait")

#Put url in this function

#Sample
#webScraper("url and &page= goes here", "the file name goes here")
webScraper("https://www.newegg.com/p/pl?d=rtx+2080+graphics+card&PageSize=96", "_RTX_2080_Sales")
webScraper("https://www.newegg.com/p/pl?d=4k+monitor&PageSize=96", "_4k_Monitor_Sales")
webScraper("https://www.newegg.com/p/pl?d=rtx+2070+super+graphics+card&PageSize=96", "_RTX_2070_Super_Sales")