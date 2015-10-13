#!/usr/bin/python 

###
# Distributed Systems Project Assignment 3clear
# Chris Blythe - 14258961
# Farbod Faghihi Berenjegani - 014343410
# Mohammad Bakharzy - 014083589
###

import sys

#Generate config file of node lists
# Arguments configGenerator.py (int nodeCount)

#format: NodeID Host Port
#port = 10000 + nodeID

#hostAddress = 'localhost'

nodeCount = int(sys.argv[1])
index = 0

configFile = open('config.txt', 'w')

while index < nodeCount:
	if(index < 256):
		line = str(index) + ' ' + "ukko049.hpc.cs.helsinki.fi" + ' ' +str(10000 + index) + '\n'
	if(index < 512 and 255 < index):
		line = str(index) + ' ' + "ukko050.hpc.cs.helsinki.fi" + ' ' + str(10000 + index) + '\n'
	if(index < 768 and 511 < index):
		line = str(index) + ' ' + "ukko026.hpc.cs.helsinki.fi" + ' ' + str(10000 + index) + '\n'
	if(index < 1024 and 767 < index):
		line = str(index) + ' ' + "ukko052.hpc.cs.helsinki.fi" + ' ' + str(10000 + index) + '\n'
	configFile.write(line)
	print line
	index += 1
	
configFile.close()
