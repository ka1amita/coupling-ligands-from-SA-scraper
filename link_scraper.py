from selenium import webdriver
import re
from bs4 import BeautifulSoup


# logging set-up
import logging
logging.basicConfig(filename='scraper.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

# reading start pages from a file
startPages = []
with open("start_pages.txt", "r") as file:
    for line in file:
        startPages.append(line.strip())
        # the strip() method removes any leading or trailing whitespace 
# https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts
# https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts/organocatalysts
# https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts/organocatalysts?country=CZ&language=en&cmsRoute=products&cmsRoute=chemistry-and-biochemicals&cmsRoute=catalysts&cmsRoute=organocatalysts&page=2
# https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts/olefin-metathesis?country=CZ&language=en&cmsRoute=products&cmsRoute=chemistry-and-biochemicals&cmsRoute=catalysts&cmsRoute=olefin-metathesis&page=2


# link scraping set-up
# links = []
# def linkScraping(soup):
#     # function for extracting links from scraped tags with bs4 and saved as a list
#     # only links inside <a> tags with href containing "/product/" and having no children are saved; links are modified before saving
#     linkTags = soup.find_all("a", href=re.compile("/catalysts/"))
#     for linkTag in linkTags:
#         if not linkTag.find_all():
#             startPage = linkTag.get('href')
#             logging.debug("appended link "+ link)
#             startPages.append(link+"?country=CZ&language=en&cmsRoute=products&cmsRoute=chemistry-and-biochemicals&cmsRoute=catalysts&cmsRoute=organocatalysts&page=1")


# url input
# startPage = None
# startPage = "https://www.sigmaaldrich.com/CZ/en/products/chemistry-and-biochemicals/catalysts/buchwald-catalysts-and-ligands?country=CZ&language=en&cmsRoute=products&cmsRoute=chemistry-and-biochemicals&cmsRoute=catalysts&cmsRoute=buchwald-catalysts-and-ligands&page=1"
# if startPage == None:
#     startPage = input("start page: ")
# logging.debug("selected start page: "+startPage)

# selenium set-up
from selenium import webdriver


driver = webdriver.Chrome()
# driver.get(startPage)
# soup = BeautifulSoup(driver.page_source, 'html.parser')


# link scraping set-up
links = []
def linkScraping(soup):
    # function for extracting links from scraped tags with bs4 and saved as a list
    # only links inside <a> tags with href containing "/product/" and having no children are saved; links are modified before saving
    linkTags = soup.find_all("a", href=re.compile("/product/"))
    for linkTag in linkTags:
        if not linkTag.find_all():
            link = linkTag.get('href')
            logging.debug("appended link "+ link)
            links.append("https://www.sigmaaldrich.com"+link)


# scraping tags all pages from catalogue with selenium


# <div role="group" aria-label="Pagination Navigation"><button class="MuiButtonBase-root MuiButton-root jss639 MuiButton-outlined jss640 MuiButtonGroup-grouped MuiButtonGroup-groupedHorizontal MuiButtonGroup-groupedOutlined MuiButtonGroup-groupedOutlinedHorizontal MuiButtonGroup-groupedOutlined MuiButton-disableElevation Mui-disabled jss641 Mui-disabled" tabindex="-1" type="button" disabled="" aria-label="Go to previous page"><span class="MuiButton-label"><svg class="MuiSvgIcon-root jss56 jss642 jss643" focusable="false" viewBox="0 0 11 20" aria-hidden="true"><path d="M8.8 20a2.16 2.16 0 01-1.67-.78l-6.6-7.77a2.24 2.24 0 010-2.9L7.13.77a2.19 2.19 0 013.1-.24 2.25 2.25 0 01.24 3.14L5.1 10l5.37 6.33a2.24 2.24 0 01-.24 3.13A2.16 2.16 0 018.8 20z"></path></svg></span></button><div class="MuiButtonGroup-grouped MuiButtonGroup-groupedHorizontal MuiButtonGroup-groupedOutlined MuiButtonGroup-groupedOutlinedHorizontal MuiButtonGroup-groupedOutlined jss644" color="default" variant="outlined">Page 1 of 16</div><button class="MuiButtonBase-root MuiButton-root jss639 MuiButton-outlined jss640 MuiButtonGroup-grouped MuiButtonGroup-groupedHorizontal MuiButtonGroup-groupedOutlined MuiButtonGroup-groupedOutlinedHorizontal MuiButtonGroup-groupedOutlined MuiButton-disableElevation" tabindex="0" type="button" aria-label="Go to next page"><span class="MuiButton-label"><svg class="MuiSvgIcon-root jss56 jss642" focusable="false" viewBox="0 0 11 20" aria-hidden="true"

def numberOfPagesScraping(soup):
    numberOfPagesTag = soup.find("div",attrs={"aria-label":"Go to next page"})
    numberOfPagesTagText = numberOfPagesTag.get_text()
    numberOfPagesIndex = numberOfPagesTagText.find("1 of ")+len("1 of ")
    numberOfPages = numberOfPagesTagText[numberOfPagesIndex:]
    logging.debug("number of pages being scraped: "+str(numberOfPages))
    return int(numberOfPages)


for startPage in startPages:
    driver.get(startPage)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    numberOfPages = numberOfPagesScraping(soup)
    for pageNumber in range(1,numberOfPages):
        webPage = startPage[:-1]+str(pageNumber)
        logging.debug("web page being scraped: " + webPage)
        driver.get(webPage)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        linkScraping(soup)

driver.close()

# saving links inside a file

with open("links.txt", "w") as file:
    for link in links:
        file.write(link + "\n")
logging.debug("done!")



