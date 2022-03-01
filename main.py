from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


driver =  webdriver.Chrome("./chromedriver")
driver.get("https://www.mercadolibre.com.co/")
search_bar = driver.find_element_by_class_name("nav-search-input")
search_bar.clear()
search_bar.send_keys("iphone12")
search_bar.send_keys(Keys.RETURN)

pagination = driver.find_element_by_xpath("//li[@class='andes-pagination__page-count']").text
pagination = [ int(s) for s in pagination.split() if s.isdigit()][0]

records = []

for _product in range(1,pagination+1):
    if _product != pagination:
        next_page_button = driver.find_element_by_css_selector("a[title='Siguiente']")

    title_products = driver.find_elements_by_xpath("//h2[@class='ui-search-item__title']")
    title_products = [     title.text  for title in title_products            ]


    price_products = driver.find_elements_by_xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-columns']//div[@class='ui-search-result__content-column ui-search-result__content-column--left']/div[1]/div//div[@class='ui-search-price__second-line']//span[@class='price-tag-amount']//span[2]")
    price_products = [ price.text for price in price_products   ]


    links_products = driver.find_elements_by_xpath("//div[@class='ui-search-item__group ui-search-item__group--title']//a[1]")
    links_products = [ link.get_attribute("href") for link in links_products   ]


    data_products = {

        "name_product":title_products,
        "price_product":price_products,
        "link_product":links_products

    }


    df =  pd.DataFrame(data_products)
    records.append(df)
    if _product != pagination:
        driver.execute_script("arguments[0].click()", next_page_button)

df = pd.concat(records)
df.to_csv("PRODUCTOS.csv")
time.sleep(4)
driver.close()