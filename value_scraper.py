from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

# logging set-up
import logging
# logging.basicConfig(filename='scraper.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.info)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# warning set-up
import warnings

driver = webdriver.Chrome()

# reading links from a file
links = []
with open("links.txt", "r") as file:
    for line in file:
        links.append(line.strip())
        # the strip() method removes any leading or trailing whitespace 

# TODO refactor into OBJECTS with CLASS Catalysts

# definition of empty lists for scraped values
# names=[]
# casNumbers=[]
# reactionTypes = []
failed = []

#  scraping of the name
def nameScraping(soup):
    # function that scrapes name
    try:
        name_tag = soup.find(id="product-name")
        name = name_tag.get_text()
        logging.info("\nname: " +name)
        return name
    except AttributeError:
        failed.append(link)
        warnings.warn("no name inside a link {}".format(link))
        # logging.debug("no name inside a link {}".format(link))
        return "not found"
    
def casScraping(soup):
        # function that scrapes CAS number
    try:
        casTag = soup.find("div", text=re.compile("CAS Number")).find_next_sibling('div').find("a") # the actual CAS is the (only) sibling to the tag with "CAS Number" string
        logging.debug("link is: "+ str(casTag))
        casNumber = casTag.get_text()
        logging.info("CAS: "+ casNumber)
        pattern = re.compile("[0-9]+\-[0-9]{2}\-[0-9]") # CAS RN is separated by hyphens into three parts, the first consisting from two up to seven digits,[7] the second consisting of two digits, and the third consisting of a single digit serving as a check digit
        assert pattern.fullmatch(casNumber)      
        return casNumber
    except AttributeError:
        failed.append(link)
        warnings.warn("no CAS inside a link {}".format(link))
        # logging.debug("no CAS inside a link {}".format(link))
        return "not found"
    
# TODO Pd (or other Metals) in Molecular FOrmula function

def reactionScraping(soup):
        # function that scrapes reaction type
    try:
        reactionTags = soup.find_all("span", text=re.compile("reaction type:"))
        # soup.find("div", text=re.compile("CAS Number")).find_next_sibling('div').find("a") # the actual CAS is the (only) sibling to the tag with "CAS Number" string
        logging.debug("links are: "+ str(reactionTags))
        reactions = []
        for reactionTag in reactionTags:
            reaction = reactionTag.get_text().split(":")[-1].strip()
            reactions.append(reaction)
            logging.info("reaction "+str(len(reactions))+" : "+reaction)
        return reactions
    except AttributeError:
        failed.append(link)
        warnings.warn("no reaction type inside a link {}".format(link))
        # logging.debug("no reaction type inside a link {}".format(link))
        return ["not found"]

import csv
data = ["name", "cas", "reactions type"]
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(data)  

for link in links:
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = nameScraping(soup)
    casNumber = casScraping(soup)
    reactionTypes = reactionScraping(soup)
    names = []
    if name not in names:
        names.append(name)
        data = [name, casNumber, reactionTypes]
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)  

driver.close()

# data = []
# data.append(["name", "cas", "reactions type"])
# for entry in names:
#     data.append([names[entry], casNumbers[entry], reactionTypes[entry]])

# logging.info("writing data")
# with open("data.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerows(data)

logging.info("writing failed links")

with open("failed_links.txt", "w") as file:
    for item in failed:
        file.write(str(item) + "\n")

logging.info("done!")