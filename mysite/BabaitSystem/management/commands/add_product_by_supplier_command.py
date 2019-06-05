from django.core.management.base import BaseCommand, CommandError
#from mysite.BabaitSystem.models import Products
#from BabaitSystem.views import findInZap
import urllib
from ...models import ProductBySupplier
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Command to do........'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        session = requests.Session()
        # Zap example url
        # zap_example_url = "https://www.zap.co.il/model.aspx?modelid=1003535"
        # zap_example_url = "https://www.zap.co.il/model.aspx?modelid=946412"
        zap_example_url = "https://www.zap.co.il/model.aspx?modelid=826449"
        # zap_example_url = "https://www.zap.co.il/model.aspx?modelid=842676&ref=www.zap.co.il"

        try:
            # try get zap data
            req = session.get(zap_example_url)
        except urllib.error.HTTPError as e:
            # except for error
            print("Error while requesting url: {0}".format(e))

        # create new BeatifulSoup object
        try:
            bsObj = BeautifulSoup(req.text, "html.parser")
            print("Request Zap html data from url...")
        except AttributeError as e:
            print("Error while requesting url: {0}".format(e))

        get_stores = bsObj.find('div', {'class': 'StoresLines'})
        # get zap products by div tag
        prodBySupp = []
        countNoSupplier = 0
        chippestProductsNum = 7
        get_product_name = bsObj.find('div', {'class': 'ProductBox'})
        prod_name = get_product_name.contents[3].contents[1].contents[1]
        prod_name = prod_name.text.strip()
        for x in range(0, chippestProductsNum):
            price = get_stores.contents[1].contents[x + x + 1].contents[1].contents[7].contents[3]
            price = price.text.replace('₪', '').strip()
            price = price.replace(',', '')
            # conSupplier = get_stores.contents[1].contents[x+x+1].contents[1].contents[9].contents[3].contents[1]
            supplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[3]
            if supplier.text.strip() == 'קנייה חכמה':
                supplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[5]
            # conSupplier=conSupplier.replace('ב-','').strip()
            # if supplier.text.strip() not in suppliers:
            #     countNoSupplier += 1
            ProductBySupplier.objects.create(product=prod_name,supplier=supplier.text,price=int(price))



