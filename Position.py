# *------------------------------------------------------------ *
# * Class: Position
# * --------------
# * class to represent a single position (frame)
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
from common_utilities import print_message, print_status

#--- Numpy ---
import numpy as np


class Position:

	#--- Data/Representations ---
	features 	= None	#numpy array describing the hand's position in this frame


	# Function: Constructor
	# ---------------------
	# fills in self.features appropriately
	def __init__ (self, this_frame, d1_frame, d2_frame):

		self.compute_features (this_frame, d1_frame, d2_frame)


	########################################################################################################################
	########################################[ --- Computing Features --- ]################################################################################
	########################################################################################################################		

	# Function: compute_positional_features
	# -------------------------------------
	# computes and returns a list of features representing the 
	# position of the passed frame.
	# Consists of:
	# - Palm location coordinates (x, y, z)
	# - Palm orientation coordinates (yaw, pitch, roll)
	def compute_positional_features (self, frame):

		positional_features = []

		### --- without hands, return all 5000s --- ###
		if len(frame.hands) == 0:
			positional_features = [float(5000)] * 6

		### --- otherwise ... ---###
		else:

			hand = frame.hands[0]
			positional_features = []

			#--- Position ---
			position = hand.palm_position
			positional_features.append (float(position[0]))
			positional_features.append (float(position[1]))
			positional_features.append (float(position[2]))

			#--- Yaw/Pitch/Roll ---
			direction = hand.direction 
			normal = hand.palm_normal	
			positional_features.append (float(direction.yaw))
			positional_features.append (float(direction.pitch))
			positional_features.append (float(normal.roll))

		return positional_features


	# Function: compute_velocity_features
	# -----------------------------
	# computes and returns a list of features representing the
	# velocity of the passed positional vector, pos_0, w/r/t
	# pos_1 and pos_2.
	# Consists of:
	# - Velocity over time interval d1 and d2 		(x, y, z)
	# - Acceleration over time interval d1 and d2 	(x, y, z)	
	# - Velocity over time interval d1 and d2 		(yaw, pitch roll)
	# - Acceleration over time interval d1 and d2 	(yaw, pitch, roll)
	def compute_velocity_features (self, pos_0, pos_1, pos_2):

		velocity_features = []

		#--- d1 velocity ---
		for (c0, c1) in zip (pos_0, pos_1):
			velocity_features.append (float(c0 - c1))

		#--- d2 velocity ---
		for (c0, c2) in zip (pos_0, pos_2):
			velocity_features.append (float(c0 - c2))

		#--- pseudo-acceleration ---
		for (c0, c1, c2) in zip (pos_0, pos_1, pos_2):
			prev_vel = (c1 - c2)
			cur_vel = (c0 - c1)
			velocity_features.append (float(cur_vel - prev_vel))

		return velocity_features



	# Funtion: compute_features
	# -------------------------
	# computes features for the current frame
	def compute_features (self, this_frame, d1_frame, d2_frame):
		
		### Step 1: empty features if no hands are found ###
		if len(this_frame.hands) == 0:
			self.features = None
			return

		### Step 2: get positional features for all of them ###
		this_positional_features 	= self.compute_positional_features (this_frame)
		d1_positional_features 		= self.compute_positional_features (d1_frame) 
		d2_positional_features 		= self.compute_positional_features (d2_frame) 		

		### Step 3: get velocity-related features ###
		velocity_features = self.compute_velocity_features (this_positional_features, d1_positional_features, d2_positional_features)

		### Step 4: combine them and set appropriately ###
		self.features = np.array(this_positional_features + velocity_features)


