import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot
import datetime

def prepare_for_forest(df):
	'''
	Input: Data Frame
	Output: X and Y Data Frame ready to feed to random forest
	y_df = predict_df
	Given my huge data frame, returns a data frame ready for random forest.
	'''
	forest_df = df.iloc[:,43:]
	forest_df[['Player Name','OneisHome']] = df[['Player Name','OneisHome']]
	y_df = df[['Player Name','3P','FG','FT','TRB','AST','BLK','STL','TOV']]

	return forest_df, y_df

def individual_forest_df(forest_df, y_df, player):
	'''
	Input: forest_df, y_df, player(or index)
	Output: player, X and Y Data Frame ready to feed to random forest for one player
	Given my data frame ready for random forest, returns data ready to feed just for the specified player
	player_y = steph_predict
	'''	
	player_x = forest_df[forest_df['Player Name'] == player]
	player_y = y_df[y_df['Player Name'] == player]
	return player, player_x, player_y

def crossval_player(player, player_x, player_y, cat=1):
	'''
	Input: Player Name, Players Data Frame, y_df
	Output: X and Y Data Frame ready to feed to random forest
	y_df = predict_df
	cat =
	1 = 3p
	2 = FG
	3 = FT 
	4 = TRB
	5 = AST
	6 = BLK
	7 = STL
	8 = TOV
	# player_y = steph_predict
	# player_x = StephCurry_df
	# player = Steph Curry
	'''
	X_train, X_test, y_train, y_test = train_test_split(player_x[player_x.columns-['Player Name']], player_y.iloc[:,cat], test_size = 0.25, random_state = 30)
	return X_train, X_test, y_train, y_test

def date_with_forest(df, cutoff=0):
	'''
	Input: Data Frame
	Output: X and Y Data Frame ready to feed to random forest
	y_df = predict_df
	Given my huge data frame, returns a data frame ready for random forest.
	'''
	today = datetime.date.today()
	stop_average_date = today - datetime.timedelta(cutoff)
	df = df[df['Date'] < stop_average_date]
	forest_df = df.iloc[:,43:]
	forest_df[['Player Name','OneisHome','Date']] = df[['Player Name','OneisHome', 'Date']]
	y_df = df[['Player Name','Date','3P','FG','FT','TRB','AST','BLK','STL','TOV']]

	return forest_df, y_df

