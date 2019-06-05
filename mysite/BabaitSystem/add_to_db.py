# -*- coding: utf-8 -*-
import requests
import urllib
import time


import requests
from bs4 import BeautifulSoup
#from Product import Product
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup
#from django.contrib.sites import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import webdriver
#from .models import Products,Suppliers,ProductBySupplier
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
import urllib
import time
import string
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.chrome.options import Options
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

from .models import ProductBySupplier,Products,Suppliers,product_in_zap
#chromedriver =r"C:\Users\User\Desktop\django.1\chromedriver.exe"

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1200x600')
#driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

results=[]
is_product=False
name_in_zap=''
def find_in_zap(makat):
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # driver = webdriver.Chrome(r"C:\Users\User\Desktop\chromeDriver\chromedriver.exe")

    # driver.get('https://www.zap.co.il/')
    #
    # text_area = driver.find_element_by_class_name("select2-selection__rendered")
    # text_area.click()
    # text_area = driver.find_element_by_class_name("select2-search__field")
    # text_area.send_keys(makat)
    # submit = driver.find_element_by_class_name("submitSearch").click()

    session = requests.Session()
    zap_example_url = "https://www.zap.co.il/search.aspx?keyword=" + makat
    try:
        # try get zap data
        req = session.get(zap_example_url)
    except urllib.error.HTTPError as e:
        # except for error
        print("Error while requesting url: {0}".format(e))

    # create new BeatifulSoup object
    try:
        bsObj = BeautifulSoup(req.text, "html.parser")
    except AttributeError as e:

        #results.update({'zap message': 'המוצר לא קיים בזאפ'})
        results.append('שגיאה')
        return results
        #return False
    get_search = bsObj.find('div', {'class': 'SearchResults'})
    if (get_search):
        results.append('יש יותר מתוצאה אחת לחיפוש הנ"ל')
        return results
    get_no_result=bsObj.find('div',{'class':'NoResultsTxt'})
    if(get_no_result):
        results.append('המוצר לא קיים בזאפ')
        return results

    get_stores = bsObj.find('div', {'class': 'StoresLines'})
    #if(get_stores == None):
     #   results.append('קרתה תקלה בהתחברות לזאפ')
     #   return results
    # if(get_stores is None):
    #     driver.get(zap_example_url)
    #     driver.find_element_by_class_name("ProdInfoTitle").click()
    #     req=session.get(driver.current_url)
    #     bsObj=BeautifulSoup(req.text,"html.parser")

    get_name = bsObj.find('div', {'class': 'ProdName'})
    conName = get_name.text
    name_in_zap = conName

    products = []
    countNoSupplier = 0
    chippestProductsNum = 7
    old_objects = product_in_zap.objects.filter(makat=makat)
    if (old_objects):
        for o in old_objects:
            o.delete()

        for x in range(0, chippestProductsNum):
            conPricer = get_stores.contents[1].contents[x + x + 1].contents[1].contents[7].contents[3]
            conPricer = conPricer.text.replace('₪', '').strip()
            conPricer = conPricer.replace(',', '')
            # conSupplier = get_stores.contents[1].contents[x+x+1].contents[1].contents[9].contents[3].contents[1]
            conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[3]
            if conSupplier.text.strip() == 'קנייה חכמה':
                conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[5]
            product_in_zap.objects.create(supplier=conSupplier.text, price=int(conPricer), makat=makat, product=conName)
        # results.update({'zap message':'המוצר נסרק בזאפ והתוצאות עודכנו במערכת'})
        is_product = True
        results.append('המוצר נסרק בזאפ והתוצאות עודכנו במערכת')
        return results

    for x in range(0, chippestProductsNum):
        conPricer = get_stores.contents[1].contents[x + x + 1].contents[1].contents[7].contents[3]
        conPricer = conPricer.text.replace('₪', '').strip()
        conPricer = conPricer.replace(',', '')
        # conSupplier = get_stores.contents[1].contents[x+x+1].contents[1].contents[9].contents[3].contents[1]
        conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[3]
        if conSupplier.text.strip() == 'קנייה חכמה':
            conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[5]
        product_in_zap.objects.create(supplier=conSupplier.text, price=int(conPricer), makat=makat, product=conName)
    # results.update({'zap message':'המוצר נסרק בזאפ והתוצאות עודכנו במערכת'})
    is_product = True
    results.append('המוצר נסרק בזאפ והתוצאות נוספו למערכת')
    return results
#
#
# def find_in_salielectric(makat):
#     flag=True
#
#     driver.get('https://www.salielectric.co.il/')
#     text_area = driver.find_element_by_id("right_srch_str")
#     text_area.click()
#     # text_area =
#     text_area.send_keys(makat)
#     text_area.send_keys(Keys.ENTER)
#
#     try:
#         driver.find_element_by_class_name("boxItem-wrap").click()
#         price_text = driver.find_element_by_id("total").text
#         price = price_text.replace(",", "")
#         name = driver.find_element_by_class_name("item-name").text
#         try:
#             old_object = ProductBySupplier.objects.get(makat=makat, supplier="sali electric")
#             old_object.price = int(price)
#             old_object.save()
#             results.append('המוצר נסרק בסאלי אלקטריק והותצאות עודכנו במערכת')
#         except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
#             ProductBySupplier.objects.create(supplier="sali electric", price=int(price), makat=makat, product=name)
#             is_product=True
#             results.append('המוצר נסרק בסאלי אלקטריק והותצאות נוספו למערכת')
#
#         #return flag
#
#     except NoSuchElementException as exception:
#         flag=False
#         #results.update({'sali electric message': 'המוצר לא נמצא בסאלי אלקטריק '})
#         results.append('המוצר לא קיים בסאלי אלקטריק')
#
#         #return flag
#
# def find_in_lastprice(makat):
#     flag=True
#     driver.get('https://www.lastprice.co.il/')
#
#     text_area = driver.find_element_by_id("searchBox")
#     text_area.click()
#     # text_area = driver.find_element_by_class_name("select2-search__field")
#     text_area.send_keys(makat)
#     submit = driver.find_element_by_class_name("btn-search").click()
#     try:
#
#         name = driver.find_element_by_class_name("degem").text
#         text_price = driver.find_element_by_class_name("price").text
#         price = text_price.replace("קנה עכשיו ב-", "")
#         price = price.replace("₪", "")
#         price = price.replace("*", "")
#         price = price.replace(",", "")
#         price = price.replace("רק", "")
#         price = price.replace("Plus", "")
#
#         price = price.split('או הגש הצעה מ-', 1)[0]
#         try:
#             old_object = ProductBySupplier.objects.get(makat=makat, supplier="last price")
#             old_object.price=int(price)
#             old_object.save()
#             results.append('המוצר נסרק בלאסט פרייס והותצאות עודכנו במערכת')
#         except (ObjectDoesNotExist,MultipleObjectsReturned) as e:
#             ProductBySupplier.objects.create(supplier="last price", price=int(price), makat=makat, product=name)
#             is_product=True
#             results.append('המוצר נסרק בלאסט פרייס והותצאות נוספו למערכת')
#
#
#
#
#
#         #return json.dumps(results)
#         return results
#     except NoSuchElementException as exception:
#         flag=False
#         #results.update({'last price message': 'המוצר לא נמצא בלאסט פרייס'})
#         results.append('המוצר לא קיים בלאסט פרייס')
#
#
#         #return json.dumps(results)
#         return results

def find_all(makat):
    results.clear()
    messege=find_in_zap(makat)
    #find_in_salielectric(makat)
    #messege=find_in_lastprice(makat)
    if(is_product):
        Products.objects.create(product=name_in_zap,makat=makat,ourPrice=0)
    return messege


