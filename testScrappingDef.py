import scrapy
from scrapy.crawler import CrawlerProcess
import os


def scrapping_1(lat, lon, city, date_min, date_max, adults, children, no_rooms):
		
	url_scrapping = f'https://www.booking.com/searchresults.fr.html?ss={lat}+{lon}&label=fr-fr-booking-desktop-DCpBIW3k2*WIo8XuzMdB9AS652796013276%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9056579%3Ali%3Adec%3Adm&aid=2311236&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&checkin={date_min}&checkout={date_max}&group_adults={adults}&no_rooms={no_rooms}&group_children={children}&sb_travel_purpose=leisure&order=review_score_and_price'
	mes_index = [3, 5, 7]
	#url_scrapping2 = f'https://www.booking.com/searchresults.fr.html?ss={lat}+{lon}&label=fr-fr-booking-desktop-DCpBIW3k2*WIo8XuzMdB9AS652796013276%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9056579%3Ali%3Adec%3Adm&aid=2311236&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&checkin={date_min}&checkout={date_max}&group_adults={adults}&no_rooms={no_rooms}&group_children={children}&sb_travel_purpose=leisure'
	## mes_index = [3, 7, 9]
	### not ok with 2 urls....


	class booking_scraper(scrapy.Spider):
		# Name of your spider
		name = "Spider_woman"



		# Url to start the spider from
		start_urls = [url_scrapping]
		#### peut être trouver un moyen de mettre les liens ici dans les urls de départ ?


		# Callback function that will be called when starting your spider
		def parse(self, response):  # Qui va mettre en forme. Ne marche pas avec un autre nom mais on peut mettre des if...
			
			for item in mes_index:
				print(item)
				try:
					note_temp = response.xpath(f'/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[{item}]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]').get()
					note = note_temp.split('note de ')[1].split('\"')[0]
				except:
					note = 'NaN'
				

				lien_temp = response.xpath(f'/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[{item}]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a').get()
				lien = lien_temp.split('.fr.html')[0].split('\"')[1]


				yield {'Ville': city, 'Note': note, 'Lien': lien}

	# Name of the file where the results will be saved
	filename = "20231220_scrapping_test.json"

	# If file already exists, delete it before crawling (because Scrapy will 
	# concatenate the last and new results otherwise)
	if filename in os.listdir('/home/melb/Documents/Projects/202311_jedha_Bloc1_Kayak/'):
			os.remove('/home/melb/Documents/Projects/202311_jedha_Bloc1_Kayak/' + filename)

	# Declare a new CrawlerProcess with some settings
	## USER_AGENT => Simulates a browser on an OS
	## LOG_LEVEL => Minimal Level of Log 
	## FEEDS => Where the file will be stored 
	## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
	process = CrawlerProcess(settings = {
		'USER_AGENT': 'Chrome/97.0',
		#'LOG_LEVEL': logging.INFO,
		"FEEDS": {
			'/home/melb/Documents/Projects/202311_jedha_Bloc1_Kayak/' + filename : {"format": "json"},
		}
	})

	# Start the crawling using the spider you defined above


	process.crawl(booking_scraper)
	process.start()



def scrapping_hotel(lien):

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