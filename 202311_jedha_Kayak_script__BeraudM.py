import scrapy
from scrapy.crawler import CrawlerProcess
import os

# try with quotes to scrape.com

## Query variables

lat = 48.635954
lon = -1.511460

date_min = '2023-12-20'
date_max = '2023-12-24'

adults = 2
children = 0
no_rooms = 1

item = 1 # ne fonctionne qu'avec le '3'


url_scrapping = f'https://www.booking.com/searchresults.fr.html?ss={lat}+{lon}&label=fr-fr-booking-desktop-DCpBIW3k2*WIo8XuzMdB9AS652796013276%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9056579%3Ali%3Adec%3Adm&aid=2311236&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&checkin={date_min}&checkout={date_max}&group_adults={adults}&no_rooms={no_rooms}&group_children={children}&sb_travel_purpose=leisure&order=review_score_and_price'

class booking_scraper(scrapy.Spider):
	# Name of your spider
	name = "Spider_woman"
	# Url to start the spider from 
	start_urls = [url_scrapping]

	# Callback function that will be called when starting your spider
	def parse(self, response):  # Qui va mettre en forme.
    

		desc_temp = response.xpath(f'/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[{item}]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]').get()
		desc = desc_temp.split('>')[1].split('<')[0]

		hotel_temp = response.xpath(f'/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[{item}]/div[1]/div[1]/div/a').get()


		return {'hotel': hotel_temp, 'description' : desc}




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
