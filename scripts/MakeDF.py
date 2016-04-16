import pandas as pd 
import numpy as np
import glob
import datetime

def create_csvs(folder):
	'''
	INPUT: folder where all the data is
	OUTPUT: None
	goes through each folder. initiates file if it doesn't exist. if it does, append 
	'''
	path = folder+'/*/'
	allFiles = glob.glob(path + "/*.csv")
	for file in allFiles:
		write_to_csv(file)
	return None

def write_to_csv(in_file):
	with open(in_file, 'r') as r:
		text = r.readlines()
		beginning = in_file.split('/')[0]
		end = in_file.split('/')[2]
		composite_file = beginning + '/alldata/' + end
	with open(composite_file, 'a+') as f:
		for i in text:
			f.write(i)
	return None

def create_df():
	'''
	INPUT: folder where all the combined files are
	OUTPUT: df
	Goes through each file and adds it to the data frame
	'''
	path = 'alldata/alldata'
	allFiles = glob.glob(path + "/*.csv")
	list_ = []
	for file_ in allFiles:
	    df = pd.read_csv(file_,index_col=None, header=None)
	    list_.append(df)
	df = pd.concat(list_)
	df.columns = ['Player Name','MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%',\
				'ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-','TS%','eFG%','3PAr',\
				'FTr','ORB%','DRB%','TRB%','AST%','STL%','BLK%','TOV%','USG%','ORtg','DRtg','Away',\
				'Home','OneisHome','Date']
	return df

def clean_df(df):
	'''
	INPUT: messy data frame
	OUTPUT: data frame filling NA, without reserves, and columns typecasted correctly
	'''
	df = df[df['Player Name']!= 'Reserves']
	df['MP'] = df['MP'].map(lambda x: '0:00' if ":" not in str(x) else str(x))
	#df['MP'] = df['MP'].apply(lambda x: '0:00' if x=="Did Not Play" or x=="Player Suspended" else x)
	df = df.fillna(0)
	df['FG']=(np.array(df['FG'])).astype(int)
	df['FGA']=(np.array(df['FGA'])).astype(int)
	df['3P']=(np.array(df['3P'])).astype(int)
	df['3PA']=(np.array(df['3PA'])).astype(int)
	df['FT']=(np.array(df['FT'])).astype(int)
	df['FTA']=(np.array(df['FTA'])).astype(int)
	df['ORB']=(np.array(df['ORB'])).astype(int)
	df['DRB']=(np.array(df['DRB'])).astype(int)
	df['TRB']=(np.array(df['TRB'])).astype(int)
	df['AST']=(np.array(df['AST'])).astype(int)
	df['STL']=(np.array(df['STL'])).astype(int)
	df['BLK']=(np.array(df['BLK'])).astype(int)
	df['TOV']=(np.array(df['TOV'])).astype(int)
	df['PF']=(np.array(df['PF'])).astype(int)
	df['PTS']=(np.array(df['PTS'])).astype(int)
	df['+/-']=(np.array(df['+/-'])).astype(int)
	df['Date']=pd.to_datetime(df['Date'])
	return df

def drop_zerominutes(df):
	return df[df['MP'] != '0:00']

def add_features(df):
	'''
	INPUT: raw df
	OUTPUT: featured df
	Goes through each file and adds it to the data frame
	'''
	#df['Suspended'] = df['MP'].apply(lambda x: 1 if x=="Player Suspended" else 0)
	#df['MP1'] = pd.to_datetime(df.MP, format = "%M:%S")
	ms_split = df['MP'].apply(lambda x: x.split(":"))
	seconds_played = [int(row[0])*60 + int(row[1]) for row in ms_split]
	df['SP'] = seconds_played
	df = df.reset_index()
	df = df.drop(['index', 'MP'], axis=1)
	return df

def make_averages(df, cutoff=0):
	'''
	original make_averages
	make_averages_until
	INPUT: messy data frame. use with X_Train. Input how many days you want to have the averages cutoff
	OUTPUT: data frame with player averages
	'''
	today = datetime.date.today()
	stop_average_date = today - datetime.timedelta(cutoff)
	df = df[df['Date'] < stop_average_date]
	Player_Averages = df.groupby(df['Player Name']).mean()[['SP', '3P', 'FG', 'FT', 'TRB', \
															'AST', 'BLK', 'STL', 'TOV', 'USG%', 'FTr', \
															'+/-', 'TS%', 'PF', 'ORtg', 'DRtg']]
	Player_Averages['Score'] = 2*Player_Averages['FG'] + Player_Averages['3P'] + Player_Averages['FT'] \
							+ 1.2*Player_Averages['TRB'] + 1.5*Player_Averages['AST'] + 2*\
                            Player_Averages['BLK'] + 2*Player_Averages['STL'] - Player_Averages['TOV']
	Player_Averages = Player_Averages.dropna(axis=1)
	return Player_Averages

def make_averages_per48(df):
	'''
	make_averages_until
	INPUT: messy data frame. use with X_Train. Input how many days you want to have the averages cutoff
	OUTPUT: data frame with player averages
	'''
	for column in df.columns[1:-1]:
		df[column] = 48*60*df[column]/df['SP']
	df=df.dropna(0)
	return df.iloc[:,1:-1]


def getdf_untildate(df, cutoff=0):
	'''
	INPUT: data frame
	OUTPUT: data frame up until date
	would be wise to match cutoff with make_averages cutoff to feed to clusters later
	'''
	today = datetime.date.today()
	stop_average_date = today - datetime.timedelta(cutoff)
	df = df[df['Date'] < stop_average_date]
	df = df[['Player Name','SP','3P','FG','FT','TRB','AST','BLK','STL','TOV']]
	return df

def get_date_matrix(df):
	'''
	INPUT: data frame
	OUTPUT: matrix with player name, dates with lag and seconds played

	This function and the next three are used to get the seconds played for previous days, indicating
	representing amount of rest.
	'''	
	df['DateM1'] = df['Date'] - pd.DateOffset(1)
	df['DateM2'] = df['Date'] - pd.DateOffset(2)
	df['DateM3'] = df['Date'] - pd.DateOffset(3)
	df['DateM4'] = df['Date'] - pd.DateOffset(4)
	#df['DateM5'] = df['Date'] - pd.DateOffset(5)
	date_matrix = df[['Player Name', 'Date', 'DateM1', 'DateM2', 'DateM3', 'DateM4', 'SP']].values
	return date_matrix

def previous_sp(index, date_matrix, days=1):
	player = date_matrix[index][0]
	date = date_matrix[index][1+days]
	for i in xrange(4):
		if (index-1-i) >= 0:
			if date_matrix[index-1-i][0] == player and date_matrix[index-1-i][1] == date:
				oldsp = date_matrix[index-1-i][-1]
				return oldsp
		else:
			return 0
	return 0

def make_lists(date_matrix, min_lag=1, max_lag=4):
	listofsp = [[] for i in xrange(min_lag, max_lag+1)]
	for num, lst in enumerate(listofsp):
		for i in xrange(len(date_matrix)):
			lst.append(previous_sp(i, date_matrix, num+1))
	return listofsp

def addcolumns(listofsp, df):
	for num, lst in enumerate(listofsp):
		df['SP_'+str(num+1)+'dayago'] = pd.Series(lst, index=df.index)
	return None

def previous_stat(index, Player_Averages, matrix, column, lag=1):
	player = matrix[index][0]
	stat = matrix[index][1]
	index -= lag
	if index >= 0:
		if matrix[index][0] == player:
			statlag = matrix[index][1]
			return statlag
		else:
			return Player_Averages.loc[player, column]
	else:
		return Player_Averages.loc[player, column]

def make_stat_lists(Player_Averages, matrix, column, min_lag=1, max_lag=4):
	listoflist = [[] for i in xrange(max_lag-min_lag+1)]
	for num, lst in enumerate(listoflist):
		for i in xrange(len(matrix)):
			lst.append(previous_stat(i, Player_Averages, matrix, column=column, lag=num+1))
	return listoflist

#dfno0
def add_slag_columns(listoflist, df, name):
	for num, lst in enumerate(listoflist):
		df[name+str(num+1)+'dayago'] = pd.Series(lst, index=df.index)
	return None

def player_average_asfeature(df, df2):
	""" Add the players lifetime averages as a feature

	Parameters
	----------
	df: data frame with all information
	df2: data frame of player averages

	Returns
	-------
	dataframe with last X games as new feature
	"""
	return None 


