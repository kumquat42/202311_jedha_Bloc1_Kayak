## Query variables
adults = 2
children = 0
no_rooms = 1
lat = 48.635954
lon = -1.511460
city = 'Paris'

date_min = '2023-12-25'
date_max = '2023-12-31'



# Appelle le scrapping de booking pour récupérer les premières addresses...

x = False
from testScrappingDef import scrapping_1, scrapping_hotel

scrapping_1(lat, lon, city, date_min, date_max, adults, children, no_rooms) # doesn't work

'''
x = True
if x == True:
   raise CloseSpider("Spider closed")



lien = 'https://www.booking.com/hotel/fr/ibis-paris-gare-montparnasse-catalogne'
scrapping_hotel(lien)
'''