import scrapy
from scrapy.crawler import CrawlerProcess
import os


lien = 'https://www.booking.com/hotel/fr/ibis-paris-gare-montparnasse-catalogne'
# 'https://www.booking.com/hotel/fr/atala' ok

### Go further on the hotel
class hotel_scraper(scrapy.Spider):
	# Name of your spider
	name = "Spider_woman2"
	# Url to start the spider from 
	start_urls = [lien] #lien hotel

	# Callback function that will be called when starting your spider
	def parse(self, response):  # Qui va mettre en forme.
		
		nom_temp = response.xpath('/html/body/div[3]/div/div[5]/div[1]/div[1]/div[1]/div/div[2]/div[9]/div[1]/div/div/h2').get()
		coord_temp = response.xpath('/html/body/div[3]/div/div[5]/div[1]/div[1]/div[1]/div/div[2]/div[9]/p/a').get()		
		desc_temp = response.xpath('/html/body/div[3]/div/div[5]/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/p').get()
		
		nom = nom_temp.split('>')[1].split('</h2')[0]
		desc = desc_temp.split('>')[1].split('\n')[0]
		coord = coord_temp.split('data-atlas-latlng=\"')[1].split('\"')[0]
	

		print(f'Ici2: \nNom: {nom},\nDescription: {desc}, \nLat/Long: {coord}')

process_hotel = CrawlerProcess(settings = {
	'USER_AGENT': 'Chrome/97.0',
	#'LOG_LEVEL': logging.INFO,
	#"FEEDS": {
	#	'/home/melb/Documents/Projects/202311_jedha_Bloc1_Kayak/' + filename : {"format": "json"},
	#}
})

# Start the crawling using the spider you defined above
process_hotel.crawl(hotel_scraper)
process_hotel.start()

## J'ai tenté en Gigogne, sans succès... En fait il n'arrive pas à le lancer un scrappeur 2 fois si je comprends bien l'erreur. Il faut donc faire 2 scripts séparés...