
# coding: utf-8

# In[793]:

import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import re
import time
import os


# # Use Basketball Reference to Scrape Box Scores

# In[794]:

base_url = 'http://www.basketball-reference.com'
box_url = 'http://www.basketball-reference.com/boxscores/'
response = requests.get(box_url)
soup = BeautifulSoup(response.content, 'lxml')


# ## Write a function that gets the dates as strings between the date and today

# In[795]:

def get_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()
    day_lst = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst = [''.join((str(day)+str(0)).split('-')) for day in day_lst]
    return day_s_lst


# In[823]:

get_string_dates((2016, 3, 15))[:10]


# ## Improve upon the formatting

# In[820]:

def get_nice_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()
    day_lst = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst = [''.join(str(day)) for day in day_lst]
    return day_s_lst


# In[824]:

get_nice_string_dates((2016, 3, 15))[:10]


# ## Get our function to match Basketball References format

# #### We want the links in descending order so we can always append newest data to the bottom

# In[853]:

def get_url_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()    
    days_lst = [d1+td(days=i) for i in xrange((d2-d1).days)]
    urls = ['index.cgi?month='+str(day.month)+'&day='+str(day.day)+'&year='+str(day.year) for day in days_lst]
    urls = [box_url+url for url in urls][1:]
    day_lst2 = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst2 = [''.join(str(day)) for day in day_lst2][1:]
    #don't want todays hence [1:]
    return urls, day_s_lst2


# In[835]:

get_url_string_dates((2016, 3, 15))


# #### Code for getting the URLS for future scraping (If we want to scrape more years)

# In[836]:

def get_url_string_dates(d1, d2):
    d1 = date(*d1)
    d2 = date(*d2)    
    days_lst = [d1+td(days=i) for i in xrange((d2-d1).days)]
    urls = ['index.cgi?month='+str(day.month)+'&day='+str(day.day)+'&year='+str(day.year) for day in days_lst]
    urls = [box_url+url for url in urls][1:]
    day_lst2 = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst2 = [''.join(str(day)) for day in day_lst2][1:]
    #don't want todays hence [1:]
    return urls, day_s_lst2


# In[841]:

#get_url_string_dates((2015, 10, 26))
#get_url_string_dates((2013, 10, 26),(2014, 4, 17))
get_url_string_dates((2014, 10, 27),(2015, 4, 16))[:5]


# #### Find the later half of all the games today

# In[839]:

urls = soup.find_all(href=re.compile('/boxscores/2'))
urls


# #### Combining the base url to form the full url for the boxscores today

# In[840]:

game_urls = [base_url + url['href'] for url in urls]
game_urls


# #### Make a list of all the responses

# In[501]:

responses = [requests.get(game_url) for game_url in game_urls]


# ## Maybe this class will come in handy later

# In[494]:

class foo():
    def __init__(self, i):
        response = requests.get(game_urls[i])
        soup = BeautifulSoup(response.content, 'lxml')
        self.stats = soup.select('table[id$="_basic"] tbody tr')
        self.advanced = soup.select('table[id$="_advanced"] tbody tr')


# #### Write a function that outputs the name of the player so we can use it as the filename

# In[845]:

def get_name(stats, i):
    name = '_'.join(str(stats[i].get_text().split('\n')[1:-1][0]).split(' '))
    # replace spaces with _ 
    return name


# In[846]:

get_name(stats, 27)


# #### Create a function that returns a list with all the values in stats, advanced stats, which two teams are playing, and the date

# In[842]:

def get_line(stats, advanced, i, cut, away_team, home_team, dateapp):
    line = stats[i].get_text().split('\n')[1:-1]
    line2 = advanced[i].get_text().split('\n')[3:-1]
    #away_team = soup.select('table.stats_table tbody td a[href]')[0].contents[0].encode('ascii')
    #home_team = soup.select('table.stats_table tbody td a[href]')[1].contents[0].encode('ascii')
    #print away_team, home_team
    line = line + line2
    #am_i_home = stats[i].get_text().split('\n')[1]
    if line[1] == 'Did Not Play' or line[1] == 'Player Suspended':
        line.append(','*32)
        # If a player DNP or PS, add delimiters for all the missing stats
    line.append(away_team)
    line.append(home_team)
    if i < cut:
        line.append('0')
    else:
        line.append('1')
    line.append(dateapp)
    return line


# #### Create a function that writes a players stats to a file

# In[564]:

def write_to_csv(player_game_stat, out_file):    
    with open(out_file, 'a+') as f:
        f.write(','.join(player_game_stat) + '\n')


# In[583]:

def not_box_score(href):
    return href and not re.compile('/boxscores/2').search(href)


# #### We need a way to identify which team someone is on. We look at where the second instance of Reserves start and subtract 5 to get index of start of second team

# In[681]:

def cutoff(stats):
    count = 0
    for index, stat in enumerate(stats):
        if stat.get_text().split('\n')[1] == 'Reserves':
            count += 1
            if count > 1.5:
                return index-5


# In[854]:

base_url = 'http://www.basketball-reference.com'
box_url = 'http://www.basketball-reference.com/boxscores/'
#day_urls = get_url_string_dates((2013, 10, 28),(2014, 4, 17))
#day_urls = get_url_string_dates((2014, 10, 27),(2015, 4, 16))
day_urls = get_url_string_dates((2015, 10, 26))
#,(2016, 3, 15))


# #### Write a single game from a player into a CSV

# In[855]:

filename = 'data1516/' + get_name(stats) + '.csv'
create_csv(get_line(stats), filename)


# ### We need a function that combines our previous functions and starts scraping

# In[856]:

def scrappy(day_urls):
    for url, dateapp in zip(day_urls[0], day_urls[1]):
        response = requests.get(url)
        time.sleep(0.6)
        soup = BeautifulSoup(response.content, 'lxml')
        urls = soup.find_all(href=re.compile('/boxscores/2'), string='Final')
        # Make sure we only grab Final and not Box Score as well for duplicate entries
        game_urls = [base_url + url['href'] for url in urls]
        game_stats = [requests.get(game_url) for game_url in game_urls]
        time.sleep(0.6)
        for game_stat in game_stats:
            soup = BeautifulSoup(game_stat.content, 'lxml')
            away_team = soup.select('table.stats_table tbody td a[href]')[0].contents[0].encode('ascii')
            home_team = soup.select('table.stats_table tbody td a[href]')[1].contents[0].encode('ascii')
            #print away_team, home_team
            stats = soup.select('table[id$="_basic"] tbody tr')
            advanced = soup.select('table[id$="_advanced"] tbody tr')
            cut = cutoff(stats)
            for index, stuff in enumerate(stats):
                filename = 'data1516/' + get_name(stats, index) + '.csv'
                write_to_csv(get_line(stats, advanced, index, cut, away_team, home_team, dateapp), filename)


# In[857]:

scrappy(day_urls)


# In[ ]:

# def initiate_filenames(stats, folder_name):
#     for index, stuff in enumerate(stats):
#         filename = folder_name + get_name(stats, index) + '.csv'
#         write_to_csv(get_line(stats, advanced, index, cut, away_team, home_team, dateapp), filename)


# In[ ]:

# def create(game_stats):
#     soup = BeautifulSoup(game_stat.content, 'lxml')
#     away_team = soup.select('table.stats_table tbody td a[href]')[0].contents[0].encode('ascii')
#     home_team = soup.select('table.stats_table tbody td a[href]')[1].contents[0].encode('ascii')
#     #print away_team, home_team
#     stats = soup.select('table[id$="_basic"] tbody tr')
#     advanced = soup.select('table[id$="_advanced"] tbody tr')
#     cut = cutoff(stats)
#     for index, stuff in enumerate(stats):
#         filename = folder_name + get_name(stats, index) + '.csv'
#         write_to_csv(get_line(stats, advanced, index, cut, away_team, home_team, dateapp), filename)


# In[ ]:

def scrappy(day_urls, folder_name, sleep_time = 0):
    for url, dateapp in zip(day_urls[0], day_urls[1]):
        response = requests.get(url)
        time.sleep(sleep_time)
        soup = BeautifulSoup(response.content, 'lxml')
        urls = soup.find_all(href=re.compile('/boxscores/2'), string='Final')
        # Make sure we only grab Final and not Box Score as well for duplicate entries
        game_urls = [base_url + url['href'] for url in urls]
        game_stats = [requests.get(game_url) for game_url in game_urls]
        time.sleep(sleep_time)
        for game_stat in game_stats:
            soup = BeautifulSoup(game_stat.content, 'lxml')
            away_team = soup.select('table.stats_table tbody td a[href]')[0].contents[0].encode('ascii')
            home_team = soup.select('table.stats_table tbody td a[href]')[1].contents[0].encode('ascii')
            #print away_team, home_team
            stats = soup.select('table[id$="_basic"] tbody tr')
            advanced = soup.select('table[id$="_advanced"] tbody tr')
            cut = cutoff(stats)
            for index, stuff in enumerate(stats):
                filename = folder_name + get_name(stats, index) + '.csv'
                write_to_csv(get_line(stats, advanced, index, cut, away_team, home_team, dateapp), filename)


# In[ ]:

scrappy(day_urls, folder_name = 'data1415/', sleep_time = 0.6)


# In[744]:

#response = requests.get(day_urls[2])
#time.sleep(0.3)
#soup = BeautifulSoup(response.content, 'lxml')
#urls = soup.find_all(href=re.compile('/boxscores/2'))
#game_urls = [base_url + url['href'] for url in urls]
#responses = [requests.get(game_url) for game_url in game_urls]
#soup = BeautifulSoup(responses[0].content, 'lxml')
#stats = soup.select('table[id$="_basic"] tbody tr')


# In[745]:

#away_team = soup.select('table.stats_table tbody td a[href]')[0].contents[0].encode('ascii')
#home_team = soup.select('table.stats_table tbody td a[href]')[1].contents[0].encode('ascii')
#am_i_home = 
#print type(away_team), home_team


# In[ ]:



