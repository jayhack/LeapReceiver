#!/usr/bin/python
# *------------------------------------------------------------ *
# * Class: Gesture_Recognizer
# * -------------------------
# * everything related to recognizing gestures in max
# *
# *  
# *------------------------------------------------------------ *

#--- Standard ---
import os
import sys
import pickle
import random
from operator import itemgetter 
from collections import defaultdict

#--- My Files ---
### NOTE: change the path below to the location of your local installation of ***scipy*** ###
sys.path.append ('/Users/jayhack/anaconda/lib/python2.7/site-packages/scipy/')
from common_utilities import print_message, print_error, print_status, print_inner_status
from Gesture import Gesture

#--- SKLearn ---
import numpy as np
from sklearn.hmm import GaussianHMM
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation


class Gesture_Recognizer:

	#--- Filenames ---
	data_dir 				= os.path.join 	(os.getcwd(), 'data/')
	classifiers_dir 		= os.path.join 	(os.getcwd (), 'classifiers/')
	hmms_filename 			= os.path.join	(classifiers_dir, 'hmms.pkl')
	classifier_filename 	= os.path.join 	(classifiers_dir, 'classifier.pkl')
	gesture_dirs 			= {}	# dict: gesture_type -> directory containing recorded examples


	#--- Recording ---
	is_recording 		= False		# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	recording_gesture 	= None		# the gesture we will record to.


	#--- Data ---
		#--- Gesture objects ---
	gesture_types = []		# list of all types of gestures
	gestures = {}			# dict: gesture_type -> list of gesture objects
		#--- Classifiable examples ---
	all_examples = []		# list of all examples of gestures in appropriate format for LR. (features, label) tuples.
	training_examples = []	# list of training examples for the classifier. (features, label) tuples.
	testing_examples = []	# list of all testing examples for the classifier. (features, label) tuples.


	#--- Classifiers/Probabilistic Modesl ---
	hmms = {}							# dict mapping gesture_type -> gaussian hmm
	classifier = LogisticRegression ()	# softmax regression classifier


	#--- Parameters ---
	num_hmm_states 					= 7		# number of states in HMM
	training_examples_proportion	= 0.75	# amount of data to train on
	prediction_prob_threshold		= 0.8



	# Function: Constructor
	# ---------------------
	# load data and train model
	def __init__ (self):
		
		### Step 1: initialize self.gestures ###
		self.gestures = {}

		### Step 2: get all gesture types ###
		self.get_gesture_types ()

		### Step 3: get all gesture dirs ###
		self.get_gesture_dirs () 



	########################################################################################################################
	##############################[ --- Data Filename Management --- ]###########################################################
	########################################################################################################################

	# Function: get_gesture_types
	# ---------------------------
	# fills in self.gesture_types by observing all the directories
	# in self.data_dir, with the exception of .DS_Store
	def get_gesture_types (self):
		self.gesture_types = os.listdir (self.data_dir)
		if '.DS_Store' in self.gesture_types:
			self.gesture_types.remove ('.DS_Store')


	# Function: get_gesture_dirs
	# --------------------------
	# fills self.gesture_dirs s.t. each gesture_type maps to it's own directory.
	# call after 'self.get_gesture_types ()'
	def get_gesture_dirs (self):

		self.gesture_dirs = {gesture_type:os.path.join(self.data_dir, gesture_type) for gesture_type in self.gesture_types}


	# Function: make_gesture_dir
	# --------------------------
	# given a gesture name, this will create a data directory for it
	# and add it to self.gesture_dirs.
	def make_gesture_dir (self, gesture_type):

		### --- make a data directory if it doesn't exist already --- ###
		if not gesture_type in self.gesture_dirs.keys ():
			gesture_dir = os.path.join(self.data_dir, gesture_type)
			os.mkdir (gesture_dir)
			self.gesture_dirs[gesture_type] = gesture_dir

		### --- do nothing otherwise --- ###
		else:
			pass


	# Function: get_save_filename
	# ---------------------------
	# given a gesture name, this will return the path of where to save it
	def get_save_filename (self, gesture_type):

		### Step 1: get the gesture_dir (does nothing when appropriate) ###
		self.make_gesture_dir (gesture_type)
		gesture_dir = self.gesture_dirs[gesture_type]

		### Step 2: make the filename - current # of examples + 1 ###
		all_recorded_gestures = os.listdir (gesture_dir)
		next_index = len(all_recorded_gestures) + 1
		filename = os.path.join (gesture_dir, str(next_index) + '.gesture')

		return filename









	########################################################################################################################
	##############################[ --- Loading/Saving Gestures --- ]#######################################################
	########################################################################################################################

	# Function: save_gesture 
	# ----------------------
	# pickles a given gesture
	def save_gesture (self, gesture):

		### Step 1: save the gesture ###
		save_filename = self.get_save_filename (gesture.name)
		gesture.pickle_self (save_filename)
		print_status ("Gesture Recognizer", "Saved recorded gesture at " + save_filename)
		print gesture.O


	# Function: load_gestures_of_type
	# -------------------------------
	# given a filepath and a gesture type, this will load all the gestures from it
	# into self.gestures
	def load_gestures_of_type (self, gesture_type):

		### Step 1: initialize list of gestures of this type ###
		self.gestures[gesture_type] = []

		### Step 2: get all filenames from the appropriate gesture_dir ###
		gesture_filenames = [os.path.join (self.gesture_dirs[gesture_type], g) for g in os.listdir (self.gesture_dirs[gesture_type])]

		### Step 3: for each filename, load in a gesture from it and add to list ###
		for gesture_filename in gesture_filenames:

			### --- create the gesture --- ###
			new_gesture = Gesture (name=gesture_type, observations_filepath=gesture_filename)

			### --- make sure it is full/clean --- ###
			if not new_gesture.is_full ():
				print_error ("Loading Gestures", "Encountered a gesture that is not yet full")

			### --- add to the list of gestures --- ###
			self.gestures[gesture_type].append (new_gesture)


	# Function: load_gestures
	# -----------------------
	# loads in training examples from the data directory
	# fills self.gestures in entirety
	def load_gestures (self):

		### Step 1: initialize self.gestures ###
		self.gestures = {}

		### Step 2: get all gesture types ###
		self.get_gesture_types ()

		### Step 3: get all gesture dirs ###
		self.get_gesture_dirs () 

		### Step 4: for each gesture_type, load in all gestures ###
		for gesture_type in self.gesture_types:
			print_inner_status ("Gesture Recognizer (load_gestures)", "Loading gestures of type " + str(gesture_type))
			self.load_gestures_of_type (gesture_type)


	# Function: print_data_stats
	# --------------------------
	# prints information on the loaded training examples
	def print_gestures_stats (self):

		print_message ("Counts of 'Gesture' objects by type: ")
		for key, value in self.gestures.items ():
			print "	- ", key, ": ", len(value)









	########################################################################################################################
	##############################[ --- Getting HMMs --- ]##################################################################
	########################################################################################################################

	# Function: get_hmms
	# ------------------
	# for each gesture_type, this will train an hmm
	def get_hmms (self):

		for gesture_type in self.gesture_types:

			print_status ("Get_Hmms", "Fitting for gesture_type: " + gesture_type)
			### Step 1: fill hmm_examples appropriately ###
			hmm_examples = []
			for gesture in self.gestures[gesture_type]:
				hmm_rep = gesture.get_hmm_rep ()
				hmm_examples.append (hmm_rep)

			### Step 2: fit parameters for the hmm ###
			hmm = GaussianHMM (self.num_hmm_states)
			hmm.fit (hmm_examples)

			### Step 3: store the hmm in self.hmms ###
			self.hmms[gesture_type] = hmm

			print_inner_status (gesture_type, "predicted the following sequences: (score: sequence)")
			for example in hmm_examples:
				print "		", hmm.score (example), ": ", hmm.predict (example)









	########################################################################################################################
	##############################[ --- Getting Testing/Training Examples --- ]#############################################
	########################################################################################################################

	# Function: get_classifiable_rep
	# ------------------------------
	# given a Gesture object, this will produce (and return) a feature-vector 
	# representation that can be passed to a LR classifier for training/classification
	def get_classifiable_rep (self, gesture):

		classifiable_rep = []

		hmm_rep = gesture.get_hmm_rep ()
		for gesture_type, hmm in self.hmms.items ():

			hmm_score 		= hmm.score 	(hmm_rep)
			hmm_sequence 	= hmm.predict 	(hmm_rep)

			### --- Note: for now, just go with scores? --- ###
			classifiable_rep.append (hmm_score)

		return classifiable_rep


	# Function: get_all_examples
	# --------------------------
	# converts self.gestures -> self.all_examples
	def get_all_examples (self):

		### Step 1: intialize self.all_examples ###
		self.all_examples = []

		### Step 2: for each gesture type, convert to appropriate format and add to list ###
		for gesture_type, gestures in self.gestures.items ():
			for gesture in gestures:

				classifiable_rep = self.get_classifiable_rep (gesture)
				self.all_examples.append ((classifiable_rep, gesture_type))

		random.shuffle(self.all_examples)


 	# Function: split_training_testing_examples
 	# -----------------------------------------
 	# splits self.all_examples into self.training_examples and self.testing_examples
 	def split_training_testing_examples (self):

 		num_training_examples = int(self.training_examples_proportion * len(self.all_examples))
 		self.training_examples = self.all_examples[:num_training_examples]
 		self.testing_examples = self.all_examples[num_training_examples:]
 		self.print_examples_stats ()

 	# Function: print_examples_stats
 	# ------------------------------
 	# prints stats on training/testing examples
 	def print_examples_stats (self):
 		
 		print "	- Training: ", len(self.training_examples)
 		print "	- Testing: ", len(self.testing_examples)
 		print "	- Total: ", len(self.all_examples)






	########################################################################################################################
	##############################[ --- Training/Evaluating Classifier --- ]##################################################
	########################################################################################################################

	# # Function: get_num_changes
	# # -------------------------
	# # number of sequence changes...
	# def get_num_changes (self, sequence):
	# 	cur = -1
	# 	num_changes = 0
	# 	for entry in sequence:
	# 		if entry != cur:
	# 			num_changes += 1
	# 		cur = entry
	# 	return num_changes


	# # Function: get_average_length
	# # ----------------------------
	# # average number of states
	# def get_state_lengths (self, sequence):
	# 	length = []
	# 	for i in range(10):
	# 		length.append (0)
	# 	for entry in sequence:
	# 		length[entry] += 1

	# 	return length



	# Function: train_classifier
	# --------------------------
	# Trains the classifier and saves it
	def train_classifier (self):

		X = [ex[0] for ex in self.training_examples]
		y = [ex[1] for ex in self.training_examples]
		self.classifier.fit (X, y)


	# Function: evaluate_classifier 
	# -----------------------------
	# evaluates current classifier on test_data
	def evaluate_classifier (self):

		print_message ("Evaluating classifier on test data")
		total_score = 0.0

		for ex in self.testing_examples:

			features = ex[0]
			true_label = ex[1]
			prediction 			= self.classifier.predict (features)[0]
			prediction_probs 	= self.classifier.predict_proba (features)[0]

			classes = list(self.classifier.classes_)
			index = classes.index (prediction)
			prediction_prob = prediction_probs [index]
			total_score += prediction_prob
			if prediction_prob < 0.9:
				print "Exception: true_label = ", true_label
				for i, c_i in enumerate(classes):
					c_i_score = prediction_probs[i]
					print "	", c_i, ": ", prediction_probs[i]

		avg_score = total_score / float(len(self.testing_examples))
		print "average score: ", avg_score


	# Function: load_model
	# --------------------
	# loads the model from a pickled file
	def load_model (self):

		self.classifier 	= pickle.load (open(self.classifier_filename, 'r'))
		self.hmms 			= pickle.load (open(self.hmms_filename, 'r'))


	# Function: save_model
	# --------------------
	# loads the model from a pickled file
	def save_model (self):

		pickle.dump (self.classifier, open(self.classifier_filename, 'w'))
		pickle.dump (self.hmms, open(self.hmms_filename, 'w'))







	########################################################################################################################
	##############################[ --- Using Classifier --- ]##############################################################
	########################################################################################################################

	# Function: classify_gesture
	# --------------------------
	# given a Gesture object, this will return the sorted scores from our classifier
	def classify_gesture (self, gesture):

		### Step 1: get feature_representation ###
		#--- gesture being passed in is consistently different ---#
		classifiable_rep = self.get_classifiable_rep (gesture)


		### Step 2: have the classifier make predictions ###
		prediction = self.classifier.predict (classifiable_rep)[0]
		prediction_probs = self.classifier.predict_proba (classifiable_rep)[0]

		### Step 3: sort the probability scores ###
		classes = list(self.classifier.classes_)
		index = classes.index (prediction)
		prediction_prob = prediction_probs [index]
		# print_message ("Best Match: " + str(prediction) + " | Probability: " + str(prediction_prob))
		# for i, c_i in enumerate(classes):
			# print ' -', c_i, ': ', prediction_probs[i]

		if prediction_prob > self.prediction_prob_threshold:
			return (prediction, prediction_prob)









if __name__ == "__main__":

	print_message ("##### Gesture Recognizer - Train and Evaluate #####")

	gr = Gesture_Recognizer ()

	### Step 1: load in all the gestures ###
	print_message ("Loading gestures")
	gr.load_gestures ()
	gr.print_gestures_stats ()

	### Step 2: train the HMMs ###
	print_message ("Getting hmms")
	gr.get_hmms ()

	### Step 3: get examples ###
	print_message ("Getting examples for training/testing")
	gr.get_all_examples ()
	gr.split_training_testing_examples ()

	### Step 4: train the classifier and save the entire model ###
	gr.train_classifier ()
	gr.save_model ()

	### Step 5: evaluate the classifier ###
	gr.evaluate_classifier ()





















