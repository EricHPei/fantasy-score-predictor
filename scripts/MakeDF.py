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
	return None

def create_df(folder):
	'''
	INPUT: folder where all the combined files are
	OUTPUT: df
	Goes through each file and adds it to the data frame
	'''
	path = '..alldata/alldata'
	allFiles = glob.glob(path + "/*.csv")
	list_ = []
	for file_ in allFiles:
	    df = pd.read_csv(file_,index_col=None, header=None)
	    list_.append(df)
	df = pd.concat(list_)
	df = df.reset_index()
	df.columns = ['index','Player Name','MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%',\
				'ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-','TS%','eFG%','3PAr',\
				'FTr','ORB%','DRB%','TRB%','AST%','STL%','BLK%','TOV%','USG%','ORtg','DRtg','Away',\
				'Home','OneisHome','Date']
	return df

def add_features(df):
	'''
	INPUT: raw df
	OUTPUT: featured df
	Goes through each file and adds it to the data frame
	'''
	df['Suspended'] = df['MP'].apply(lambda x: 1 if x=="Player Suspended" else 0)
	df['MP'] = df['MP'].apply(lambda x: 0:00 if x=="Did Not Play" or x=="Player Suspended" else x)
	df['MP1']=pd.to_datetime(df.MP, format = "%M:%S")
	ms_split = df['MP'].apply(lambda x: x.split(":"))
	ms_split = df['MP'].apply(lambda x: x.split(":"))
	df['SP'] = seconds_played
	df = df.drop(['index', 'MP1', 'MP'], axis=1)
	return df

def clean_df(df):
	'''
	INPUT: messy data frame
	OUTPUT: data frame filling NA, without reserves, and columns typecasted correctly
	'''
	df = df.fillna(0)
	df = df[df['Player Name']!= 'Reserves']
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

def make_averages(df):
	'''
	INPUT: messy data frame
	OUTPUT: data frame with player averages
	'''	
	Player_Averages = df.groupby(df['Player Name']).mean()[['SP', '3P', 'FG', 'FT', 'TRB', \
																	'AST', 'BLK', 'STL', 'TOV']]
	Player_Averages['Score'] = 2*Player_Averages['FG'] + Player_Averages['3P'] + Player_Averages['FT'] \
                            + 1.2*Player_Averages['TRB'] + 1.5*Player_Averages['AST'] + 2*\
                            Player_Averages['BLK'] + 2*Player_Averages['STL'] - Player_Averages['TOV']
    return Player_Averages

def previous_stat(index, matrix=tp_matrix, lag=1, column='3P', Player_Averages):
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

def make_stat_lists(min_lag=1, max_lag=4, matrix=tp_matrix, column='3P'):
    listoflist = [[] for i in xrange(max_lag-min_lag+1)]
    for num, lst in enumerate(listoflist):
        for i in xrange(len(matrix)):
            lst.append(previous_stat(i, matrix, lag=num+1, column=column))
    return listoflist

#dfno0
def add_slag_columns(listoflist, df, name='TP'):
    for num, lst in enumerate(listoflist):
        df[name+str(num+1)+'dayago'] = pd.Series(lst, index=df.index)
    return None
