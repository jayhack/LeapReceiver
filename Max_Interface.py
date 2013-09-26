#!/usr/bin/python
# *------------------------------------------------------------ *
# * Class: Max_Interface
# * ---------------------
# * contains everything needed to interface with max.
# *
# *  
# *------------------------------------------------------------ *
#--- Standard ---
import string

#--- UDP ---
from socket import *

#--- JSON ---
import json

#--- My Files ---
from common_utilities import print_message, print_error, print_status, print_inner_status

class Max_Interface:

	#--- Interface/Protocol Parameters ---
	host = 'localhost'
	port = 7401
	butf = 1024
	addr = (host, port)

	#--- Objects for Communication ---
	UDPSock = None


	########################################################################################################################
	########################################[ --- Constructor/Destructor --- ] #############################################
	########################################################################################################################		


	# Function: Constructor
	# ---------------------
	# binds to the correct port, initializes 'available_gestures'
	def __init__ (self):

		### Step 1: create socket ###
		self.UDPSock = socket (AF_INET, SOCK_DGRAM)

	# Function: Destructor 
	# --------------------
	# closes self.UDPSock
	def __del__ (self):
		
		self.UDPSock.close ()





	########################################################################################################################
	########################################[ --- Sending Messages --- ] ###################################################
	########################################################################################################################		


	# Function: send_gesture
	# ----------------------
	# sends a message to max denoting the occurence of a gesture
	# Format: "Gesture [Gesture Type]"
	def send_gesture (self, gesture_type):

		gesture_message = "Gesture " + str(gesture_type)
		self.send_message (gesture_message)


	# Function: send_hand_state
	# -------------------------
	# sends a message to max denoting the current state of the hand
	# Format: "Hand_State [(palm coordinates) x, y, z] [(palm orientation) yaw, pitch, roll] [number of fingers]"
	def send_hand_state (self, hand):

		#--- Initialize Dict ---
		hand_state_dict = {}

		#--- Send Palm Coords ---
		palm_position = (hand.palm_position[0], hand.palm_position[1], hand.palm_position[2])
		palm_position_message = "Palm_Position " + " ".join([str(coord) for coord in palm_position])
		self.send_message (palm_position_message)

		#--- Send Palm Orientation ---
		palm_orientation = (hand.palm_normal[0], hand.palm_normal[1], hand.palm_normal[2])
		palm_orientation_message = "Palm_Orientation " + " ".join([str(coord) for coord in palm_orientation])
		self.send_message (palm_orientation_message)

		#--- Send Number of Fingers ---
		num_fingers = len(hand.fingers)
		num_fingers_message = "Num_Fingers " + str(num_fingers)
		self.send_message (num_fingers_message)




	# Function: send_message
	# ----------------------
	# given a python dict, this will send a max-readable format of it.
	def send_message (self, message):

		if not self.UDPSock.sendto(message, self.addr):
			print_error ("Max Interface", "Failed to send gesture" + str(message) + " to Max")



if __name__ == '__main__':

	max_interface = Max_Interface ()

	max_interface.send_gesture ("Start")
	max_interface.send_gesture ("Swirl")
	max_interface.send_hand_state ("Test")
	# max_interface.send_message ("Palm_Position 1 2 3")
	max_interface.send_gesture ("Stop")

