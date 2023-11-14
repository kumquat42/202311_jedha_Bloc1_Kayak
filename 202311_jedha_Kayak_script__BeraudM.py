import scrapy
from scrapy.crawler import CrawlerProcess
import os
import logging

# try with quotes to scrape.com

class Booking(scrapy.Spider):
   
    name = "booking"

    # Url to start your spider from 
    start_urls = [
        'https://www.booking.com/searchresults.html?ss=Paris%2C+Ile+de+France%2C+France&label=gen173nr-1FCAEoggI46AdIM1gEaE2IAQGYATG4ARnIAQ_YAQHoAQH4AQKIAgGoAgO4AoHbzKoGwAIB0gIkNDg0MGEyMzQtYzdkZC00MGRjLWJjN2YtN2FiNzBkMzZhYjQ02AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=12193a808ea90264&ac_meta=GhAxMjE5M2E4MDhlYTkwMjY0IAAoATICZW46BXBhcmlzQABKAFAA&checkin=2023-12-01&checkout=2023-12-03&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure', # on peut mettre pleins d'url en pus, c'est une classe, donc il suffit de faire pleins d'instances.
    ]

    # Callback function that will be called when starting your spider
    def parse(self, response):  # Qui va mettre en forme. yield pour en faire plusieurs.... On peut faire un return, mais ça va stopper la boucle. Donc le return peut nous permettre d'aller dans des sous-pages pour chopper d'autres infos...
        n = 5
        for i in range(2, n+1):
            yield {
                'product': response.xpath(f'/html/body/main/div[2]/div/div[2]/div/ul/li[{i}]/div/div/div[2]/div[1]/h3/a/text()').get(),  # on prend notre texte
                #'ref_image': response.xpath('/html/body/main/div[2]/div/div[2]/div/ul/li[{i}]/div/div/div[2]/div[1]/h3/a').get()   #on fait un dico. Donc clé et on faire un XPATH.get
            }
# Plutôt que .get(), on peut prendre .getall() car des fois, on a plusieurs choses qui appartiennent à une même classe. Et attention où on fait le .getall()

# Name of the file where the results will be saved
filename = "Several_spider.json" # on peut importer datetime et ajouter today pour ajouter la date du jour sur les fichiers automatiquement... Ca range (si yyyy-mm-dd ou Unix)
# l'avantage des json => c'est typé. Donc on peut cleaner, récupérer en dataframe...
# les json se lisent automatiquement avec pandas ! et font nos colonnes


# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('/home/mel/Documents/Data_management/Web scraping/'): 
        os.remove('/home/mel/Documents/Data_management/Web scraping/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO, # permet de voir les bugs... ou ce qu'il se passe. Seulement du visuel. Il faut demander de le sauvegarder si on veut le sauvegarder
    "FEEDS": {
        '/home/mel/Documents/Data_management/Web scraping/' + filename : {"format": "json"},
    "AUTOTHROTTLE_ENABLED": True # permet de se limiter dans le temps, mets de l'aléatoire. Pour évter de se faire choper
    #Il y a aussi une fonction qui permet de changer d'agent pour éviter que ce soit toujours la même personne.
    # Pareil avec les adresses IP, mais ça coute pas mal d'avoir plusieurs adresses IP.
    }
})

# Start the crawling using the spider you defined above
process.crawl(BoubouSpider)
process.start()

'''

>df = pd.read_json('/home/mel/Documents/Data_management/Web scraping/Boubou_scrap_5_article_text.json')
>df
                                             product
0  \n              Boubou Africain wax Femme | Vê...
1  \n              Robe africaine en wax grande t...
2  \n              Boubou Africain Femme | Vêteme...
3  \n              Robe africaine en wax mi longu...>

'''