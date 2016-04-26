import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import re
import time
import os


def get_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()
    day_lst = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst = [''.join((str(day)+str(0)).split('-')) for day in day_lst]
    return day_s_lst

def get_nice_string_dates(d1):
    d1 = date(*d1)
    d2 = date.today()
    day_lst = [str(d1 + td(days=day)) for day in xrange((d2-d1).days)]
    day_s_lst = [''.join(str(day)) for day in day_lst]
    return day_s_lst

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



def get_name(stats, i):
    name = '_'.join(str(stats[i].get_text().split('\n')[1:-1][0]).split(' '))
    # replace spaces with _ 
    return name





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



def write_to_csv(player_game_stat, out_file):    
    with open(out_file, 'a+') as f:
        f.write(','.join(player_game_stat) + '\n')




def cutoff(stats):
    count = 0
    for index, stat in enumerate(stats):
        if stat.get_text().split('\n')[1] == 'Reserves':
            count += 1
            if count > 1.5:
                return index-5



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



if __name__ == '__main__':
    base_url = 'http://www.basketball-reference.com'
    box_url = 'http://www.basketball-reference.com/boxscores/'
    day_urls = get_url_string_dates((2015, 10, 26))
    filename = 'data1516/' + get_name(stats) + '.csv'
    scrappy(day_urls)



