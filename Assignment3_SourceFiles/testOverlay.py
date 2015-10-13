#!/usr/bin/python 

###
# Distributed Systems Project Assignment 3clear
# Chris Blythe - 14258961
# Farbod Faghihi Berenjegani - 014343410
# Mohammad Bakharzy - 014083589
###

# Test overlay network

#usage: python testOverlay.py (str config.txt, int numberOfMessages)

#Sends required number of messages to randomised nodes with randomised target addresses


import sys
import socket
import pickle
import threading
from collections import deque
import random
import time

print "TEST"

def test( source, target ):

	msgHost = 'localhost'
	msgPort = 10000 + source
	msg = [source, 0, target]
	print msg, " ", msgPort

def send( source, target ):

#	for i in range(0,len(nodeList)):
#		if(nodeList[i].split(' ')[0] == source):
#			msgHost = nodeList[i].split(' ')[1]
	if(source < 256):
		msgHost = "ukko049.hpc.cs.helsinki.fi"
	if(255 < source < 512):
		msgHost = "ukko050.hpc.cs.helsinki.fi"
	if(511 < source < 768):
		msgHost = "ukko026.hpc.cs.helsinki.fi"
	if(767 < source < 1024):
		msgHost = "ukko052.hpc.cs.helsinki.fi"
	msgPort = 10000 + source
	msg = [source, 0, target]
	print msgHost, " ", msgPort
	try:					#catches error if server not available
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((msgHost, msgPort))
		
		
		#Pickle message to send over socket
		pickledMessage = pickle.dumps(msg)		# Pickle message
		s.send(pickledMessage)					# Send message
		data = s.recv(1024)						# Receive response - not used
		messageClock = None
		s.close()								# Close socket
		global sendCount
		sendCount += 1

	except: 
		print 'SERVER NOT AVAILABLE'
		pass

########### Initialisation ###########
fp = open(sys.argv[1])
#open config file from argument 1, split lines into list and remove line breaks
nodeList = [line.rstrip('\n') for line in fp]
fp.close()

messageCount = int(sys.argv[2])

#clear hopcount log file before test
open('testing/hopcount.log', 'w').close()
open('testing/hopcount1.log', 'w').close()
open('testing/hopcount2.log', 'w').close()
open('testing/hopcount3.log', 'w').close()
open('testing/hopcount4.log', 'w').close()
#record total number of nodes
numberOfNodes = len(nodeList)

for index, line in enumerate(nodeList):
      print line	


timer = 0
sendCount = 0

while timer < messageCount:

	rndSource = 0
	rndTarget = 0
	
	while rndSource == rndTarget:
		rndSource = random.randint(0,numberOfNodes-1)
		rndTarget = random.randint(0,numberOfNodes-1)
		
	#rndSource = random.randint(0,numberOfNodes-1)
	#rndTarget = random.randint(0,numberOfNodes-1)
	
	print rndSource, rndTarget
	
	send(rndSource, rndTarget)
	time.sleep(0.0001)
	timer += 1
	
	



print "Sent count", sendCount



















