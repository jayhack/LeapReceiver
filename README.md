-----------------------------------------------------
PrimeSenseReceiver
------------------
Python utility for making hand pose data from the Leap
Motion Available throughout your system via UDP ports
by Jay Hack, Fall 2013
-----------------------------------------------------

1: Contact Info
===============
Email: jhack@stanford.edu
Github: https://github.com/jayhack
Hit me up on FB with any questions. I should be pretty easy to find if you are on the Stanford network.


2: Overview
===========
• This is a python script and accompanying Max MSP patch that I developed during the "Science of Sound" Arts Intensive, summer 2013, taught by Jay Kadis and Sasha Leitman
• It enables one to:
	- train/recognize custom gestures using the leap motion (See: "Record/Train" mode)
	- send gesture occurences and hand position paramters to a max patch
• This is good because:
	- the Leap is inexpensive
	- the Leap is conducive to creating natural interaction-oriented musical experiences.
	- Max MSP is also conducive to creating said experiences. (It is not, however, inexpensive.)
• I originally developed this for a gesture-activated beat machine.
	- certain gestures map to playing samples
	- others map to starting/stopping tracks
	- L/R balance of tracks can be controlled via "drag and drop" above the leap.
	- check it out on my github account
	- It was a great learning project and I encourage others to do vamp on this idea. It looks very cool.


3: Installation
===============
• In order to get this running, you will need all of the following:
	- A Leap sensor
	- python 2.7 or later. (Pre-installed on Mac OSX)
	- scikit-learn and all dependencies: http://scikit-learn.org/stable/install.html
		- make sure this is installed correclty by doing the following in your python environment
			>>> import sklearn
			>>> print sklearn.__version__
	- Leap drivers: https://www.leapmotion.com/setup
	- Leap SDK: (sign up and download) https://www.leapmotion.com/developers 
• You will need to change the path added to sys.path (near the top of the file) to point to your local installation of the Leap SDK in the following files:
	- Synth_Listener.py
	- run.py
	- Position.py
	- Gesture.py
• You will need to change the path added to sys.path (near the top of the file) to point to your local installation of scipy in the following files:
	- Gesture_Recognizer
• Make the program easily executable:
	- to figure out where your installation of python is, type the following command in terminal: which python
	- put the result of this next to the "hashbang" (e.g. in the original files #!/usr/bin/python) at the top of 'run.py'
	- run the following command in terminal: chmod +x run.py
	- you can now run the program via the following command: ./run.py



4: Making use of it
===================
• Record some examples of gestures:
	- ./run.py -> select 'Record' mode -> enter the name of the gesture you want to record for -> press enter once
	- you will see 'x's streaming down the terminal screen when it detects your hand
	- press enter with your other hand to record an instance of a gesture. ('.' will start streaming instead of 'x')
	- you will know the recording of a single gesture example is finished when a large matrix is displayed on the screen. (this is our representation of the hand)
	- by default it will record 10 examples of the gesture you entered; you can record more by entering the same gesture name (case-sensitive) again.
	- I suggest at least 30 examples for each gesture, and record only 10 at a time of a single type of gesture in order to ensure that there is enough variance between examples s.t. it is sufficiently broad to capture all variants of the gesture.
	(if you do the exact same thing 30 times, it becomes hard to correctly classify instances of the same gesture that even slightly deviate from the form of the homogenous training examples.)
• Train the classifier:
	- ./run.py -> select 'Train' mode -> chill for ~10 seconds
	- your classifier is now trained.
• Use it:
	- ./run.py -> select 'Synth' mode -> perform gestures at will.
	- you will need to have the terminal in the *foreground* during program operation if you want it to recognize gestures.


Enjoy!
- Jay Hack, Class of 2015



