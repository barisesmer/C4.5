import numpy as np
from utils import *
class C45:

	"""Creates a decision tree with C4.5 algorithm"""
	def __init__(self, data, is_categorical):
		self.tree = None

		self.add_data(data, is_categorical)

	def add_data(self, data, is_categorical):
		self.data = data
		self.attrs = data.columns[:-1].to_numpy()
		self.output_label = data.columns[-1]
		self.is_categorical = {a[0] : a[1] for a in zip(self.attrs, is_categorical)}

		self.attr_vals = {a : (self.data[a].unique() if self.is_categorical[a] else None) for a in self.attrs}

	def generate_tree(self):
		self.tree = self.recursive_generate_tree(None, self.data, self.attrs)

	def recursive_generate_tree(self, parent, cur_data, cur_attributes):
		if len(cur_data) == 0:
			# no datapoints left, return a leaf node with parents label
			return Leaf(parent.label)
		elif len(cur_data[self.output_label].unique()) == 1:
			# all datapoints belong to the same class, return a leaf node with that label
			return Leaf(cur_data[self.output_label].unique()[0])
		elif len(cur_attributes) == 0:
			# return a leaf node with the majority label
			return Leaf(cur_data[self.output_label].mode().iloc[0])
		else:
			# need to split over an attribute
			attr, partitions = self.choose_attribute(cur_data, cur_attributes)

			# create a Node
			node = Node(attr)

			next_attributes = cur_attributes.delete(attr)

			node.children = {attr_val:self.recursive_generate_tree(node, partition, next_attributes) for attr_val,partition in partitions}

			return node

	def choose_attribute(self, cur_data, cur_attributes):
		attr, d, _ = max( ((attr, *self.split(cur_data, attr)) for attr in cur_attributes), key = lambda x : x[-1])

		return attr, d

	def split(self, cur_data, attribute):
		if self.is_categorical[attribute]:
			partitions =  [(attr_val, cur_data[cur_data[attribute] == val]) for attr_val in self.attr_vals[attribute]]

			gain_rt = gain_ratio(cur_data, list(d.values()))
		else:
			# sort according to attribute
			thres_value, S = numerical_best_split(cur_data, attribute)

			partitions = [ (thres_value , S[0]), (thres_value + 0.001, S[1]) ]

			gain_rt = thres_value

		return partitions, gain_rt
	
	def printTree(self):
		self.printNode(self.tree)

	def printNode(self, node, indent=""):
		if not node.isLeaf:
			if node.threshold is None:
				#discrete
				for index,child in enumerate(node.children):
					if child.isLeaf:
						print(indent + node.label + " = " + attributes[index] + " : " + child.label)
					else:
						print(indent + node.label + " = " + attributes[index] + " : ")
						self.printNode(child, indent + "	")
			else:
				#numerical
				leftChild = node.children[0]
				rightChild = node.children[1]
				if leftChild.isLeaf:
					print(indent + node.label + " <= " + str(node.threshold) + " : " + leftChild.label)
				else:
					print(indent + node.label + " <= " + str(node.threshold)+" : ")
					self.printNode(leftChild, indent + "	")

				if rightChild.isLeaf:
					print(indent + node.label + " > " + str(node.threshold) + " : " + rightChild.label)
				else:
					print(indent + node.label + " > " + str(node.threshold) + " : ")
					self.printNode(rightChild , indent + "	")





	def recursiveGenerateTree(self, curData, curAttributes):
		allSame = self.allSameClass(curData)

		if len(curData) == 0:
			#Fail
			return Node(True, "Fail", None)
		elif allSame is not False:
			#return a node with that class
			return Node(True, allSame, None)
		elif len(curAttributes) == 0:
			#return a node with the majority class
			majClass = self.getMajClass(curData)
			return Node(True, majClass, None)
		else:
			(best,best_threshold,splitted) = self.splitAttribute(curData, curAttributes)
			remainingAttributes = curAttributes[:]
			remainingAttributes.remove(best)
			node = Node(False, best, best_threshold)
			node.children = [self.recursiveGenerateTree(subset, remainingAttributes) for subset in splitted]
			return node

	def getMajClass(self, curData):
		freq = [0]*len(self.classes)
		for row in curData:
			index = self.classes.index(row[-1])
			freq[index] += 1
		maxInd = freq.index(max(freq))
		return self.classes[maxInd]


	def allSameClass(self, data):
		for row in data:
			if row[-1] != data[0][-1]:
				return False
		return data[0][-1]

	def isAttrDiscrete(self, attribute):
		if attribute not in self.attributes:
			raise ValueError("Attribute not listed")
		elif len(self.attrValues[attribute]) == 1 and self.attrValues[attribute][0] == "continuous":
			return False
		else:
			return True

	def splitAttribute(self, curData, curAttributes):
		splitted = []
		maxEnt = -1*float("inf")
		best_attribute = -1
		#None for discrete attributes, threshold value for continuous attributes
		best_threshold = None
		for attribute in curAttributes:
			indexOfAttribute = self.attributes.index(attribute)
			if self.isAttrDiscrete(attribute):
				#split curData into n-subsets, where n is the number of 
				#different values of attribute i. Choose the attribute with
				#the max gain
				valuesForAttribute = self.attrValues[attribute]
				subsets = [[] for a in valuesForAttribute]
				for row in curData:
					for index in range(len(valuesForAttribute)):
						if row[i] == valuesForAttribute[index]:
							subsets[index].append(row)
							break
				e = gain(curData, subsets)
				if e > maxEnt:
					maxEnt = e
					splitted = subsets
					best_attribute = attribute
					best_threshold = None
			else:
				#sort the data according to the column.Then try all 
				#possible adjacent pairs. Choose the one that 
				#yields maximum gain
				curData.sort(key = lambda x: x[indexOfAttribute])
				for j in range(0, len(curData) - 1):
					if curData[j][indexOfAttribute] != curData[j+1][indexOfAttribute]:
						threshold = (curData[j][indexOfAttribute] + curData[j+1][indexOfAttribute]) / 2
						less = []
						greater = []
						for row in curData:
							if(row[indexOfAttribute] > threshold):
								greater.append(row)
							else:
								less.append(row)
						e = self.gain(curData, [less, greater])
						if e >= maxEnt:
							splitted = [less, greater]
							maxEnt = e
							best_attribute = attribute
							best_threshold = threshold
		return (best_attribute,best_threshold,splitted)

	def gain(self,unionSet, subsets):
		#input : data and disjoint subsets of it
		#output : information gain
		S = len(unionSet)
		#calculate impurity before split
		impurityBeforeSplit = self.entropy(unionSet)
		#calculate impurity after split
		weights = [len(subset)/S for subset in subsets]
		impurityAfterSplit = 0
		for i in range(len(subsets)):
			impurityAfterSplit += weights[i]*self.entropy(subsets[i])
		#calculate total gain
		totalGain = impurityBeforeSplit - impurityAfterSplit
		return totalGain

	def entropy(self, dataSet):
		S = len(dataSet)
		if S == 0:
			return 0
		num_classes = [0 for i in self.classes]
		for row in dataSet:
			classIndex = list(self.classes).index(row[-1])
			num_classes[classIndex] += 1
		num_classes = [x/S for x in num_classes]
		ent = 0
		for num in num_classes:
			ent += num*self.log(num)
		return ent*-1


	def log(self, x):
		if x == 0:
			return 0
		else:
			return math.log(x,2)