from selenium import webdriver
import re
from bs4 import BeautifulSoup


# logging set-up
import logging
logging.basicConfig(filename='scraper.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


# url input
startPage = None
startPage = "https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts"

if startPage == None:
    startPage = input("start page: ")
logging.debug("selected start page: "+startPage)

# selenium set-up

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# link scraping set-up

def partialLinkScraping(soup):
    # function for extracting links from scraped tags with bs4 and saved as a list
    # only links inside <a> tags with href containing "/product/" and having no children are saved; links are modified before saving
    partialLinks = []
    linkTags = soup.find_all("a", href=re.compile("/catalysts/"))
    for linkTag in linkTags:
        if not linkTag.find_all():
            partialLink = linkTag.get('href')
            logging.debug("appended link "+ partialLink)
            partialLinks.append("https://www.sigmaaldrich.com"+partialLink)
            return partialLinks


def fullLinkScraping(partialLinks):
    fullLinks = []
    for partialLink in partialLinks:
            driver.get(partialLink)
             
            nextButtons = driver.find_elements(By.TAG_NAME,"button")
            #  nextButton = driver.find_element_by_xpath("//div[@aria-label='Any time']/div[@class='mn-hd-txt'][text()='Any time']")
            #  nextButton = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '[@aria-label="Go to next page"]')))
            for nextButton in nextButtons:
                try:
                    nextButton.click()
                    url = driver.current_url
                except:
                    pass

             
            fullLink = str(url)[0:str(url).rfind("=")+1]
            fullLinks.append(fullLink)
    return fullLinks

driver = webdriver.Chrome()
driver.get(startPage)
soup = BeautifulSoup(driver.page_source, 'html.parser')

partialLinks = partialLinkScraping(soup)
fullLinks = fullLinkScraping(partialLinks)

driver.close()

# saving links inside a file

with open("start_pages.txt", "w") as file:
    for link in fullLinks:
        file.write(link + "\n")
logging.debug("done!")



