#!/usr/bin/env python3

# --------
# LIB
# --------

import socket
import adafruit_hcsr04
import board
import time


# ----------
# SONAR VALUES
# ----------
# threshold is defaulted at 10cm
threshold = 10

# code from Adafruit library for HCSR04 ultrasonic sensor
# sonar = sensor, defines the echo and trigger pins on the GPIOs
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

# rounds to 2 decimal points
value = round((sonar.distance), 2)

# -----------
# FUNCS
# ----------

# intro screen
def intro():
        print("\nWelcome to your hand sanitizer monitor interface!\n")
        print("What would you like to do?")

# lets user change measurement
def changeMes():
        print("\nUpdate your measurements for your sanitizer")
        print("Currently set at:", threshold, "cm") # prints current threshold
        # gets new threshold from user (integer)
        newThres = int(input("\nPlease enter how low your sanitizer should be before we send a signal (in cm!): "))
        # prints new measurement
        print("Your measurement is now set at:", newThres)
        # returns value to be set as new threshold
        return newThres


# setting into monitor mode
def checker():
        # while loop keeps getting values from sensor
        while True:
                value = round((sonar.distance), 2)

                # code example worked off Adafruit example
                try:
                        print(value) # prints measurement to screen

                        # if value is above the threshold: prints warning, encodes + sends
                        if value >= threshold:
                                print("!!Warning!! Value has hit threshold")
                                value = str(value) # changes int to string
                                message = value.encode() # encodes to bits (can only send bits over sockets)
                                sendAll(message) # starts function to send

                # runtime error if measurements out of range
                except RuntimeError:
                        print("Issues with sensor; retrying....")
                #time between measurements
                time.sleep(10)

# function to connect and send to server (within checker() )
def sendAll(x):
        HOST = '192.168.x.x' # insert server IP at ".x.x"
        PORT = 65420 # server port

        # sample from realPython basic socket communication
        # altered slightly
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT)) # connects to host
                s.sendall(x) # sends value
                data = s.recv(1024)
        print('Sent low value:', value, ' to server at', HOST) # prints to screen

# ----
# MAIN
# ----

intro() # starts intro

# while true loop keeps bringing user back to menu
while True:

        # main menu:
        print("\n ================================================")
        print(" | 1. Change the threshold for the sensor  \t|" )
        print(" | 2. Set the interface into monitor mode \t|")
        print(" | 3. ....exit \t\t\t\t\t|")
        print(" ================================================\n")

        #allows for user selection
        option = int(input("Selection: "))

        # sends user into the change measurement function
        if option == 1:
                threshold = changeMes() # sets the new value permantly until program restarts

        # sends user into monitor mode
        elif option == 2:
                print("This will now monitor the hand sanitizer.")
                print("\nYou won't be able to change any thresholds/measurements at this time.")
                conf = input("Are you sure? (y/n): ")

                # if user confirms, checker function begins
                if conf == "y":
                        print("\nSetting up monitor mode... Threshold is set at:", threshold)
                        checker()
                # any wrong keys or 'n' sends back to menu
                else:
                        pass
        #user prompted exit on option 3
        elif option == 3:
                print("Thank you!")
                exit() # system exit