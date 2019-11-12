from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
This file goes to Smogon's OU competitive pokedex and scrapes all the movesets from it,
allowing the bot to access almost all the likely movesets in a given OU match.
'''


# loading the dex page and putting it into r
def render_page(link_url, button=False):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link_url)

    # If the page has an export button, click all of them so bot can access importables
    if button:
        buttons = driver.find_elements_by_class_name("ExportButton")
        for button in buttons:
            button.click()
    rend = driver.page_source
    driver.quit()
    return rend


# URL of the page that contains all web pages of pokemon with OU analyses
url = "https://www.smogon.com/dex/sm/formats/ou/"
r = render_page(url)

# Creating soup object for page
soup = BeautifulSoup(r, "html.parser")
dexData = soup.find_all("div", class_="PokemonAltRow-name")

# Defining base link to add all new links to
baseLink = "https://www.smogon.com"

# List containing links for each mon
monLinks = [x.find("a").get("href") for x in dexData]

# List containing all pokemon movesets
monData = []

outerIndex = 0
while outerIndex < len(monLinks):
    link = monLinks[outerIndex]

    # Getting the page of the pokemon
    r = render_page(baseLink + link, True)
    name = link[16:len(link) - 1]

    # Adding a new dict (key being pokemon's name) to the list
    monData.append({name: []})
    soup = BeautifulSoup(r, "html.parser")

    # Finding all instances of a given moveset on a web page
    dexData = soup.find_all("div", class_="BlockMovesetInfo")

    # Get importable for each moveset and add it to the dict of the pokemon
    for entry in dexData:
        monSet = entry.find("textarea").get_text()
        monData[outerIndex][name].append(monSet)
    outerIndex = outerIndex + 1
