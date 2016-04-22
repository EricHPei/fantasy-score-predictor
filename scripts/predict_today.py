from __future__ import division
from scipy import stats
import matplotlib.pyplot as plt
import random_forest
import datetime
import pandas as pd
import cPickle as pickle
import numpy as np
from bs4 import BeautifulSoup
import requests
import re


def get_url_today_teams():
	'''Todays Games are encoded differently on Basketball Reference. Use this function
	to return the urls of the teams that are playing today'''
	url = 'http://www.basketball-reference.com/leagues/NBA_2016_games.html'
	base_url = 'http://www.basketball-reference.com'
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'lxml')
	today = datetime.date.today()
	str_date = ''.join((str(today)+str(0)).split('-'))
	urls = soup.find_all(csk=re.compile(str_date))
	away_team = urls[1::3]
	home_team = urls[2::3]
	away_addon_urls = [url.contents for url in away_team]
	away_urls = [base_url + addon[0]['href'] for addon in away_addon_urls]
	home_addon_urls = [url.contents for url in home_team]
	home_urls = [base_url + addon[0]['href'] for addon in home_addon_urls]
	return away_urls, home_urls

def get_list_of_players_today(away_urls, home_urls):
	'''Get list of team urls and return list of players'''
	away_list = []
	home_list = []
	compilation = zip(away_urls, home_urls)
	rr = re.compile(r'([A-Z]{3})')
	r = re.compile(r'\bUNIVERSITY\b | \bCOLLEGE\b | \bCC\b | \bINSTITUTE\b', flags=re.I | re.X)
	for away_url, home_url in compilation:
		home_team = re.search(rr, home_url).group(0)
		response_away = requests.get(away_url)
		response_home = requests.get(home_url)
		soup_away = BeautifulSoup(response_away.content, 'lxml')
		soup_home = BeautifulSoup(response_home.content, 'lxml')
		away = soup_away.select('table[id$="roster"] tbody tr a[href]')
		home = soup_home.select('table[id$="roster"] tbody tr a[href]')
		for a in away:
			if r.findall(a.contents[0]) == []:
				away_list.append((a.contents[0].encode('ascii'), home_team))
		for h in home:
			if r.findall(h.contents[0]) == []:
				home_list.append((h.contents[0].encode('ascii'), home_team))
	return away_list, home_list

def create_line(df, away_list, home_list):
	'''Feed list of tuples with Player Name and place playing, output line to feed to predict'''
	col = df.columns
	elev = read_to_dict()
	today = datetime.date.today()
	today = np.datetime64(today)
	player_dict = {}
	for each_tuple in away_list:
		name = each_tuple[0]
		if sum(df['Player Name']==name) != 0:
			player_df = df[df['Player Name'] == name]
			player_df = player_df.iloc[::-1][:1]
			player_dict[name] = {}
			for cat in ['FG','TP','FT','TRB','AST','STL','BLK','TOV','PF','DRtg','TSP','PM','USGP','FTr','ORtg','DRtg']: 
				for i in xrange(1, 5):
					if i==1:
						if cat == 'TP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['3P'].values[0]
						elif cat == 'TSP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['TS%'].values[0]
						elif cat == 'PM':
							player_dict[name][cat+str(i)+'dayago'] = player_df['+/-'].values[0]
						elif cat == 'USGP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['USG%'].values[0]							
						else:
							player_dict[name][cat+str(i)+'dayago'] = player_df[cat].values[0]
					else:
						player_dict[name][cat+str(i)+'dayago'] = player_df[cat+str(i-1)+'dayago'].values[0]
			player_dict[name]['Elevation'] = elev[each_tuple[1]]
			player_dict[name]['OneisHome'] = 0
			time_difference = today - player_df['Date'].values[0].astype('M8[D]')
			if time_difference == datetime.timedelta(1):
				player_dict[name]['SP_1dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_2dayago'] = player_df['SP_1dayago'].values[0]
				player_dict[name]['SP_3dayago'] = player_df['SP_2dayago'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_3dayago'].values[0]
			elif time_difference == datetime.timedelta(2):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_3dayago'] = player_df['SP_1dayago'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_2dayago'].values[0]
			elif time_difference == datetime.timedelta(3):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_1dayago'].values[0]
			elif time_difference == datetime.timedelta(4):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = 0
				player_dict[name]['SP_4dayago'] = player_df['SP'].values[0]
			else:
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = 0
				player_dict[name]['SP_4dayago'] = 0
	for each_tuple in home_list:
		name = each_tuple[0]
		if sum(df['Player Name']==name) != 0:
			player_df = df[df['Player Name'] == name]
			player_df = player_df.iloc[::-1][:1]
			player_dict[name] = {}
			for cat in ['FG','TP','FT','TRB','AST','STL','BLK','TOV','PF','DRtg','TSP','PM','USGP','FTr','ORtg','DRtg']: 
				for i in xrange(1, 5):
					if i==1:
						if cat == 'TP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['3P'].values[0]
						elif cat == 'TSP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['TS%'].values[0]
						elif cat == 'PM':
							player_dict[name][cat+str(i)+'dayago'] = player_df['+/-'].values[0]
						elif cat == 'USGP':
							player_dict[name][cat+str(i)+'dayago'] = player_df['USG%'].values[0]							
						else:
							player_dict[name][cat+str(i)+'dayago'] = player_df[cat].values[0]
					else:
						player_dict[name][cat+str(i)+'dayago'] = player_df[cat+str(i-1)+'dayago'].values[0]
			player_dict[name]['Elevation'] = elev[each_tuple[1]]
			player_dict[name]['OneisHome'] = 1
			time_difference = today - player_df['Date'].values[0].astype('M8[D]')
			if time_difference == datetime.timedelta(1):
				player_dict[name]['SP_1dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_2dayago'] = player_df['SP_1dayago'].values[0]
				player_dict[name]['SP_3dayago'] = player_df['SP_2dayago'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_3dayago'].values[0]
			elif time_difference == datetime.timedelta(2):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_3dayago'] = player_df['SP_1dayago'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_2dayago'].values[0]
			elif time_difference == datetime.timedelta(3):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = player_df['SP'].values[0]
				player_dict[name]['SP_4dayago'] = player_df['SP_1dayago'].values[0]
			elif time_difference == datetime.timedelta(4):
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = 0
				player_dict[name]['SP_4dayago'] = player_df['SP'].values[0]
			else:
				player_dict[name]['SP_1dayago'] = 0
				player_dict[name]['SP_2dayago'] = 0
				player_dict[name]['SP_3dayago'] = 0
				player_dict[name]['SP_4dayago'] = 0
	return player_dict

def predict_now(lines):
	'''Feed a df of lines to predict'''
	filename = 'score-predictor/pickles/cluster_pickles_with_dictionary.r'
	with open(filename,'rb') as fp:
		cl_di=pickle.load(fp)
		model0_d=pickle.load(fp)
		model1_d=pickle.load(fp)
		model2_d=pickle.load(fp)
	#my_cols = list(lines.drop(['Date', 'Player Name'], axis=1).columns)
	col_id = []
	feature_names = ['SP_1dayago', 'SP_2dayago', 'SP_3dayago', 'SP_4dayago', 'TP1dayago', 'TP2dayago', 'TP3dayago', 'TP4dayago', 
		'FG1dayago', 'FG2dayago', 'FG3dayago', 'FG4dayago', 'FT1dayago', 'FT2dayago', 'FT3dayago', 'FT4dayago', 'TRB1dayago', 'TRB2dayago', 'TRB3dayago', 
		'TRB4dayago', 'AST1dayago', 'AST2dayago', 'AST3dayago', 'AST4dayago', 'BLK1dayago', 'BLK2dayago', 'BLK3dayago', 'BLK4dayago', 'STL1dayago', 
		'STL2dayago', 'STL3dayago', 'STL4dayago', 'TOV1dayago', 'TOV2dayago', 'TOV3dayago', 'TOV4dayago', 'USGP1dayago', 'USGP2dayago', 'USGP3dayago', 
		'USGP4dayago', 'FTr1dayago', 'FTr2dayago', 'FTr3dayago', 'FTr4dayago', 'PM1dayago', 'PM2dayago', 'PM3dayago', 'PM4dayago', 'TSP1dayago', 'TSP2dayago', 
		'TSP3dayago', 'TSP4dayago', 'PF1dayago', 'PF2dayago', 'PF3dayago', 'PF4dayago', 'ORtg1dayago', 'ORtg2dayago', 'ORtg3dayago', 'ORtg4dayago', 'DRtg1dayago', 
		'DRtg2dayago', 'DRtg3dayago', 'DRtg4dayago', 'Elevation', 'OneisHome']
	for feat in feature_names:
		col_id.append(np.where(lines.columns==feat)[0][0])
	for i, line in enumerate(lines.values):
		player = line[np.where(lines.columns=='Player Name')[0][0]]
		features = line[col_id].reshape(1, -1)
		#features = lines.iloc[i][['SP_1dayago', 'SP_2dayago', 'SP_3dayago', 'SP_4dayago', 'TP1dayago', 'TP2dayago', 'TP3dayago', 'TP4dayago', 'FG1dayago', 'FG2dayago', 'FG3dayago', 'FG4dayago', 'FT1dayago', 'FT2dayago', 'FT3dayago', 'FT4dayago', 'TRB1dayago', 'TRB2dayago', 'TRB3dayago', 'TRB4dayago', 'AST1dayago', 'AST2dayago', 'AST3dayago', 'AST4dayago', 'BLK1dayago', 'BLK2dayago', 'BLK3dayago', 'BLK4dayago', 'STL1dayago', 'STL2dayago', 'STL3dayago', 'STL4dayago', 'TOV1dayago', 'TOV2dayago', 'TOV3dayago', 'TOV4dayago', 'USGP1dayago', 'USGP2dayago', 'USGP3dayago', 'USGP4dayago', 'FTr1dayago', 'FTr2dayago', 'FTr3dayago', 'FTr4dayago', 'PM1dayago', 'PM2dayago', 'PM3dayago', 'PM4dayago', 'TSP1dayago', 'TSP2dayago', 'TSP3dayago', 'TSP4dayago', 'PF1dayago', 'PF2dayago', 'PF3dayago', 'PF4dayago', 'ORtg1dayago', 'ORtg2dayago', 'ORtg3dayago', 'ORtg4dayago', 'DRtg1dayago', 'DRtg2dayago', 'DRtg3dayago', 'DRtg4dayago', 'Elevation', 'OneisHome']]
		#double check if its first element
		print player
		if player in cl_di[0]:
			print 'cluster 0:'
			for category, model in model0_d.iteritems():
				print model.predict(features), str(category)
		elif player in cl_di[1]:
			print 'cluster 1:'
			for category, model in model1_d.iteritems():
				print model.predict(features), str(category)
		elif player in cl_di[2]:
			print 'cluster 2:'
			for category, model in model2_d.iteritems():
				print model.predict(features), str(category)
		else:
			print player + ' is a ninja' 

def predict_today(player_dict):
	'''Take a dictionary of values to predict and predict'''
	filename = 'score-predictor/pickles/cluster_pickles_with_dictionary.r'
	with open(filename,'rb') as fp:
		cl_di=pickle.load(fp)
		model0_d=pickle.load(fp)
		model1_d=pickle.load(fp)
		model2_d=pickle.load(fp)
	# col_id = []
	feature_names = ['SP_1dayago', 'SP_2dayago', 'SP_3dayago', 'SP_4dayago', 'TP1dayago', 'TP2dayago', 'TP3dayago', 'TP4dayago', 
		'FG1dayago', 'FG2dayago', 'FG3dayago', 'FG4dayago', 'FT1dayago', 'FT2dayago', 'FT3dayago', 'FT4dayago', 'TRB1dayago', 'TRB2dayago', 'TRB3dayago', 
		'TRB4dayago', 'AST1dayago', 'AST2dayago', 'AST3dayago', 'AST4dayago', 'BLK1dayago', 'BLK2dayago', 'BLK3dayago', 'BLK4dayago', 'STL1dayago', 
		'STL2dayago', 'STL3dayago', 'STL4dayago', 'TOV1dayago', 'TOV2dayago', 'TOV3dayago', 'TOV4dayago', 'USGP1dayago', 'USGP2dayago', 'USGP3dayago', 
		'USGP4dayago', 'FTr1dayago', 'FTr2dayago', 'FTr3dayago', 'FTr4dayago', 'PM1dayago', 'PM2dayago', 'PM3dayago', 'PM4dayago', 'TSP1dayago', 'TSP2dayago', 
		'TSP3dayago', 'TSP4dayago', 'PF1dayago', 'PF2dayago', 'PF3dayago', 'PF4dayago', 'ORtg1dayago', 'ORtg2dayago', 'ORtg3dayago', 'ORtg4dayago', 'DRtg1dayago', 
		'DRtg2dayago', 'DRtg3dayago', 'DRtg4dayago', 'Elevation', 'OneisHome']
	#for feat in feature_names:
	#	col_id.append(np.where(lines.columns==feat)[0][0])
	for player, feature_dict in player_dict.iteritems():
		#player = line[np.where(lines.columns=='Player Name')[0][0]]
		#features = line[col_id].reshape(1, -1)
		features = np.zeros((1, len(feature_names)))
		for i, feat in enumerate(feature_names):
			features[0, i] = feature_dict[feat]
		if player in cl_di[0]:
			print 'cluster 0:'
			for category, model in model0_d.iteritems():
				print player, model.predict(features), str(category)
		elif player in cl_di[1]:
			print 'cluster 1:'
			for category, model in model1_d.iteritems():
				print player, model.predict(features), str(category)
		elif player in cl_di[2]:
			print 'cluster 2:'
			for category, model in model2_d.iteritems():
				print player, model.predict(features), str(category)
		else:
			print player + ' is a ninja' 

def read_to_dict():
	'''add .. before score'''
	Elevation = pd.read_csv('score-predictor/data/Elevation.csv', delimiter=' ', header=None)
	elev = {k:int(v) for (k, v) in zip(Elevation[0], Elevation[3])}
	return elev


