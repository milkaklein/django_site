# -*- coding: utf-8 -*-
import requests
import urllib
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
#from Product import Product

from bs4 import BeautifulSoup

import os
from bs4 import BeautifulSoup
#from django.contrib.sites import requests
import json
from django.http import HttpResponse, HttpResponseRedirect

#from .models import Products,Suppliers,ProductBySupplier
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
import urllib
import time
import string
import asyncio
from pyppeteer import launch
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

from .models import ProductBySupplier,Products,Suppliers,product_in_zap,price_in_past
from requests_html import HTMLSession

results=[]
is_product=False
name_in_zap=''
def find_in_zap(makat):


    session = requests.Session()
    zap_example_url = f"https://www.zap.co.il/search.aspx?keyword={makat}"
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

        results.append('שגיאה בהתחברות לזאפ')
        return
    get_search = bsObj.find('div', {'class': 'FiltersMain'})
    if (get_search):
        results.append('יש יותר מתוצאה אחת לחיפוש הנ"ל')
        return
    get_no_result=bsObj.find('div',{'class':'NoResultsTxt'})
    if(get_no_result):
        results.append('המוצר לא קיים בזאפ')
        return
    get_not_makat=bsObj.find('div',{'class':'MultiFilters'})
    if(get_not_makat):
        results.append('החיפוש לא כלל דגם תקין')
        return

    get_stores = bsObj.find('div', {'class': 'StoresLines'})
    if (len(get_stores)<7):
        chippestProductsNum=len(get_stores)
    else:
        chippestProductsNum=7


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
            conSupplier=conSupplier.text.replace("ב-","")
            product_in_zap.objects.create(supplier=conSupplier, price=int(conPricer), makat=makat, product=conName)
        # results.update({'zap message':'המוצר נסרק בזאפ והתוצאות עודכנו במערכת'})
        is_product = True
        results.append('המוצר נסרק בזאפ והתוצאות עודכנו במערכת')
        return

    for x in range(0, chippestProductsNum):
        conPricer = get_stores.contents[1].contents[x + x + 1].contents[1].contents[7].contents[3]
        conPricer = conPricer.text.replace('₪', '').strip()
        conPricer = conPricer.replace(',', '')
        # conSupplier = get_stores.contents[1].contents[x+x+1].contents[1].contents[9].contents[3].contents[1]
        conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[3]
        if conSupplier.text.strip() == 'קנייה חכמה':
            conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[5]
        conSupplier = conSupplier.text.replace("ב-", "")
        product_in_zap.objects.create(supplier=conSupplier, price=int(conPricer), makat=makat, product=conName)
    # results.update({'zap message':'המוצר נסרק בזאפ והתוצאות עודכנו במערכת'})
    is_product = True
    results.append('המוצר נסרק בזאפ והתוצאות נוספו למערכת')
    return


def find_in_salielectric(makat):



    session = HTMLSession()
    page = session.get('https://www.salielectric.co.il/items.asp?Qsearch=' + makat)
    get_price = page.html.find('.priceholder', first=True)
    get_name = page.html.find('.item-name', first=True)
    # get_details=get_details.find('.priceholder',first=True)

    if(get_price and get_name):
        get_price=get_price.text
        get_name = get_name.text
        get_price = get_price.replace(",", "")
        try:
            old_object = ProductBySupplier.objects.get(makat=makat, supplier="sali electric")
            if(old_object.price<int(get_price)):
                price_in_past.object.create(makat=makat,date=old_object.date,price=old_object.price,supplier="sali ellectric")
                old_object.price = int(get_price)
                old_object.save()

            results.append('המוצר נסרק בסאלי אלקטריק והותצאות עודכנו במערכת')
            return


        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            ProductBySupplier.objects.create(supplier="sali electric", price=int(get_price), makat=makat, product=get_name)
            is_product=True
            results.append('המוצר נסרק בסאלי אלקטריק והותצאות נוספו למערכת')
            return
    else:
        results.append('המוצר לא קיים בסאלי אלקטריק')
        return







def find_in_lastprice(makat):

    #
    # chromedriver = r"C:\Users\User\Desktop\django.1\chromedriver.exe"
    #
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1200x600')
    # driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    #
    # driver.get('https://www.lastprice.co.il/')
    #
    # text_area = driver.find_element_by_id("searchBox")
    # text_area.click()
    # # text_area = driver.find_element_by_class_name("select2-search__field")
    # text_area.send_keys(makat)
    # submit = driver.find_element_by_class_name("btn-search").click()
    session = HTMLSession()
    page = session.get('https://www.lastprice.co.il/category.asp?q=' + makat)
    try:

        name = page.html.find('.degem' ,first=True)
        price = page.html.find('.price')
        if(price.__len__()==1):
            price=price[0].text
            name=name.text
            price = price.replace("קנה עכשיו ב-", "")
            price = price.replace("₪", "")
            price = price.replace("*", "")
            price = price.replace(",", "")
            price = price.replace("רק", "")
            price = price.replace("Plus", "")

            price = price.split('או הגש הצעה מ-', 1)[0]
            try:
                old_object = ProductBySupplier.objects.get(makat=makat, supplier="last price")
                if (old_object.price < int(price)):
                    price_in_past.object.create(makat=makat, date=old_object.date, price=old_object.price,supplier="last price")
                    old_object.price = int(price)
                    old_object.save()
                results.append('המוצר נסרק בלאסט פרייס והותצאות עודכנו במערכת')
                return



            except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
                ProductBySupplier.objects.create(supplier="last price", price=int(price), makat=makat, product=name)
                is_product = True
                results.append('המוצר נסרק בלאסט פרייס והותצאות נוספו למערכת')


        else:
            results.append('תוצאות רבות בלאסט פרייס')



        #return json.dumps(results)
        return results
    except NoSuchElementException as exception:

         results.append('המוצר לא קיים בלאסט פרייס')



    return results








def find_all(makat):
    results.clear()
    find_in_zap(makat)
    find_in_salielectric(makat)
    messege=find_in_lastprice(makat)
    if(is_product):
        Products.objects.create(product=name_in_zap,makat=makat,ourPrice=0)
    return messege


