#!/bin/bash

###
# Distributed Systems Project Assignment 3clear
# Chris Blythe - 14258961
# Farbod Faghihi Berenjegani - 014343410
# Mohammad Bakharzy - 014083589
###

while read line
do
    name=$line
    nodeID=$(echo "$name" | cut -d' ' -f1)
	nodeAddress=$(echo "$name" | cut -d' ' -f2)
	if [ $HOSTNAME != $(echo "$nodeAddress" | cut -c1-7) ]
		then
		continue
	fi
	python overlayNode.py $1 $nodeID &
done < $1

