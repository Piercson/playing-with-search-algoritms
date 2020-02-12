# Piercson Thomas
# Nov. 11th 2019
# A program to show the nodes expanded for each, Dijkstras, A*, and landmark
import math
import sys
import inspect
import heapq, random
import random

class Node:
    def __init__(self, vector = None, edges_to = None):
        self.edges_to = list()
        self.vector = []
def getNumberNodesVisited(listOfNodes):
	#checks all the entries in the list that are non infinity
	amountVistedNodes = 0
	for node in listOfNodes:
		if node != math.inf:
			amountVistedNodes += 1
	return amountVistedNodes

def getDistance(vector1, vector2):
	#Calculates the distances between to pairs of lat. long.
    dlat = 2 * math.pi * (vector2[0] - vector1[0]) / 360
    mlat = 2 * math.pi * (vector1[0] + vector2[0]) / 2 / 360
    dlon = 2 * math.pi * (vector2[1] - vector1[1]) / 360
    return 6371009 * (dlat ** 2 + (math.cos(mlat) * dlon) ** 2) ** 0.5
def readInput():
	# Processes the input file int a format of
	# Node 1 = [[cords],[what node it connects to]]
	# and in the list, index 0 is Node 1, and Node 1000 is index 999
	file = open("Input_Graph.txt","r+")
	nodes = list()
	i = 0
	while i < 1000:
		line = file.readline()
		fields = line.split(":")
		fields = fields[1].split(",")
		fields[0] = float(fields[0])
		fields[1] = float(fields[1])
		node = Node()
		node.vector = [fields[0], fields[1]]
		nodes.append(node)
		i += 1
	file.readline()
	i = 0
	while i < 1000:
		line = file.readline()
		fields = line.split(":")
		fields = fields[1].split(",")
		for data in fields:
			try:
				nodes[i].edges_to.append(int(data) - 1)
			except ValueError:
				continue
		i += 1
	return nodes
def dijkstra(startNode, goalNode, listOfNodes):
	fringe = PriorityQueue() #PQ of indices of the Nodes
	fringe.push(startNode,0) # startNode  is start
	distToNodes = [math.inf] * 1000 #the distances of the nodes visisted
	distToNodes[startNode] = 0
	while not fringe.isEmpty():
		#Get Next Node
		currentNode = fringe.pop()
		if currentNode == goalNode:
			return distToNodes
		for connectedNode in listOfNodes[currentNode].edges_to:
			distance = distToNodes[currentNode] + getDistance(
					listOfNodes[currentNode].vector, listOfNodes[connectedNode].vector)
			if distance < distToNodes[connectedNode]:
				distToNodes[connectedNode] = distance
				fringe.update(connectedNode, distance)
	return distToNodes
def aStar(startNode, goalNode, listOfNodes):
	fringe = PriorityQueue() #PQ of indices of the Nodes
	fringe.push(startNode,0) # startNode  is start
	distToNodes = [math.inf] * 1000 #the distances of the nodes visisted
	distToNodes[startNode] = 0
	while not fringe.isEmpty():
		#Get Next Node
		currentNode = fringe.pop()
		# print("Current Node", currentNode, "Current distance ", distToNodes[currentNode])
		#check if goal state
		if currentNode == goalNode:
			return distToNodes
		for connectedNode in listOfNodes[currentNode].edges_to:
			distance = distToNodes[currentNode] + getDistance(
					listOfNodes[currentNode].vector, listOfNodes[connectedNode].vector)
			if distance < distToNodes[connectedNode]:
				distToNodes[connectedNode] = distance
				fringe.update(connectedNode, distance + getDistance(
					listOfNodes[connectedNode].vector, listOfNodes[goalNode].vector))
	return distToNodes
def landmarkSearch(startNode, goalNode, listOfNodes, landmarks):
	fringe = PriorityQueue() #PQ of indices of the Nodes
	fringe.push(startNode,0) # startNode  is start
	distToNodes = [math.inf] * 1000 #the distances of the nodes visisted
	distToNodes[startNode] = 0
	while not fringe.isEmpty():
	#Get Next Node
		currentNode = fringe.pop()
		# print("Current Node", currentNode, "Current distance ", distToNodes[currentNode])
		#check if goal state
		if currentNode == goalNode:
			return distToNodes
		for connectedNode in listOfNodes[currentNode].edges_to:
			distance = distToNodes[currentNode] + getDistance(
					listOfNodes[currentNode].vector, listOfNodes[connectedNode].vector)
			if distance < distToNodes[connectedNode]:
				distToNodes[connectedNode] = distance
				fringe.update(connectedNode, 
					distance + landmarkHueristic(landmarks,connectedNode,goalNode))
	return distToNodes
def findLandmarks(listOfNodes):
	# find 4 landmarks, each being the max/min of both
	#	Lat. and Long
	maxLong = 0
	maxLat = 0
	minLong = 0
	minLat = 0
	landmarks = [None] * 4
	for i in range(1000):
		if listOfNodes[i].vector[0] < listOfNodes[minLat].vector[0]:
			minLat = i
		elif listOfNodes[i].vector[0] > listOfNodes[maxLat].vector[0]:
			maxLat = i
		elif listOfNodes[i].vector[1] < listOfNodes[minLong].vector[1]:
			minLong = i
		elif listOfNodes[i].vector[1] > listOfNodes[maxLong].vector[1]:
			maxLong = i
	maxLongLandmark = dijkstra(maxLong, 1000, listOfNodes)
	maxLatLandmark = dijkstra(maxLat, 1000, listOfNodes)
	minLongLandmark = dijkstra(minLong, 1000, listOfNodes)
	minLatLandmark = dijkstra(minLat, 1000, listOfNodes)
	landmarks[0] = minLatLandmark
	landmarks[1] = maxLatLandmark
	landmarks[2] = minLongLandmark
	landmarks[3] = maxLongLandmark
	return landmarks
def landmarkHueristic(landmarks, postion, goalPosition):
	e1 = abs(landmarks[0][goalPosition] - landmarks[0][postion])
	e2 = abs(landmarks[1][goalPosition] - landmarks[1][postion])
	e3 = abs(landmarks[2][goalPosition] - landmarks[2][postion])
	e4 = abs(landmarks[3][goalPosition] - landmarks[3][postion])
	return max(e1,e2,e3,e4)
class PriorityQueue:
	# Priority Queue is from a previous assignment
	# created by John DeNero
	# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
	# Student side autograding was added by Brad Miller, Nick Hay, and
	# Pieter Abbeel (pabbeel@cs.berkeley.edu).
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
#End Priority Queue
def main():
	listOfNodes = readInput()
	landmarks = findLandmarks(listOfNodes)
	numTests = 20
	dijktest = 0
	aStartTest = 0
	landTest = 0
	for x in range(numTests):
		start = random.randint(0,999)
		goal = random.randint(0,999)
		n = dijkstra(start,goal,listOfNodes)
		dijktest += getNumberNodesVisited(n)
		a = aStar(start,goal,listOfNodes)
		aStartTest += getNumberNodesVisited(a)
		l = landmarkSearch(start,goal,listOfNodes,landmarks)
		landTest += getNumberNodesVisited(l)
	avgNodesD = dijktest/numTests
	avgNodesA = aStartTest/numTests
	avgNodesL = landTest/numTests
	print("dijkstra Avg nodes Visited: ", avgNodesD)
	print("A* Avg nodes Visited: ", avgNodesA)
	print("Landmark search Avg nodes Visited: ", avgNodesL)
	print("A* visits ", (avgNodesA/avgNodesD)*100, "Percent less Nodes visited than Dijkstras")
	print("Landmark visits ", (avgNodesL/avgNodesD)*100, "Percent less Nodes visited than Dijkstras")

if __name__ == "__main__":
    main()