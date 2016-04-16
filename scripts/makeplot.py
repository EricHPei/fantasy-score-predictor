from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
	


def make_plots(df):
	estimators = {'k_means_bball_4': KMeans(n_clusters=4, random_state=30),
					'k_means_bball_5': KMeans(n_clusters=5, random_state=30),
					'k_means_bball_6': KMeans(n_clusters=6, random_state=30)}
	fignum = 1
	for name, est in estimators.items():
		fig = plt.figure(fignum, figsize=(12, 9))
		plt.clf()
		ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

		plt.cla()
		est.fit(df)
		labels = est.labels_

		ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2], c=labels.astype(np.float))

		ax.w_xaxis.set_ticklabels([])
		ax.w_yaxis.set_ticklabels([])
		ax.w_zaxis.set_ticklabels([])
		ax.set_xlabel('Principal Component 1')
		ax.set_ylabel('Principal Component 2')
		ax.set_zlabel('Principal Component 3')
		name1 = str(est.n_clusters)
		plt.savefig('score-predictor/img/' + name1 + '.png')
		# for i in np.linspace(45,360,8):
		# 	ax.view_init(45-i,0)
		# 	plt.savefig('score-predictor/img/' + name1 + 'clusters' + str(i) + '.png')
		fignum = fignum + 1
	return None