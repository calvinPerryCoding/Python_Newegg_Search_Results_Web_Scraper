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

class webScraper:

    def webScraperEverything(URL, numberOfPages, fileName):

        #This will tell the user to wait
        print("Scanning Newegg For Deals Please Wait . . .")

        #Gets Date And Time For File Name
        dateTime = getDateTime()

        #Creates csv file
        with open(dateTime + fileName + ".csv", "w", newline = "") as f:
            thewriter = csv.writer(f)

            #Creates headers for csv file
            thewriter.writerow(["Sale?", "URL", "Name", "Current Price", "Shipping" , "Page URL"])

            #loops through number of pages
            pageNumber = 0
            for i in range(numberOfPages):     
                pageNumber = pageNumber + 1

                #Converts page number to string and adds it to url
                urlAndPageNumber = (URL + str(pageNumber))
         
                neweggProductElements = getElements.getProductElements(urlAndPageNumber)

                #Gets info for each individual product
                for neweggProductElements in neweggProductElements:
                
                    #This try/except allows program to skip ads in results
                    try:
                        neweggProductPriceElements = getElements.getPriceElements(neweggProductElements)
                        price = neweggProductPriceElements.text.strip()
                    
                        productName = getData.getProductName(neweggProductElements)
                        productURLFull = getData.getURL(neweggProductElements)
                        priceCurrent = getData.getCurrentPrice(neweggProductPriceElements)
                        priceShip = getData.getShippingPrice(neweggProductPriceElements)

                        #Gets Price Was
                        #priceWasFull = neweggProductPriceElements.find("span", class_= "price-was-data")
                        #priceWas = priceWasFull.text.strip()                    

                        #Gets Rating Elements
                        #neweggRatingElements = neweggProductElements.find("a", class_= "item-rating")

                        #ratingFull = neweggRatingElements.find("span", class_= "hid-text")
                        #rating = ratingFull.text.strip()
                        #print(rating)                                    
                    except AttributeError:
                        continue

                    output.showEverything(price, thewriter, productName, productURLFull, priceCurrent, priceShip, urlAndPageNumber)

    def webScraperSalesOnly(URL, numberOfPages, fileName):
        #This will tell the user to wait
        print("Scanning Newegg For Deals Please Wait . . .")

        #Gets Date And Time For File Name
        dateTime = getDateTime()

        #Creates csv file
        with open(dateTime + fileName + ".csv", "w", newline = "") as f:
            thewriter = csv.writer(f)

            #Creates headers for csv file
            thewriter.writerow(["Sale?", "URL", "Name", "Current Price", "Shipping" , "Page URL"])

            #loops through number of pages
            pageNumber = 0
            for i in range(numberOfPages):     
                pageNumber = pageNumber + 1

                #Converts page number to string and adds it to url
                urlAndPageNumber = (URL + str(pageNumber))
         
                neweggProductElements = getElements.getProductElements(urlAndPageNumber)

                #Gets info for each individual product
                for neweggProductElements in neweggProductElements:
                
                    #This try/except allows program to skip ads in results
                    try:
                        neweggProductPriceElements = getElements.getPriceElements(neweggProductElements)
                        price = neweggProductPriceElements.text.strip()
                    
                        productName = getData.getProductName(neweggProductElements)
                        productURLFull = getData.getURL(neweggProductElements)
                        priceCurrent = getData.getCurrentPrice(neweggProductPriceElements)
                        priceShip = getData.getShippingPrice(neweggProductPriceElements)

                        #Gets Price Was
                        #priceWasFull = neweggProductPriceElements.find("span", class_= "price-was-data")
                        #priceWas = priceWasFull.text.strip()                    

                        #Gets Rating Elements
                        #neweggRatingElements = neweggProductElements.find("a", class_= "item-rating")

                        #ratingFull = neweggRatingElements.find("span", class_= "hid-text")
                        #rating = ratingFull.text.strip()
                        #print(rating)                                    
                    except AttributeError:
                        continue

                    output.showSalesOnly(price, thewriter, productName, productURLFull, priceCurrent, priceShip, urlAndPageNumber)

class getElements:

    def getProductElements(urlAndPageNumberMethod):
        #Code that gets product elements, name and price
        page = requests.get(urlAndPageNumberMethod)

        #Use html.parser or #lxml in next line
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_= "list-wrap")
        neweggProductElementsMethod = results.findAll("div", class_= "item-cell")

        return neweggProductElementsMethod

    def getPriceElements(neweggProductElementsMethod):
        #Gets price, shipping, and sale info
        neweggProductPriceElementsMethod = neweggProductElementsMethod.find("ul", class_= "price")

        return neweggProductPriceElementsMethod

class getData:

    def getProductName(neweggProductElementsMethod):

        productNameFull = neweggProductElementsMethod.find("a", class_= "item-title")
        productNameMethod = productNameFull.text.strip()

        return productNameMethod

    def getURL(neweggProductElementsMethod):
        #Trying to get URL
        productURLFullMethod = neweggProductElementsMethod.find("a", href = True, text = True)

        return productURLFullMethod

    def getCurrentPrice(neweggProductPriceElementsMethod):
        #Gets current price
        priceCurrentWholeFull = neweggProductPriceElementsMethod.find("strong")
        #Gets decimal of current price
        priceCurrentDecimalFull = neweggProductPriceElementsMethod.find("sup")
        priceCurrentMethod = "$" + priceCurrentWholeFull.text.strip() + priceCurrentDecimalFull.text.strip()

        return priceCurrentMethod

    def getShippingPrice(neweggProductPriceElementsMethod):
        #Gets Shipping
        priceShipFull = neweggProductPriceElementsMethod.find("li", class_= "price-ship")
        priceShipMethod = priceShipFull.text.strip()

        return priceShipMethod

class output:

    def showEverything(priceMethod, thewriterMethod, productNameMethod, productURLFullMethod, priceCurrentMethod, priceShipMethod, urlAndPageNumberMethod):
        #This try/except fixes the following issue
        #Message='charmap' codec can't encode character '\ufffd' in position 88: character maps to <undefined>
        try:
            #Tells you if product is on sale or not
            #If a product is on sale the word "SALE" will appear before the product name
            #Otherwise the cell will be blank
            if "Sale Ends in" in priceMethod:
                thewriterMethod.writerow(["SALE", productURLFullMethod, productNameMethod, priceCurrentMethod, priceShipMethod, urlAndPageNumberMethod])
            else:
                thewriterMethod.writerow(["", productURLFullMethod, productNameMethod, priceCurrentMethod, priceShipMethod, urlAndPageNumberMethod])
        except:
            thewriterMethod.writerow(["ERROR: Something Went Wrong"])

    def showSalesOnly(priceMethod, thewriterMethod, productNameMethod, productURLFullMethod, priceCurrentMethod, priceShipMethod, urlAndPageNumberMethod):
        #This try/except fixes the following issue
        #Message='charmap' codec can't encode character '\ufffd' in position 88: character maps to <undefined>
        try:
            #Tells you if product is on sale or not
            #If a product is on sale the word "SALE" will appear before the product name
            #Otherwise the program will skip the product and continue
            if "Sale Ends in" in priceMethod:
                thewriterMethod.writerow(["SALE", productURLFullMethod, productNameMethod, priceCurrentMethod, priceShipMethod, urlAndPageNumberMethod])
        except:
            thewriterMethod.writerow(["ERROR: Something Went Wrong"])

#THIS IS THE MAIN PROGRAM

#Put url in this function
#Don't forget to add &page= to your url

#Sample
#webScraper.webScraperEverything("url and &page= goes here", number of pages go here, "the file name goes here")

webScraper.webScraperSalesOnly("https://www.newegg.com/p/pl?d=1080p+monitor+27+inch&N=4814&page=", 10,  "_1080p_monitor_SalesOnly")
webScraper.webScraperEverything("https://www.newegg.com/p/pl?d=1080p+monitor+27+inch&N=4814&page=", 10,  "_1080p_monitor_Everything")
                              
