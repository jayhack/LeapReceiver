# *------------------------------------------------------------ *
# * Class: Gesture
# * --------------
# * class to represent a single gesture (as a list of poses)
# *  
# *------------------------------------------------------------ *
#--- Standard ---
import os
import sys
import pickle

#--- Leap ---

### NOTE: change the path below to the location of your local installation ###
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_message, print_error, print_status
from Position import Position

#--- Numpy ---
import numpy as np



# Class: Gesture
# --------------
# respresents a list of frames that can be classified as gestures
class Gesture:

	name 					= '__UNCLASSIFIED__'	# Name of this gesture

	#--- Data ---
	frames 		= []			# list of Leap 'Frame' objects constituting this gesture
	O 			= []			# "Observations": list of vector-representations constituting this gesture
	hmm_rep 	= []			# can be passed to an hmm

	#--- Parameters ---
	gesture_length 			= 40		# number of frames stored in the gesture
	frame_reduction_const 	= 5			# gesture_length/frame_reduction_const = # of frames in final feature rep
	d1_length 				= 5			# small derivative of motion
	d2_length 				= 10		# large derivative of motion



	# Function: Constructor
	# ---------------------
	# initializes an empty frame
	def __init__ (self, name='__UNCLASSIFIED__', observations_filepath=None):

		### Step 1: set/initialize data and parameters ###
		self.name 					= name
		self.frames 				= []
		self.O 						= []


		### Step 2: load the observations in, if appropriate ###
		if observations_filepath:
			self.load_observations(observations_filepath)






	########################################################################################################################
	########################################[ --- Getting Stats on Gesture  --- ]###########################################
	########################################################################################################################

	# Function: is_full
	# -----------------
	# returns wether the gesture is full or not
	def is_full (self):

		return (len(self.O) >= self.gesture_length)


	# Function: get_hmm_rep
	# -------------------------
	# returns a feature-vector representation of the gesture.
	# this will be applied 
	def get_hmm_rep (self):
			
		self.hmm_rep = []
		### Step 1: add all frames appropriate for frame-reduction const ###
		for i, O_i in enumerate(self.O):
			if i % self.frame_reduction_const == 0:
				self.hmm_rep.append (np.array(O_i))
			
		### Step 2: add the very last frame ###
		self.hmm_rep.append (np.array(self.O[-1]))

		### Step 3: convert to numpy array and return ###
		self.hmm_rep = np.array (self.hmm_rep)
		return self.hmm_rep







	########################################################################################################################
	########################################[ --- Adding Frames  --- ]######################################################
	########################################################################################################################		

	# Function: pop_oldest_frame
	# --------------------------
	# pops off the oldest frame contained in this gesture
	def pop_oldest_frame (self):

		self.O.pop(0)
		self.frames.pop (0)

	# Function: get_prev_frames
	# -------------------------
	# gets the frames to use for first/second derivative features.
	def get_prev_frames (self):

		### Step 1: get the newest frame ###
		newest_frame = self.frames[-1]

		### Step 2: set d1_frame, d2_frame as frame if insuffucient 
		d1_frame = newest_frame
		d2_frame = newest_frame
		if len (self.O) > self.d1_length:
			d1_frame = self.frames[-self.d1_length]
		if len(self.O) > self.d2_length:
			d2_frame = self.frames[-self.d2_length]

		return (d1_frame, d2_frame)


	# Function: add_frame 
	# -------------------
	# takes in a Leap frame object and adds to the current gesture;
	# removes excessive frames if necessary
	# Note: should probably have a mechanism that clears the gesture if the hand disappears?
	def add_frame (self, frame):

		### Step 1: add to list of 'Frame' objects (self.frames) ###
		self.frames.append (frame)

		### Step 2: add to the list of observations (self.O) ###
		(d1_frame, d2_frame) = self.get_prev_frames ()
		position = Position (frame, d1_frame, d2_frame)
		self.O.append (position.features)


		### Step 3: if the hand was missing, reset the gesture (only consider sequences where we see the hand) ###
		if position.features == None:
			self.clear ()
			return


		### Step 5: remove frames if necessary ###
		if len(self.O) > self.gesture_length:
			self.pop_oldest_frame ()


	# Function: clear
	# ---------------
	# clears the gesture. should be called after a classification goes through
	def clear (self):

		self.frames = []
		self.O = []










	########################################################################################################################
	########################################[ --- Loading/Saving --- ]######################################################
	########################################################################################################################		


	# Function: pickle_self
	# ---------------------
	# saves all data from this gesture
	def pickle_self (self, save_filepath):

		save_file = open(save_filepath, 'w')
		pickle.dump (self.O, save_file)
		save_file.close ()


	# Function: load_observations
	# ---------------------------
	# loads in observations describing this gesture
	def load_observations (self, observations_filepath):

		open_file = open (observations_filepath, 'r')
		self.O = pickle.load (open_file)
		open_file.close ()











