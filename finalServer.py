#!/usr/bin/env python3

# --------
# LIB
# ------

from datetime import date
import csv
import socket

# ---------
# CONSTANTS
# --------

# system date used for logging in DD/MM/YYYY
date = (date.today()).strftime("%d/%m/%y")

# --------
# FUNCTIONS
# --------

# function to log values from client
def writeData(y):
        # opens find in append mode
        with open('log.csv', 'a') as logFile:
                # sets up delimeters as its a csv
                logWriter = csv.writer(logFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #writes row with y value used
                logWriter.writerow([y, date])

# -------
# MAIN
# ------

# keeps connection open indefinitely
while True:

        # host and port numbers
        # '.x.x' is replaced with server IP
        HOST = '192.168.x.x' #.. could also use 127.0.0.1
        PORT = 65420

        # code sampled from realPython reference, slightly edited
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT)) # binds to port (e.g. keeps own port open)
                s.listen() # listens in for connections
                conn, addr = s.accept()

                # when theres a connection:
                with conn:
                        print("Connection!")
                        while True:
                                data = conn.recv(1024) # data received from client
                                if not data:
                                        break
                                print("Logged value at", date) # prints the value and system date

                                # decodes data before writing to file
                                writeData(data.decode('utf-8'))
                                # sends data back to server
                                conn.sendall(data)