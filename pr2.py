# Student: Bryan Allen
# Class: CS456 Spring 2015
# Assignment: Project 2
# Required Files: alphabet.txt
# To Run: navigate to folder containing pr2.py in console/terminal and enter: python pr1.py

import os, sys, math, collections, string

class HuffNode(object):
	def __init__(self, c, f, l=None, r=None):
		self.character = c
		self.freq = f
		self.left = l
		self.right = r
	
class MinHeap:
	def __init__(self, items=None):
		if items == None:
			self.__items = collections.deque()
		else:
			self.__items = self.__build_heap(items)

	def __build_heap(self, items):
		count = len(items)
		for i in range(int(math.floor(count/2)) - 1, -1, -1):
			self.__heapify(items, i, count)
		return items

	def __heapify(self, items, idx, max_element):
		left = 2*idx + 1
		right = 2*idx + 2

		# Compare the value of the left child with value at the index
		# to determine which is smallest
		if left < max_element and items[left].freq < items[idx].freq:
			smallest = left
		else:
			smallest = idx

		# Now, compare the value of the right child with the smallest
		# determined above, again picking the smallest
		if right < max_element and items[right].freq < items[smallest].freq:
			smallest = right

		if not smallest == idx:
			items[idx], items[smallest] = items[smallest], items[idx]
			self.__heapify(items, smallest, max_element)

	def add(self, item):
		self.__items.append(item)
		self.__build_heap(self.__items)

	def remove(self):
		item = self.__items.popleft()
		self.__build_heap(self.__items)
		return item

	def is_empty(self):
		return len(self.__items) == 0
		
	def isSizeOne(self):
		return len(self.__items) == 1
		
class HuffTree(object):
	def __init__(self, frequencies):
		self.heap = MinHeap()
		self.map = frequencies
		for f in frequencies:
			self.heap.add(HuffNode(f, frequencies[f]['freq']))
			
		while not self.heap.isSizeOne():
			left = self.heap.remove()
			right = self.heap.remove()
			print 'combining two smallest nodes', left.character, left.freq, right.character, right.freq, left.freq + right.freq
			
			top = HuffNode(None, left.freq + right.freq, left, right)
			self.heap.add(top)
			
		self.root = self.heap.remove()
		arr = []
		self.createMap(self.root, arr)
	
	def createMap(self, root, arr):
		if(root.left):
			newarr = list(arr)
			newarr.append(0)
			self.createMap(root.left, newarr)
		if(root.right):
			newarr = list(arr)
			newarr.append(1)
			self.createMap(root.right, newarr)
		if not root.left and not root.right:
			self.map[root.character]['code'] = ''.join(str(i) for i in arr)
			
	def getAvg(self):
		avg = 0
		for c in self.map:
			avg += len(self.map[c]['code']) * ( self.map[c]['freq'] / 100.0)
		return avg
			
	def printMap(self):
		print 'Average:', self.getAvg()
		for c in self.map:
			print c, self.map[c]['code']
	
	def encodeString(self, string):
		output = []
		for c in string:
			output.append(self.map[c]['code'])
		
		return ''.join(str(i) for i in output)
		
	def decode(self, string):
		
	
	
		
if __name__ == "__main__":
	root = os.path.dirname(os.path.realpath(sys.argv[0]))
	inputFile = os.path.join(root, 'alphabet.txt')
	ifile = open(inputFile)
	
	# get input from file
	frequencies = {}	
	for line in ifile:
		l = line.split()
		temp = {'freq':int(l[1])}
		frequencies[l[0]] = temp
		
	for f in frequencies:
		print f, frequencies[f]['freq']
	
	huffTree = HuffTree(frequencies)
	
	huffTree.printMap()
	
	text = str(raw_input('type in a string to encode: '))
	print huffTree.encodeString(text)