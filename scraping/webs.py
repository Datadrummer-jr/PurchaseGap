
from playwright.sync_api import sync_playwright
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

prices_pymes = mf.read_json(r"..\\data\\prices_pymes.json")
prices_amazon = mf.read_json(r"..\\data\\amazon.json")

def Sinterceros():
    products = []
    prices = []
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
        
        prices_pymes["4"]["products"] = mf.list_to_dict(products, [ int(mf.you_type(''.join(mf.del_value(p[:-3],","))))  for p in prices])
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Guamay():
    products = []
    prices = []
    scrap = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/MEGACARIBE%20Megacaribe%20-%20Higiene%20y%20Limpieza%20-%20Productos%20para%20el%20cabello.html")

        web_poducts =  page.locator("p.fw-bold")
   
        for i in range(web_poducts.count()):
          scrap.append(web_poducts.nth(i).inner_text())

        products = [ scrap[i].strip().replace("\\", "") for i in range(len(scrap)) if i % 2 == 0]
        prices = [ float(scrap[i][:-3][1:].strip())for i in range(len(scrap)) if i % 2 != 0]
        prices_pymes["8"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Cubanearme():
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Cubanearme%20S.R.L_mercado..html")

        web_poducts =  page.locator("a.link-nav-a")

        web_prices =  page.locator("p.price-offer")

        for i in range(web_poducts.count()):
          products.append(web_poducts.nth(i).inner_text().strip())
        
        for j in range(web_prices.count()):
          prices.append(float(web_prices.nth(j).inner_text().replace(',', '.')[:-3]))
        
        prices_pymes["9"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")
      
        browser.close()

def Renova():
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Todos%20los%20productos%20%E2%80%93%20P%C3%A1gina%205%20%E2%80%93%20RENOVA%20S.R.L..html", wait_until="domcontentloaded")
        
        web_poducts =  page.locator("h2.woocommerce-loop-product__title")

        web_prices =  page.locator("bdi")

        for i in range(web_poducts.count()):
          products.append(web_poducts.nth(i).inner_text().strip())
        
        for j in range(web_prices.count()):
          prices.append(float(web_prices.nth(j).inner_text()[6:].replace(",", "")))
    
        prices_pymes["10"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Envios_Cuba(url: str, index: int):
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",   
            headless=True)
        page =  browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        
        web_poducts = page.locator("a.text-capitalize")

        web_prices =  page.locator("span.text-dark")

        for i in range(web_poducts.count()):
          products.append(web_poducts.nth(i).inner_text().strip())
        
        for j in range(web_prices.count()):
          precio = web_prices.nth(j).inner_text()
          if str(precio)[0] == "$":
           prices.append(float(precio[:-3][1:]))
    
        prices_pymes[str(index)]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")
        
        browser.close()

def Envios_Cuba_Isla():
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Mercado%20Isla%20de%20la%20Juventud%20-%20Envios%20Cuba,%20Paquetes%20a%20Cuba%20-%20El%20Pinero%20-%20Isla%20Juventud.html", wait_until="domcontentloaded")
        
        web_poducts = page.locator("a.text-capitalize")

        web_prices =  page.locator("span.text-dark") 

        for i in range(web_poducts.count()):
          products.append(web_poducts.nth(i).inner_text().strip())
        
        for j in range(web_prices.count()):
          precio = web_prices.nth(j).inner_text()
          if str(precio)[-3:] == "EUR":
           prices.append(float(precio[:-4]))

        prices_pymes["27"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")
      
        browser.close()

def Super_Fácil():
    products_with_prices = []
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("https://www.superfacil.cu/secretos-de-fragancias", wait_until="domcontentloaded")
        
        web_poducts = page.locator("div.prod-item-info")

        for i in range(web_poducts.count()):
          producto = web_poducts.nth(i).all()
          for j in producto:
             if j.inner_text()[-3:] == "cup":
               products_with_prices.extend(j.inner_text().split('\n'))
        products_with_prices = mf.del_value(products_with_prices)

        products.extend([products_with_prices[i] for i in range(len(products_with_prices)) if i % 2 == 0])
        prices.extend([float(products_with_prices[i][:-3].replace(",", "")) for i in range(len(products_with_prices)) if i % 2 != 0])
        prices_pymes["31"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Amazon(category: str, url=str):
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        
        web_products = page.locator("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")

        web_prices =  page.locator("span.p13n-sc-price") 

        n, m = web_products.count(), web_prices.count()

        if n != m:
            return False
        
        print((n,m))
        
        for i in range(web_products.count()):
           products.append(web_products.nth(i).inner_text().strip())

        for j in range(web_prices.count()):
           prices.append(float(web_prices.nth(j).inner_text()[3:]))
        
        prices_amazon[category].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_amazon, r"..\\data\\amazon.json")
         
        browser.close()


def Agruco():
    products = []
    prices = []
    with sync_playwright() as p:
        browser =  p.chromium.launch(
        headless=True
        )
        page =  browser.new_page()
        page.goto("", wait_until="domcontentloaded", timeout=60000)
        
        web_products = page.locator("a.d-block")

        web_prices =  page.locator("div.text-dark") 

        for i in range(web_products.count()):
          products.append(web_products.nth(i).inner_text().replace('\"', '').strip())
        
        for j in range(web_prices.count()):
          match = re.search(r"(\d+[.,]?\d*)\s*USD", web_prices.nth(j).inner_text())
          if match:
            prices.append(float(match.group(1).replace(",", ".")))
    
        prices_pymes["19"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def El_Gelato():
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",  
            headless=True)
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/FireShot/El%20Gelato_1.html", timeout=60000)
        
        web_products = page.locator("div.mb-2") #class="text-sm xs:text-base md:text-lg text-foreground font-medium line-clamp-2 h-[3rem]"
  
        def parser(text:str, ):
           lista = text.split()
           for i in range(len(lista)):
              if lista[i] == "CUP":
                 return " ".join(lista[:i-1]), float(lista[i-1].replace(",", ""))
              else:
                 continue     
  
        for i in range(web_products.count()):
          product = parser(web_products.nth(i).inner_text().strip())
          if product and len(product) == 2 and product[1] != 0:
             products.append(product[0])
             prices.append(product[1])
      
        prices_pymes["21"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Pymesbulevar():
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",   
            headless=True)
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Charcuter%C3%ADa%20Cuervo's.html", wait_until="domcontentloaded", timeout=60000)
        
        web_products = page.locator("h4.mat-body-2")

        web_prices =  page.locator("p.ng-star-inserted") 

        for i in range(web_products.count()):
          products.append(web_products.nth(i).inner_text().strip().upper())
        
        for j in range(web_prices.count()):
            price = web_prices.nth(j).inner_text().strip()
            if price[-3:] == "CUP":
              prices.append(float(price[:-4].replace(".","").replace(",",".")))
            else:
               continue
    
        prices_pymes["26"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def Elyerromenu():
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",   
            headless=True)
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Garaje%20minorista%20-%20Zamour%20_%20El%20Yerro%20Men%C3%BA.html", wait_until="domcontentloaded", timeout=60000)
        
        web_products = page.locator("div.pt-28 ") 

        for i in range(web_products.count()):
          producto = web_products.nth(i).inner_text().replace('\n', " " ).replace(" ... ", " ").strip().split(" ")[:-1]
          products.append(" ".join(producto[:-1]))
          prices.append(float(producto[-1].replace(",","")))
    
        prices_pymes["27"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()

def mercatoria():
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",  
            headless=True)
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/Mercatoria%20-%20Env%C3%ADos%20a%20Cuba_%20El%20futuro%20es%20ahora,%20al%20alcance%20de%20un%20click.html", timeout=120000)
        
        web_products = page.locator("p.css-m6tgpv") #MuiTypography-root MuiTypography-h3 mt-0 md:mt-2 css-p9dpgq
        print(web_products.first.inner_text())
        # def parser(text:str, ):
        #    lista = text.split()
        #    for i in range(len(lista)):
        #       if lista[i] == "CUP":
        #          return " ".join(lista[:i-1]), float(lista[i-1].replace(",", ""))
        #       else:
        #          continue     
  
        # for i in range(web_products.count()):
        #   product = parser(web_products.nth(i).inner_text().strip())
        #   if product and len(product) == 2 and product[1] != 0:
        #      products.append(product[0])
        #      prices.append(product[1])
      
        # prices_pymes["21"]["products"].update(mf.list_to_dict(products, prices))
        # mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()


def biznecubano():
    products = []
    prices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",  
            headless=True)
        page =  browser.new_page()
        page.goto("file:///D:/download/Download_Edge/305%20Ventas%20Habana%20_%20305%20Venta$Habana.html", timeout=60000)
        
        web_products = page.locator("a.font-weight-bold") 
        web_prices = page.locator("div.text-dark")

        for i in range(5,web_products.count()):
          products.append(web_products.nth(i).inner_text().strip().upper())

        for j in range(web_prices.count()):
            price = web_prices.nth(j).inner_text().strip().upper()[:-4]
            if price[0:5] == "DESDE":
               prices.append(float(price[5:]))
            else:
               prices.append(float(price))
      
        prices_pymes["39"]["products"].update(mf.list_to_dict(products, prices))
        mf.save_json(prices_pymes, r"..\\data\\prices_pymes.json")

        browser.close()
   

if __name__ == "__main__":
    # Amazon("Productos de Cuidado Personal", "file:///C:/Users/Joswald/Downloads/Amazon Los más vendidos_ Mejor Productos de Cuidado Personal_2.htm")
    Envios_Cuba("https://www.envioscuba.com/villaclara/Villa%20Clara", 42)
    pass


  

