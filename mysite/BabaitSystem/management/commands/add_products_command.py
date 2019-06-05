from django.core.management.base import BaseCommand, CommandError
#from mysite.BabaitSystem.models import Products
#from BabaitSystem.views import findInZap
import urllib
from ...models import Products
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
            #zap_example_url = "https://www.zap.co.il/model.aspx?modelid=842676&ref=www.zap.co.il"

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
            chippestProductsNum = 7

            for x in range(0, chippestProductsNum):
                print(x)
                conPricer = get_stores.contents[1].contents[x + x + 1].contents[1].contents[7].contents[3]

                conPricer = conPricer.text.replace('₪', '').strip()

                conPricer = int(conPricer.replace(',', ''))

                # conSupplier = get_stores.contents[1].contents[x+x+1].contents[1].contents[9].contents[3].contents[1]
                conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[3]

                if conSupplier.text.strip() == 'קנייה חכמה':
                    conSupplier = get_stores.contents[1].contents[x + x + 1].contents[1].contents[9].contents[5]
                print("I am here9")
                print("supplier:", type(conSupplier), conSupplier)
                print("pricer:", type(conPricer), conPricer)
                Products.objects.create(product=conSupplier.text,makat="blablabla",ourPrice=int(conPricer))
                print("I am here")

               # pr = Products(product=conSupplier, makat="blablabla", ourPrice=conPricer)

                # pr.save()


            print("I am here")
