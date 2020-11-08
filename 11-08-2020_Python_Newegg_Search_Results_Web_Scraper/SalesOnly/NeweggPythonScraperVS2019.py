#Required imports for program
import requests
from bs4 import BeautifulSoup
import csv

#Progress Bar Credit
#http://qpleple.com/add-progress-bars-to-your-python-loops/
from progressbar import ProgressBar
pbar = ProgressBar()

#Function that gets date and time for csv file
def getDateTime():
    from datetime import datetime

    now = datetime.now()
    #When using time for file name change ":" into ";" without quotes
    #the ":" character cannot be used for file names
    dateTimeF = now.strftime("%m-%d-%Y_%H;%M;%S")

    return dateTimeF

#Web scraper function
def webScraper(URL, numberOfPages, fileName):

    #Gets Date And Time For File Name
    dateTime = getDateTime()

    #Creates csv file
    with open(dateTime + fileName + ".csv", "w", newline = "") as f:
        thewriter = csv.writer(f)

        #Creates headers for csv file
        thewriter.writerow(["Sale?", "URL", "Name", "Current Price", "Shipping" , "Page URL"])

        #loops through number of pages
        pageNumber = 0
        for i in pbar(range(numberOfPages)):     
            pageNumber = pageNumber + 1
            #Converts page number to string and adds it to url
            urlAndPageNumber = (URL + str(pageNumber))

            #Code that gets product elements, name and price
            page = requests.get(urlAndPageNumber)
            #html.parser
            #lxml
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", class_= "list-wrap")
            neweggProductElements = results.findAll("div", class_= "item-cell")

            #Gets info for each individual product
            for neweggProductElements in neweggProductElements:
                
                #This try/except allows program to skip ads in results
                try:
                    neweggProductTitle = neweggProductElements.find("a", class_= "item-title")
                    product = neweggProductTitle.text.strip()

                    #Trying to get URL
                    productURLFull = neweggProductElements.find("a", href = True, text = True)
                    productURL = productURLFull

                    #Gets price, shipping, and sale info
                    neweggProductPriceElements = neweggProductElements.find("ul", class_= "price")
                    price = neweggProductPriceElements.text.strip()

                    #Gets current price
                    priceCurrentWholeFull = neweggProductPriceElements.find("strong")
                    #Gets decimal of current price
                    priceCurrentDecimalFull = neweggProductPriceElements.find("sup")
                    priceCurrent = "$" + priceCurrentWholeFull.text.strip() + priceCurrentDecimalFull.text.strip()

                    #Gets Price Was
                    #priceWasFull = neweggProductPriceElements.find("span", class_= "price-was-data")
                    #priceWas = priceWasFull.text.strip()

                    #Gets Shipping
                    priceShipFull = neweggProductPriceElements.find("li", class_= "price-ship")
                    priceShip = priceShipFull.text.strip()

                    #Gets Rating Elements
                    #neweggRatingElements = neweggProductElements.find("a", class_= "item-rating")

                    #ratingFull = neweggRatingElements.find("span", class_= "hid-text")
                    #rating = ratingFull.text.strip()
                    #print(rating)

                except AttributeError:
                    continue

                #This try/except fixes the following issue
                #Message='charmap' codec can't encode character '\ufffd' in position 88: character maps to <undefined>
                try:
                    #Tells you if product is on sale or not
                    #If a product is on sale the word "SALE" will appear before the product name
                    #Otherwise the program will skip the product and continue
                    if "Sale Ends in" in price:
                        thewriter.writerow(["SALE", productURLFull, product, priceCurrent, priceShip, urlAndPageNumber])
                    else:
                        continue
                except:
                    thewriter.writerow(["ERROR: Something Went Wrong"])

#Put url in this function
#Don't forget to add &page= to your url

#Sample
#webScraper("url and &page= goes here", number of pages go here, "the file name goes here")

print("Scanning Newegg For Deals Please Wait")

#Main program that calls the function
webScraper("https://www.newegg.com/p/pl?d=1080p+monitor&page=", 78,  "_1080p_monitor_Sales")
