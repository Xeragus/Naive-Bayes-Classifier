import csv
import random
import math

# method to load the .csv file and return a dataset with it's contents
def read_csv(filename):
	# read the lines
	lines = csv.reader(open(filename, "rt"))
	# dataset is a list of the lines read previously
	dataset = list(lines)
	# iterate through all the lines in the dataset and convert them
	for i in range(len(dataset)):
		# print(dataset[i])
		# convert the lines into list of float number
		# ['1', '102', '74', '0', '0', '39.5', '0.293', '42', '1']
		# [1.0, 102.0, 74.0, 0.0, 0.0, 39.5, 0.293, 42.0, 1.0]
		dataset[i] = [float(x) for x in dataset[i]]
		# print(dataset[i])
	# return the modified dataset
	return dataset

# method to print the content of the whole dataset
def print_dataset(dataset):
	for row in dataset:
		print(row)

# spliting the dataset into training dataset (67%) and testing dataset (33%)
def dataset_split(dataset, spliting_ratio):
	# the size of the training dataset depends on the spliting ratio
	training_size = int(len(dataset) * spliting_ratio)
	# define the training dataset as a list
	training_dataset = []
	# create a copy of the dataset
	dataset_copy = list(dataset)
	# loop until we fill the capacity of the training dataset
	while len(training_dataset) < training_size:
		# get the position (index) in the list
		position_index = random.randrange(len(dataset_copy))
		training_dataset.append(dataset_copy.pop(position_index))
	return [training_dataset, dataset_copy]

# separate data by class
def class_separation(dataset):
	# dictionary with classes and the lists of data instances in that class
	class_dictionary = {}
	# loop through the dataset
	for index in range(len(dataset)):
		temp_var = dataset[index]
		# the last attribute (-1) is the last attribute
		if(temp_var[-1] not in class_dictionary):
			class_dictionary[temp_var[-1]] = []
		# fill the class dictionary
		class_dictionary[temp_var[-1]].append(temp_var)
	return class_dictionary

# calculate the mean of each attribute for a class value
def calculate_mean(data):
	# 'data' is a list of numbers, ex: data = [5, 2, 3, 1, 2]
	return sum(data)/float(len(data))

# calculate the standard deviation by formula
def calculate_standard_deviation(data):
	# 'data' is a list of numbers, ex: data = [5, 2, 3, 1, 2]
	# std_dev = square root of the variance
	# variance = average of the squared differences for each attribute value from the mean, with n-1 method
	average = calculate_mean(data)
	variance = sum([pow(x-average,2) for x in data])/float(len(data)-1)
	return math.sqrt(variance)

# calculate the mean and standard deviation for each attribute
def calculate_summary(dataset):
	summaries = [(calculate_mean(attribute), calculate_standard_deviation(attribute))
		for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

# calculate the summaries for each attribute
def calculate_class_summary(dataset):
	class_separated = class_separation(dataset)
	# define a dictionary
	summaries = {}
	for value, instances in class_separated.items():
		summaries[value] = calculate_summary(instances)
	return summaries

# calculate the probability of an attribute belonging to a class
def calculate_probability(x, mean, standard_deviation):
	e = math.exp(-(math.pow(x-mean,2)/(2*math.pow(standard_deviation,2))))
	return (1 / (math.sqrt(2*math.pi) * standard_deviation)) * e

# combine the probabilities of all the attribute values for a data instance
# and calculate the probability of the entire data instance belonging to a class
def combine_probabilities(summaries, input_vector):
	probabilities = {}
	for class_type, class_summaries in summaries.items():
		probabilities[class_type] = 1
		for i in range(len(class_summaries)):
			mean, standard_deviation = class_summaries[i]
			x = input_vector[i]
			probabilities[class_type] *= calculate_probability(x, mean, standard_deviation)
	return probabilities

# look for the largest probability and return the associated class
def find_largest_probability(summaries, input_vector):
	probabilities = combine_probabilities(summaries, input_vector)
	largest_class_type = None
	best_probability = -1
	# looking for the maximum probability
	for class_type, probability in probabilities.items():
		if largest_class_type is None or probability > best_probability:
			best_probability = probability
			largest_class_type = class_type
	return largest_class_type

def test_largest_probability():
	summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
	input_vector = [1.1, '?']
	print(find_largest_probability(summaries, input_vector))

# test written for the class_separation method
def test_class_separation():
	dataset = [[42,4,0], [1,77,0], [31,8,1]]
	class_dictionary = class_separation(dataset)
	print(class_dictionary)	

# test written for the calculate_mean and calculate_standard_deviation methods
def test_mean_and_standard_deviation():
	data = [5,4,3,2,1]
	print("Mean and standard deviation for {0}".format(data))
	print("mean = {0}, standard_deviation = {1}"
		.format(calculate_mean(data), calculate_standard_deviation(data)))

# test written for the read_csv and print_dataset methods
def test_read_and_print_dataset():
	dataset = read_csv(filename)
	print_dataset(dataset)

# test written for the calculate_summaries method
def test_calculate_summary():
	# tester dataset
	dataset = [[3,19,1],[1,25,0],[4,20,0]]
	print("Mean and standard deviation calculated for each attribute")
	print(calculate_summary(dataset))

# test written for the calculate_class_summary
def test_calculate_class_summary():
	dataset = [[1,20,1],[2,21,0],[3,22,1],[4,22,0]]
	summary = calculate_class_summary(dataset)
	print(summary)

def test_calculate_probability():
	# the first argument is x, the second is the mean and the last is the standard deviation
	print(calculate_probability(71.5, 73, 6.2))

def test_combine_probabilities():
	summaries = {0:[(1, 0.5)], 1:[(20, 5.0)]}
	tester = [1.1, '?']
	print(combine_probabilities(summaries, tester))

# specify the name of the file
filename = 'pima-indians-diabetes.data.csv'