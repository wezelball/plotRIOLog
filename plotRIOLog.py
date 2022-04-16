#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plotRIOLog.py

Retrieves, saves, and plots the RIO log file
"""


# Matplotlib
import matplotlib.pyplot as plt
import csv

# need a file dialog
import tkinter as tk
from tkinter import filedialog

# for time stamping files
from datetime import datetime

# For remote connection to RIO
from subprocess import call

import sys
import getopt

# Globals
load_file = False

def usage():
   print("Don't be a dummy, dummy!")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'lf:h', ['load', 'file=', 'help'])
except getopt.GetoptError:
   usage()
   sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-l', '--load'):
        load_file = True
    elif opt in ('-f', '--file'):
        file = arg
    else:
        load_file = False # User wants to connect to RIO


# A file was specified on the command line
if load_file:
   root = tk.Tk()
   root.withdraw()
   dest_file_path = filedialog.askopenfilename()
# Getting the Logging.txt file from the RIO instead
else: 
   file = "Logging.txt"
   dest_path = "/home/dcohen/tmp/"
   #dest_path = "/home/dcohen/Dropbox/Public/frc/programming_2022/data/"
   now = datetime.now()
   timestamp = now.strftime("_%Y%m%d_%H%M%S")
   dest_file_path = dest_path + file[:7] + timestamp + file[-4:]
   # Get the Log file
   try:
      cmd = "scp lvuser@10.3.84.2:" + file + " " +  dest_file_path
      call(cmd.split(" "))
   except:
      print("Unable to connet to RIO")
      sys.exit(2)

# Set up lists
setpoint = []
error = []
output = []
feedback = []
xaxis = []    # change this to read timestamp
loop = 0

with open(dest_file_path,'r') as csvfile:
   data = csv.reader(csvfile, delimiter=' ')
   for row in data:

      if 'SP:' in row:
         SP = row[-1]
         setpoint.append(float(SP))
         xaxis.append(loop)
         loop += 1
              
      if 'err:' in row:
         err = row[-1]
         error.append(float(err))

      if 'CV:' in row:
         CV = row[-1]
         output.append(float(CV))
    
      if 'fbk:' in row:
         fbk = row[-1]
         feedback.append(float(fbk))
        
# Plot it
plt.plot(xaxis, setpoint, feedback)
plt.show()
