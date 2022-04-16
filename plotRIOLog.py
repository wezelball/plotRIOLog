#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plotRIOLog.py

Retrieves, saves, and plots the RIO log file

NOte that ssh has to be setup and working - the client computer must have a 
public key that is recognized by the RIO.

(TODO: add directions on how to do that on the repository.)

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


def reformat(s):
   """ Takes the timestamp string s and properly pads the
   fractional seconds so that the plotting strftime is not fooled by
   Java stoopidness. The stoopidness is as follows:
   
   timestamp, msec      interpreted by strftime as (microseconds)
   02:07:18:5           02:07:18:500000
   02:07:18:50          02:07:18:500000
   02:07:18:500         02:07:18:500000
   
   It should be ovvious that this only the 3 decimal place timestamps
   will be properly interpreted.  So the purpose of this procedure
   is to properly pad one- or 2-digit msec timestamps to 3-digit 
   values before strftime is called.
   
   Note that there's no guarantee that H:M:S values are padded, so there
   could still be more issues.  For now, assume they are padded.
      
   """
   
   chunks = s.split(':')
   
   # Pad 
   if len(chunks[3]) == 1:
      chunks[3] = '00' + chunks[3]
   elif len(chunks[3]) == 2:
      chunks[3] = '0' + chunks[3]

   # The fractional seconds are now properly padded, just need to
   # reassemble and return
   value = chunks[0] + ':' + chunks[1] + ':' + chunks[2] + ':' + chunks[3]
   
   return value

# Parse the arguments too see what to do 
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
#time_mark_string = []
time_mark_dt_SP = []
time_mark_dt_ERR = []
time_mark_dt_CV = []
time_mark_dt_FBK = []

loop = 0

with open(dest_file_path,'r') as csvfile:
   data = csv.reader(csvfile, delimiter=' ')
   for row in data:
      # Get the time marker for this row
      a = row[0]
      time_mark_string = reformat(a[3:])

      if 'SP:' in row:
         SP = row[-1]
         setpoint.append(float(SP))
         # xaxis will be deprecated soon
         xaxis.append(loop)
         time_mark_dt_SP.append(datetime.strptime(time_mark_string, "%H:%M:%S:%f"))
         # loop will be deprecated soon
         loop += 1
              
      if 'err:' in row:
         err = row[-1]
         error.append(float(err))
         time_mark_dt_ERR.append(datetime.strptime(time_mark_string, "%H:%M:%S:%f"))

      if 'CV:' in row:
         CV = row[-1]
         output.append(float(CV))
         time_mark_dt_CV.append(datetime.strptime(time_mark_string, "%H:%M:%S:%f"))
    
      if 'fbk:' in row:
         fbk = row[-1]
         feedback.append(float(fbk))
         time_mark_dt_FBK.append(datetime.strptime(time_mark_string, "%H:%M:%S:%f"))
        

# Plot it

#plt.plot(time_mark_dt_SP, setpoint)
plt.plot(time_mark_dt_FBK, feedback)
#plt.plot(xaxis, setpoint, feedback)
plt.show()
