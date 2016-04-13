import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def kmeanscluster_ready(eigenvector, player_average):
	'''
	input second item
	Input: Player_average with cutoff date to determine clusters
	Output: 2p X n matrix to feed to kmeans
	'''
	return None

def get_player_list(df):
	'''
	Input: df
	Output: get array of unique player names
	'''
	return df['Player Name'].unique()

def get_individual_df(name):
	'''
	Input: name
	Output: get data frame of player
	'''
	return df['Player Name'] == name

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

def run_pca(df):
	'''
	Input: data frame (pca_nomnom)
	Output: pca matrix and eigenvectors
	'''
    pca              = PCA(n_components=8, whiten=True)
    pca.fit(df)
    top95percent_PC  = get_95_var(pca.explained_variance_ratio_)
    pca.n_components = top95percent_PC
    X_reduced        = pca.fit_transform(df)
    PCA_matrix       = pd.DataFrame(X_reduced)
    return(PCA_matrix, pca.components_)

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
        print pos-1, total
        if total>=0.95:
            #print total
            return(pos)




