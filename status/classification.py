'''
This file contains the class 'Classification', 
which contains the main script that the user will interface with. 
It is to be executed in the format: python classification.py <input_file> <output_file>. 
'''
#Import the built-in 'system' library.
import sys
#Import Pandas
import pandas as pd
#Import Numpy
import numpy as np
#Import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
#Import Pickle
import pickle
#Import json
import json
#Import the dictionary of types
from type_dict import type

#Import the config.json file
with open('config.json') as data_file:    
    config = json.load(data_file)

class Classification:
	#The following method intializes the Classification class by taking in the input file and predicting source types.
	def __init__(self, input_path):
		
		#Read the input csv file into a dataframe
		self.df = pd.read_csv(input_path, dtype=object).fillna('')
		
		# Extract the one feature '#status' to be used
		feature = self.df[config['attribute_label']].astype(str)

		vocab = list(np.load(config['model_folder'] + "/" + config['features_file_name']))
		
		# Use sklearn 's CountVectorizer to extract word count for the infered token list.
		model = CountVectorizer(analyzer='word', vocabulary = vocab)
		
		model._validate_vocabulary()
		
		#Extract the infered token list.
		feature_names = np.array(model.get_feature_names())

		#Fit and transform
		X = model.fit_transform(feature)

		# Convert it into dense matrix representation form
		X = X.toarray()


		#Extract the infered token list.
		feature_names = np.array(model.get_feature_names())
		
		#Create an empty list that will hold the predicted source types
		self.predicted = []
		
		#Fetch and invoke the saved model
		with open(config['model_folder'] + "/" + config['model_file_name'], 'rb') as f:
			clf = pickle.load(f)

		predicted = clf.predict(X)
		for arr in predicted:
			labels = [type[i] for i, k in enumerate(arr) if k > 0]
			final_label = ','.join(list(labels))
			self.predicted.append(final_label)
				

	#The following method is called to generate the output csv file, once categorization is complete after initialization
	def generate_csv(self, output_path):
		#Create a copy of the original dataframe
		new_df = self.df.copy()
		#Append the self.predicted list as the new column
		new_df[config['class_label']] = self.predicted
		#Save the new dataframe to the intended output_path
		new_df.to_csv(output_path, index=False)
		print "-------------------------------------------------"
		print "Classification successful: output file saved to: " + output_path
		print "-------------------------------------------------"
	
# Read the command arguments
args = sys.argv
#validate number of arguments.(The first is always the filename)
if len(args) != 3:
	sys.exit("Incorrect Format. Please enter: python classification.py <input_file> <output_file>")

#Extract the input and output file names
input_path = args[1]
output_path = args[2]

#Create a 'Classification' object, which will directly call the __init__ method
classifier = Classification(input_path)
#Call the generate_csv method to generate the output file
classifier.generate_csv(output_path)
