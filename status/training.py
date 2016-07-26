'''
This file contains the class 'Training', 
which contains the script that the user will interface with to train/retrain the model. 
It is to be executed in the format: python training.py <training_file>. 
'''
#Import the built-in 'system' library.
import sys
#Import Pandas
import pandas as pd
#Import Numpy
import numpy as np
#Import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
#Import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
#Import GridSearchCV
from sklearn.grid_search import GridSearchCV
#Import Pickle
import pickle
#Import json
import json
# Suppress scientific notation
np.set_printoptions(suppress = True)
#np.set_printoptions(threshold=np.nan)

#Import the config.json file
with open('config.json') as data_file:    
    config = json.load(data_file)


class Training:
	#The following method intializes the Training class by taking in the input file and trains, hypertunes and then saves a new model.
	def __init__(self, input_path):
		# Read the file, replace NAs with empty string
		df = pd.read_csv(input_path, dtype = object).fillna('')
		
		# Extract the one feature '#status' to be used
		feature = df[config['attribute_label']].astype(str)
		
		# Use sklearn 's CountVectorizer to extract word count for the infered token list.
		model = CountVectorizer(analyzer='word')

		#Fit and transform
		X = model.fit_transform(feature)
		
		#Extract the infered token list as an numpy array.
		feature_names = np.array(model.get_feature_names())

		#The numpy array will be persisted on disk for use by classification.py
		np.save(config['model_folder'] + "/" + config['features_file_name'], feature_names)

		# Convert it into dense matrix representation form
		self.X = X.toarray()
		
		# Extract he label column and codify it into numeric form
		uniques = df[config['class_label']]
		
		#Replace blank class with null, so that it's not ignored by the countVectorizer. We will account for it by specifying the correct value in the index in type_dict.py
		uniques = uniques.replace({'': 'null'})

		#To generate a multilabel sparse matrix, we'll use:
		model = CountVectorizer(analyzer='word')
		

		#Fit and transform
		uniques = model.fit_transform(uniques)

		#Convert labels matrix from dense form to sparse form
		self.y = uniques.toarray()

	def save_model(self):
	
		# Change to binary form: keyword present(1) or not present(0)
		#self.X[self.X > 1] = 1

		#Set the base random forest estimator.
		base_clf = RandomForestClassifier()

		print "-------------------------------------------------"
		print "Hyper-tuning the Random Forest to find the best performer."
		print "-------------------------------------------------\n"
		
		# We'll use grid search for RF estimator, and use fold cross validation to hypertune.
		clf = GridSearchCV(base_clf, config['rf_learn_hyperparameters'], cv = config['cv_count'])

		# Fit the available dataset to it.
		clf.fit(self.X, self.y)

		print "-------------------------------------------------"
		print "Best grid search accuracy:"
		print clf.best_score_
		print "-------------------------------------------------\n"
		print "Best parameters set found on development set:"
		print clf.best_params_

		# Isolate the best performing estimator
		best_clf = clf.best_estimator_
		
		print best_clf.predict(self.X)

		#Save the best model to disk.
		with open(config['model_folder'] + "/" + config['model_file_name'], 'wb') as f:
			pickle.dump(best_clf, f)
		print "-------------------------------------------------"
		print "Training successful: A new random forest model has been trained, tuned and saved.\n"

# Read the command arguments
args = sys.argv

# validate number of arguments.(The first is always the filename)
if len(args) != 2:
    sys.exit("Incorrect Format. Please enter: python training.py <training_data_file>")

# Extract the training file name
file_path = args[1]
#Create a 'Training' object, which will directly call the __init__ method
trainer = Training(file_path)
#Call the save_model method to save the model.
trainer.save_model()

