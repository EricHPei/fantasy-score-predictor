from __future__ import division
from scipy import stats
import matplotlib.pyplot as plt
import RandomForest
import datetime
import pandas as pd

def something(df, cluster_dict, cluster_num=2, cutoff=0):
	today = datetime.date.today()
	stop_average_date = today - datetime.timedelta(cutoff)
	df_x, df_y = RandomForest.date_with_forest(df, remove_date=False)
	df_x = df_x[df_x['Player Name'].isin(cluster_dict[cluster_num])]
	df_y = df_y[df_y['Player Name'].isin(cluster_dict[cluster_num])]
	before_df_x = df_x[df_x['Date'] <= stop_average_date]
	before_df_y = df_y[df_y['Date'] <= stop_average_date]
	after_df_x = df_x[df_x['Date'] > stop_average_date]
	after_df_y = df_y[df_y['Date'] > stop_average_date]
 	my_cols = list(after_df_x.drop(['Date', 'Player Name'], axis=1).columns)
 	model_dict = RandomForest.make_8_models(before_df_x[my_cols], before_df_y.iloc[:,2:])
 	predictedFG = model_dict['FG'].predict(after_df_x[my_cols])
	predictedFT = model_dict['FT'].predict(after_df_x[my_cols])
	predicted3P = model_dict['3P'].predict(after_df_x[my_cols])
	predictedTRB = model_dict['TRB'].predict(after_df_x[my_cols])
	predictedAST = model_dict['AST'].predict(after_df_x[my_cols])
	predictedSTL = model_dict['STL'].predict(after_df_x[my_cols])
	predictedBLK = model_dict['BLK'].predict(after_df_x[my_cols])
	predictedTOV = model_dict['TOV'].predict(after_df_x[my_cols])
	predictedscores = pd.DataFrame({'index':after_df_x.index, 'FG':predictedFG})
	predictedscores['FT'] = predictedFT
	predictedscores['3P'] = predicted3P
	predictedscores['TOV'] = predictedTOV
	predictedscores['TRB'] = predictedTRB
	predictedscores['STL'] = predictedSTL
	predictedscores['AST'] = predictedAST
	predictedscores['BLK'] = predictedBLK
	predictedscores['SCR'] = 2*predictedscores['FG'] + predictedscores['3P'] + predictedscores['FT'] \
							+ 1.2*predictedscores['TRB'] + 1.5*predictedscores['AST'] + 2*\
							predictedscores['BLK'] + 2*predictedscores['STL'] - predictedscores['TOV']
	return predictedscores, after_df_y