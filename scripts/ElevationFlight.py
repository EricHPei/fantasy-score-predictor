import pandas as pd
import numpy as np

def read_to_dict():
	Elevation = pd.read_csv('score-predictor/data/Elevation.csv', delimiter=' ', header=None)
	elev = {k:int(v) for (k, v) in zip(Elevation[0], Elevation[3])}
	return elev

def lookup_and_add(dictionary, df):
	df['Elevation'] = [dictionary[i] for i in df['Home']]
	return None