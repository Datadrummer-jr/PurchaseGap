
from playwright.sync_api import sync_playwright
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

products = []
prices = []

prices_pymes = mf.read_json(r"..\\data\\prices_pymes.json")

def main():
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Sinterceros.html")

        web_poducts =  page.locator("h3.font-medium")
        
        web_prices =  page.locator("p.font-medium")

        for i in range(web_poducts.count()):
          products.append(web_poducts.nth(i).inner_text())
        
        for j in range(web_prices.count()):
          prices.append(web_prices.nth(j).inner_text())

        browser.close()

if __name__ == "__main__":
    main()
    prices_pymes["5"]["products"] = mf.list_to_dict(products[1:], [ int(mf.you_type(''.join(mf.del_value(p[:-3],","))))  for p in prices])
    mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")


  

