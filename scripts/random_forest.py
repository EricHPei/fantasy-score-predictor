import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot
import datetime

def prepare_for_forest(df):
	'''
	restructures a single data frame to return a Xdf and Ydf ready to feed to random forest

	@param df: entire data frame X and Y
	@return forest_df: data frame of features that is ready for random forest
	@return y_df: data frame of values we are trying to predict that is ready for random forest
	'''
	forest_df = df.iloc[:,43:]
	forest_df[['Player Name','OneisHome']] = df[['Player Name','OneisHome']]
	y_df = df[['Player Name','3P','FG','FT','TRB','AST','BLK','STL','TOV']]

	return forest_df, y_df

def date_with_forest(df, cutoff=0, remove_date=True):
	'''
	returns a X and Y ready to feed to random forest

	@param df: entire data frame with features and values we are trying to predict
	@param cutoff: how many days to not include in our data frame
	@param remove_date: True or False depending if you want the date column to be returned
	@return forest_df: data frame with relevant features to feed to random forest
	@return y_df: data frame of items we want to predict without date
	'''
	today = datetime.date.today()
	stop_average_date = today - datetime.timedelta(cutoff)
	df = df[df['Date'] < stop_average_date]
	forest_df = df.iloc[:,43:]
	forest_df[['Player Name','OneisHome','Date']] = df[['Player Name','OneisHome', 'Date']]
	y_df = df[['Player Name','Date','3P','FG','FT','TRB','AST','BLK','STL','TOV']]
	if remove_date == True:
	 	forest_df = forest_df.ix[:, forest_df.columns != 'Date']
	 	y_df = y_df.ix[:, y_df.columns != 'Date']
	return forest_df, y_df

def individual_forest_df(forest_df, y_df, player):
	'''
	returns the data frames for a single player

	@param forest_df: data frame of features
	@param y_df: data frame of what we are trying to predict
	@param player: player name
	@return player: player name
	@return player_x: specific player's data frame of features
	@return player_y: specific player's data frame of values we are trying to predict
	'''	
	player_x = forest_df[forest_df['Player Name'] == player]	
	player_y = y_df[y_df['Player Name'] == player]
	return player, player_x, player_y

def crossval_player(player, player_x, player_y, cat=1):
	'''
	train test split for a single player for a single category in the data frame

	1 = 3p
	2 = FG
	3 = FT 
	4 = TRB
	5 = AST
	6 = BLK
	7 = STL
	8 = TOV

	player_y = steph_predict
	player_x = StephCurry_df
	player = Steph Curry

	@param player: player name
	@param player_x: players features
	@param player_y: players predictions
	@param cat: category number to associate with cat
	@return X_train: inputs to train with
	@return X_test: inputs to test with
	@return y_train: outputs to train model with
	@return y_test: ouputs to crossvalidate with
	'''
	X_train, X_test, y_train, y_test = train_test_split(player_x[list(player_x.columns-['Player Name'])], player_y.iloc[:,cat], test_size = 0.25, random_state = 30)
	return X_train, X_test, y_train, y_test

def make_8_models(df, y):
	'''
	generates a dictionary of models
	
	@param df: data frame (X) of features
	@param y: data frame (y) to predict
	@return model_dict: dictionary of models
	'''
	model_dict = {}
	for column in y.columns:
		model_dict[column] = RandomForestRegressor(n_estimators=100)
		model_dict[column].fit(df, y[column])
	return model_dict



def make_predictions(d, x_test):
	''' 
	Pass in dictionary of models and what we are trying to predict

	@param d: dictionary 
	@param x_test: pass in what we want to predict
	@return predictions: predict stuff
	'''
	for cat, model in d.iteritems():
		model.predict(x_test[cat])
