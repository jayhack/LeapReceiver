# *------------------------------------------------------------ *
# * Class: Synth_Listener
# * --------------------------
# * Main class for this application; does all of the following:
# *     - receives frames from the leap
# *     - discerns gestures via Leap_Gesture object
# *     - sends gesture events to Max via Max_Interface object
# *------------------------------------------------------------ *
#--- Standard ---
import sys

#--- Leap ---
### NOTE: change the path below to the location of your local installation ###
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

#--- My Files ---
from common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status



class Synth_Listener(Leap.Listener):

    #--- Recent Frames ---
    most_recent_frame = None
    new_frame_available = False


    # Function: Constructor
    # ---------------------
    # creates max_interface and leap_gesture
    def on_init(self, controller):

        ### Step 2: notify of initialization ###
        print_status ("Synth Listener", "controller initialized")




    ########################################################################################################################
    ##############################[ --- Initialization/Finalization --- ]###################################################
    ########################################################################################################################        


    # Function: on_connect
    # --------------------
    # callback function for when the controller is connected
    def on_connect(self, controller):

        print_status ("Synth Listener", "controller connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);



    # Function: on_disconnect
    # -----------------------
    # callback function for when the controller is disconnected
    def on_disconnect(self, controller):

        print_status ("Synth Listener", "Controller disconnected")

    # Function: on_exit
    # -----------------
    # callback function for exit of the program
    def on_exit(self, controller):
 
        print_status ("Synth Listener", "Exiting")














    ########################################################################################################################
    ##############################[ --- Frame Processing --- ]##############################################################
    ########################################################################################################################        

    # Function: print_frame
    # ---------------------
    # prints a user-readable format of the current frame
    def print_frame (self, frame):

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
                print "Hand has %d fingers, average finger tip position: %s" % (
                      len(fingers), avg_pos)

            # Get the hand's sphere radius and palm position
            print "Hand sphere radius: %f mm, palm position: %s" % (
                  hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # # Gestures
            # for gesture in frame.gestures():
            #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
            #         circle = CircleGesture(gesture)

            #         # Determine clock direction using the angle between the pointable and the circle normal
            #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
            #             clockwiseness = "clockwise"
            #         else:
            #             clockwiseness = "counterclockwise"

            #         # Calculate the angle swept since the last frame
            #         swept_angle = 0
            #         if circle.state != Leap.Gesture.STATE_START:
            #             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
            #             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

            #         print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            #     if gesture.type == Leap.Gesture.TYPE_SWIPE:
            #         swipe = SwipeGesture(gesture)
            #         print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 swipe.position, swipe.direction, swipe.speed)

            #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
            #         keytap = KeyTapGesture(gesture)
            #         print "Key Tap id: %d, %s, position: %s, direction: %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 keytap.position, keytap.direction )

            #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
            #         screentap = ScreenTapGesture(gesture)
            #         print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""


    # Function: on_frame
    # ------------------
    # this function is called for every frame that is observed from the leap.
    def on_frame(self, controller):

        ### Step 1: get the frame ###
        frame = controller.frame()

        ### Step 2: update our public member data ###
        self.most_recent_frame = frame
        self.new_frame_available = True

        ### Step 3: print out info about the frame ###
        # self.print_frame (frame)


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"













