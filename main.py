import bs4
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

FORM_URL = "https://forms.gle/RM6v6Eut4omd1WrDA"
ZILLOW_LINK = "https://appbrewery.github.io/Zillow-Clone/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }


zillow = requests.get(ZILLOW_LINK, headers=HEADERS)
zillow.raise_for_status()
soup = bs4.BeautifulSoup(zillow.text, "html.parser")

#Get all prices
prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
formatted_prices = []
for price in prices:
    text_price = price.text
    new_price = re.split(pattern='[+ | / | ]+', string=text_price)
    formatted_prices.append(new_price[0])


#Get all addresses and links
addresses_and_links = soup.find_all(name="a", class_ ="StyledPropertyCardDataArea-anchor")
links = [links.get("href") for links in addresses_and_links]
formatted_addresses = [address.text.strip() for address in addresses_and_links]
final_addresses = []
for address in formatted_addresses:
    if "|" in address:
        temp_word = address.split(" | ")
        new_word = " ".join(temp_word)
        final_addresses.append(new_word)
    else:
        final_addresses.append(address)

#Initialize selenium for the form filling
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)
wait = WebDriverWait(driver, 5)

for i in range(len(final_addresses)): #for the entire length of addresses, can use links or amount of prices as well
    address = final_addresses[i]
    link = links[i]
    price = formatted_prices[i]

    #input address
    property_address = wait.until(ec.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    ActionChains(driver).move_to_element(property_address).perform()
    property_address.send_keys(address)

    #input price
    price_per_month = wait.until(ec.visibility_of_element_located((By.XPATH,
                                                                 "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    ActionChains(driver).move_to_element(price_per_month).perform()
    price_per_month.send_keys(price)

    #input link
    link_to_property = wait.until(ec.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    ActionChains(driver).move_to_element(link_to_property).perform()
    link_to_property.send_keys(link)

    #Submit all inputted info here
    submit = driver.find_element(By.CLASS_NAME, value="Y5sE8d")
    submit.click()

    #Resubmit to continue adding stuff to the sheets until all data has been scraped.
    successfully_sent = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "vHW8K")))
    if successfully_sent.is_displayed():
        driver.find_element(By.TAG_NAME, value="a").click()

print("All Done.")
driver.quit()




