#!/usr/bin/python 

###
# Distributed Systems Project Assignment 3clear
# Chris Blythe - 14258961
# Farbod Faghihi Berenjegani - 014343410
# Mohammad Bakharzy - 014083589
###

import sys
import socket
import pickle
import threading
from collections import deque
import random
import time
import math 		# Importing math module for log() and pow()


########### Classes ###########

# Server thread to wait for connections and add messages to queue
class ServerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.quit = False
		
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	#allow port reuse before listener timout
		s.bind(('', port))					#bind to port from config file
		s.listen(10)						#wait for client connection
		print 'SERVER RUNNING - listening on ', port

		while not self.quit:
			try:
				conn, addr = s.accept()    		# Establish connection with client.
				data = conn.recv(1024)			# Recieve data
				msgQueue.append(pickle.loads(data))	# Unpickle packet and add to message queue
				conn.send('file received')		# Send confirmation (not used)
				conn.close()              		# Close the connection
			except:
				pass
		
		print "SERVER SHUTDOWN"
		
	def stop(self):
		self.quit = True
 
########### Functions ###########
	
#get host name from routingTable index number
def getHost( index ):
	return routingTable[index].split(' ', 2)[1]
	
#get port number from routingTable index number
def getPort( index ):
	return int(routingTable[index].split(' ', 2)[2])

#Routing Table Generation - create array of strings 'routingTable' - use clientID
	#test with configRoutingTest.txt
def routingTableGen():
	indexList = []					#list of calculated nodeID for routing table
	#for each node X, there are 10 nodes that node X has-
	# -their routing info in its routing table
	for index in range(0,int(math.log(numberOfNodes,2))):
		# The index of nodes which are saved in routing-
		# -table of each individual node is calculated below
		tempIndex = nodeID + int(math.pow(2,index))
		# In case the index which is calculated is more than number-
		# -of total nodes, then a subtract is needed to find the actual index
		if tempIndex == numberOfNodes:
			tempIndex = 0
		if tempIndex > numberOfNodes:
			tempIndex = tempIndex - numberOfNodes
			indexList.append(tempIndex)
		else:
			indexList.append(tempIndex)
	routingTableArray = []
	# nodesList is the list of lines read from config file
	for line in nodeList:
		# indexList(calculated about) has 10 IDs(indexes) of- 
		# -nodes which are supposed to be in this routing table	
		indexFromFile = int(line.split()[0])
		# Find the line from config file associated-
		# -with each ID from indexList and add to routing table
		if indexFromFile in indexList:
			routingTableArray.append(line)
	return routingTableArray
	# Example of one line of the routing table:
	# 4 ukko049.hpc.cs.helsinki.fi 10001

#Routing Agorithm - calculate next node to send message too
def routeMessage( destination ):
	#count is keeping track of the index of next hop node in the routing table
	count=0
	#ceil is the number of entries in the routing table
	ceil = int(math.log(numberOfNodes,2)-1)
	#for loop is searching to find the position of-
	#- destination between the routing table entries
	for i in range(0,ceil):
		if (destination>=int(routingTable[i].split(' ')[0]) and int(routingTable[i+1].split(' ')[0])>destination):
			return(routingTable[count]) #returning the next hop information
		else:
			if (i==(ceil-1)):
				return(routingTable[ceil]) #the destination ID is bigger than-
				#-the last entry so the next hop is the last entry
			count = count + 1
	#return node WHICH IS IN LOCAL ROUTING TABLE
	#return destination #TEMP - return inut parameter until agorithm implemented



#process and clear incoming message queue	
def processQueue():	
	# While remaining messages
	while len(msgQueue) > 0:
		#RECIEVE MESSAGE
		#count number of messages processed
		global messageCount
		messageCount += 1
		#process message
		incomingMessage = msgQueue.popleft()
		targetNode = incomingMessage[2]
		#######print "TARGET CLIENT", targetNode
		if targetNode == nodeID:		#if this node is message destination output hopcount
			#######print "MESSAGE REACHED DESTINATION"
			#log hopcount
			text = str(incomingMessage[1]) + '\n'
			hcLog.write(text)
		else:							#else increment hop count and pass message on
			incomingMessage[1] += 1		#increment hopcount
			sendMessage(incomingMessage)
		
		
		



#Send message using routing algorithm
def sendMessage( message ):
	target = message[2]
	# route message to appropriate node form routingTable based on destination node
	nextNode = routeMessage( target )
	
	msgHost = nextNode.split(' ')[1]
	msgPort = int(nextNode.split(' ')[2])
	
	try:					#catches error if server not available
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((msgHost, msgPort))
		
		
		#Pickle message to send over socket
		pickledMessage = pickle.dumps(message)	# Pickle message
		s.send(pickledMessage)					# Send message
		data = s.recv(1024)						# Receive response - not used
		messageClock = None
		s.close()								# Close socket
		#####print "SENT MESSAGE ON"

	except: 
		print 'SERVER NOT AVAILABLE'
		pass
	
	

#kill server thread	
def killServer():			
	#set quit flag to true
	server.stop()
	time.sleep(1)
	#then connect to socket to bypass accept block and process quit flag to shut down
	try:
		killSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		killSocket.connect(('localhost', port))
		killSocket.close()
	except:
		pass



########### Initialisation ###########

#open config file from argument 1, split lines into list and remove line breaks
fp = open(sys.argv[1])
nodeList = [line.rstrip('\n') for line in fp]
fp.close()


#TEMP###### - temp make routingTable = nodeList for testing
#routingTable = nodeList
#TEMP#####

#record total number of nodes
numberOfNodes = len(nodeList)

#set nodeID from argument 2
nodeID = int(sys.argv[2])

#open hopcount log file
#hcLog = open('testing/hopcount.log', 'a')
if(nodeID < 256):
	hcLog = open('testing/hopcount1.log', 'a')
if(nodeID < 512 and 255 < nodeID):
	hcLog = open('testing/hopcount2.log', 'a')
if(nodeID < 768 and 511 < nodeID):
	hcLog = open('testing/hopcount3.log', 'a')
if(nodeID < 1024 and 767 < nodeID):
	hcLog = open('testing/hopcount4.log', 'a')

#set port number using nodeID from full nodeList
port = int(nodeList[nodeID].split(' ', 2)[2])

#generate routing table
routingTable = routingTableGen()

#MISC VARIABLES
messageCount = 0	#record number of messages process by node
myClock = 0			#internal timer

#Queue to store incoming messages for processing
msgQueue = deque([])

#Start server
server = ServerThread()
server.start()
time.sleep(0.5)

########### MAIN PROGRAM LOOP ########### 

## INITIAL DELAY to allow all processes to start before running main loop
time.sleep(15)

while myClock < 30:			

	#Process any received massages from queue
	processQueue()

	#Slowdown processing slightly
	time.sleep(0.5)
	myClock += 1
	
	
print "Message count", messageCount	

## Kill server thread and exit
killServer()
#close log file
hcLog.close()


