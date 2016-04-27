import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import defaultdict

def get_player_list(df):
	'''
	Input: df
	Output: get array of unique player names
	'''
	
	return df['Player Name'].unique()

def get_individual_df(name, df):
	'''
	Input: name, df
	Output: get data frame of player
	'''
	return df[df['Player Name'] == name]

def individual_to_pca(df):
	'''
	Input: df of one player DF
	Output: Cleaned DF with only columns to feed PCA
	'''
	bad_columns = ['Player Name', 'Away', 'Home', 'OneisHome', 'Date', 'DateM1', 'DateM2', 'DateM3', 'DateM4']
	cols_to_use = [x for x in df.columns if x not in bad_columns]
	df_to_use = df[cols_to_use]
	pca_nomnom = df_to_use[['FG','FG','3P','TRB', 'AST', 'STL', 'BLK', 'TOV']]
	return pca_nomnom

def get_lst_pca(df):
	'''
	Input: df
	Output: list of pca
	'''
	pca_lst = []
	players = get_player_list(df)
	for player in players:
		pca_lst.append((player, individual_to_pca(get_individual_df(player, df))))
	return pca_lst

def run_pca(df):
	'''
	Input: data frame (pca_nomnom)
	Output: pca matrix and eigenvectors
	'''
	pca              = PCA(n_components=3, whiten=True)
	pca.fit(df)
	X_reduced        = pca.fit_transform(df)
	PCA_matrix       = pd.DataFrame(X_reduced)
	return(PCA_matrix, pca.components_)

def kmeanscluster_ready(pca_lst, player_average):
	'''
	input second item
	Input: Player_average with cutoff date to determine clusters
	Output: 2p X n ndarray to feed to kmeans
	'''
	aray = np.zeros((len(pca_lst), 17))
	PA = player_average.reset_index()
	for i, (player, df) in enumerate(pca_lst):
		PCA_matrix, Eigenvectors = run_pca(df)
		p_avg = PA[PA['Player Name']== player]
		p = p_avg.iloc[:,1:-1].values
		kclusterme = np.append(p, Eigenvectors[0])
		if kclusterme.shape == (17,):
			aray[i] = kclusterme
	return aray


def get_95_var(array):
	'''
	Input: array
	Output: return eigenvectors up untl PCA explains .95+ of variance
	'''
	total = 0
	pos = 0
	for x in array:
		total += x
		pos   += 1
		if total>=0.95:
			return(pos)

def make_cluster_dictionary(km,PA):
	'''
	Input: model, player average
	Output: dictionary
	'''
	cluster_dictionary = {}
	for cluster, player in zip(km.labels_, PA.index.values):
		cluster_dictionary[player] = cluster
	return cluster_dictionary

def make_cluster_dictionary2(km,PA):
	'''
	Input: model, player average
	Output: dictionary
	'''
	cluster_dictionary = defaultdict(list)
	for player, cluster in zip(PA.index.values, km.labels_):
		cluster_dictionary[cluster].append(player)
	return cluster_dictionary

