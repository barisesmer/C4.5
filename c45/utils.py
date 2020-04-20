import numpy as np

class Node:
	def __init__(self, attribute):
		self.attribute = attribute
		self.is_leaf = False

		# self.children = {}

class Leaf(Node):
	def __init__(self, label):
		self.label = label
		self.is_leaf = True

def numerical_best_split(data, attribute):
	sorted = data.sort_values(by = attribute, inplace = False)

	labels = data.iloc[:,-1]

	best_val = None
	best_gain_rt = -np.inf

	for i in range(len(labels) - 1):
		if labels[i] != labels[i+1]:
			S1, S2 = data.iloc[:(i+1),:], data.iloc[(i+1):, :]
			
			gain_rt = gain_ratio(data, [S1,S2])

			if gain_rt > best_gain_rt:
				best_gain_rt = gain_rt
				best_val = np.mean(data[attribute][i:i+2])

	return best_val, [data.iloc[:(i+1),:], data.iloc[(i+1):, :]]


def expected_information(T):
	"""Returns the expected information required to classify a datapoint in T to its class
	
	Args:
		T (pandas Dataframe): Dataset to be considered
	"""

	freq = T.iloc[:,-1].value_counts().to_numpy().astype(dtype=np.float64)

	freq /= sum(freq)

	return -np.dot( freq, np.log2( freq, where=(freq != 0) ) )

def expected_information_split(S):
	"""Returns the average expected information given the split S
	
	Args:
		S (list): A list of pandas Dataframes that represent the split due to an attribute
	"""

	freq = np.array([len(x) for x in S], dtype =np.float64)

	freq /= sum(freq)

	return sum(f * expected_information(S_f) for f, S_f in zip(freq, S))
	
def information_gain(T, S):
	"""Returns the information gain that arises from dividing T into S_1, ..., S_m
	
	Args:
		T (pandas Dataframe): Dataset to be split
		S (list): Partitions of T, each a pandas Dataframe
	"""

	return expected_information(T) - expected_information_split(S)

def gain_ratio(T, S):
	"""Returns the gain ratio that arises from dividing T into S_1, ..., S_m
	
	Args:
		T (pandas Dataframe): Dataset to be split
		S (list): Partitions of T, each a pandas Dataframe
	"""
	freq = np.array([len(x) for x in S], dtype=np.float64)

	freq /= sum(freq)

	split_info = -np.dot( freq, np.log2( freq, where=(freq != 0) ) )

	return information_gain(T,S)/split_info