# ---------------------------------------------------------- #
# File: common_utilities.py
# ---------------------------
# random functions that are common (interface-related) 
# utilities
# ---------------------------------------------------------- #

# Function: print_welcome
# -----------------------
# prints out a welcome message
def print_welcome ():
	print "######################################################################"
	print "##############[ --- Leap Receiver for Max MSP Controller --- ]########"
	print "##############[ -   by Jay Hack, Summer 2013      - ]#################"
	print "######################################################################"
	print "\n"


# Function: print_message
# -----------------------
# prints the specified message in a salient format
def print_message (message):
	print "-" * len(message)
	print message
	print "-" * len(message)

# Function: print_error
# ---------------------
# prints an error and exits 
def print_error (top_string, bottom_string):
	print "Error: " + top_string
	print "---------------------"
	print bottom_string
	exit ()

# Function: print_status
# ----------------------
# prints out a status message 
def print_status (stage, status):	
	print "-----> " + stage + ": " + status


# Function: print_inner_status
# ----------------------------
# prints out a status message for inner programs
def print_inner_status (stage, status):
	
	print "	-----> " + stage + ": " + status







