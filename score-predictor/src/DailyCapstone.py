import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import re

base_url = 'http://www.basketball-reference.com'
box_url = 'http://www.basketball-reference.com/boxscores/'
response = requests.get(box_url)
soup = BeautifulSoup(response.content, 'lxml')

def get_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()
    day_lst = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst = [''.join((str(day)+str(0)).split('-')) for day in day_lst]
    return day_s_lst

#get_string_dates((2014, 3, 22))

urls = soup.find_all(href=re.compile('/boxscores/2'))
game_urls = [base_url + url['href'] for url in urls]

for url in game_url:
    Beautifulsoup(url.content)

responses = [requests.get(game_url) for game_url in game_urls]

# class foofoo():

#     def __init__(self):
#         response = requests.get(game_urls[0])
#         soup = BeautifulSoup(response.content, 'lxml')
#         self.stats = soup.select('table[id$="_basic"] tbody tr')
#         self.advanced = soup.select('table[id$="_advanced"] tbody tr')

#     def get_name(stats, i):
#     	name = '_'.join(str(stats[i].get_text().split('\n')[1:-1][0]).split(' '))
#     	return name

#     def get_line(stats, advanced, i):
# 		line = stats[i].get_text().split('\n')[1:-1]
# 		line2 = advanced[i].get_text().split('\n')[3:-1]
# 		line = line + line2
# 		return line

# 	def create_csv(player_game_stat, out_file):
# 	    file = open(out_file, 'w+')
# 	    file.write(','.join(player_game_stat))
# 	    return None




for index, stuff in enumerate(stats):
    filename = 'data/' + get_name(stats, index) + '.csv'
    #print filename
    create_csv(get_line(stats, advanced, index), filename)


filename = 'data/' + get_name(stats) + '.csv'
create_csv(get_line(stats), filename)