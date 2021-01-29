from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests

try:
    source = requests.get('https://yugiohprices.com/').text
except requests.exceptions.ConnectionError:
    print("Connection refused. Potentially too many requests to URL")

# uses lxml parses
soup = BeautifulSoup(source, 'lxml')
# parses data from html file where the card info can be found
article = soup.find_all('tr', class_= 'content')
allcards = soup.find_all('p')
plotAllBoolean = False

yourCard = input("Enter your card name. If you want all cards plotted, type ALLCARDS: ")
if (yourCard == "ALLCARDS"):
    plotAllBoolean = True

nameList = []
price = []
percent = []

for obj in allcards:
    string = obj.text
    string = string.replace("\n", " ")
    # excludes information about the site not relevant to the card data
    if ((string.count("Ebay") == 0) and (string.count("Home") == 0) and (string.count("Javascript") == 0)):
        cardName = ""
        cardchar = ""
        doublespace = 0

        for i in range(len(string) - 2):
             cardchar = (str(string[i + 2]))
             if (cardchar == " " and doublespace == 1):
                doublespace = 0
                break
             elif (cardchar == " " and doublespace == 0):
                 doublespace = 1
             else: 
                 doublespace = 0
             cardName += cardchar

        # inserts the data into the name, percent, or price list based on its first character
        if (cardName[:1].isdigit() == True):
            price.append(cardName)
        elif (cardName[:1] == "+" or cardName[:1] == "-"):
            percent.append(cardName)
        else:
            nameList.append(cardName)

# removes all the additional spaces after the data has been parsed into the correct list
nameList = [x.strip(" ") for x in nameList]
price = [x.strip(" ") for x in price]
percent = [x.strip(" ") for x in percent]

# searches through the name list and tries to find all similar cards. If it is true, 
# it prints them out
cardFound = False
# lists that are made up of ONLY the data similar to user input
plottedCardNames = []
plottedCardPrices = []
plottedCardPercents = []

print("Printing all cards similar to your input")
for eachcard in nameList:
    if (eachcard.find(yourCard) != -1):
        cardFound = True
        yourCardIndex = nameList.index(eachcard)
        
        plottedCardNames.append(nameList[yourCardIndex])
        plottedCardPrices.append(price[yourCardIndex])
        plottedCardPercents.append(percent[yourCardIndex])

if (cardFound == False and plotAllBoolean == False):
    print("Card was not found, or is not changing a significant amount in price")
else:
    if (plotAllBoolean == True):
        # prints every card that has major changes in value
        plot = PrettyTable()
        plot.add_column("Card Name", nameList)
        plot.add_column("Percent Change", percent)
        plot.add_column("Current Price", price)
        print(plot)   

    else:
        # prints out only cards with names similar to user input
        plot = PrettyTable()
        plot.add_column("Card Name", plottedCardNames)
        plot.add_column("Percent Change", plottedCardPercents)
        plot.add_column("Current Price", plottedCardPrices)
        print(plot)

