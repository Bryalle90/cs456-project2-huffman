# Student: Bryan Allen
# Class: CS456 Spring 2015
# Assignment: Project 2
# Required Files: alphabet.txt
# To Run: navigate to folder containing pr2.py in console/terminal and enter: python pr2.py

import os, sys, math, collections

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
		
	def isSizeOne(self):
		return len(self.__items) == 1
		
class HuffTree(object):
	def __init__(self, frequencies):
		# create min-heap and add input frequencies
		self.__heap = MinHeap()
		self.__map = frequencies
		for f in frequencies:
			self.__heap.add(HuffNode(f, frequencies[f]['freq']))
			
		while not self.__heap.isSizeOne():
			# remove the two smallest frequencies and create a parent for them
			left = self.__heap.remove()
			right = self.__heap.remove()
			parent = HuffNode(None, left.freq + right.freq, left, right)
			
			# insert parent into the heap
			self.__heap.add(parent)
			
		# when there is only one node in the heap, remove it and set it as the root for the huffman tree
		self.__root = self.__heap.remove()
		code = ''
		self.__createMap(self.__root)
	
	def __createMap(self, curr, code=''):
		if(curr.left):
			newcode = code
			newcode += '0'
			self.__createMap(curr.left, newcode)
		if(curr.right):
			newcode = code
			newcode += '1'
			self.__createMap(curr.right, newcode)
		if not curr.left and not curr.right:
			self.__map[curr.character]['code'] = code
			
	def getMap(self):
		return self.__map
		
	def getAvg(self):
		avg = 0
		for c in self.__map:
			avg += len(self.__map[c]['code']) * ( self.__map[c]['freq'] / 100.0)
		return avg
			
	def printMap(self):
		print 'Average:', self.getAvg()
		for c in self.__map:
			print c, self.__map[c]['code']
	
	def encodeString(self, string):
		output = ''
		for c in string:
			output += self.__map[c]['code']
		
		return output
		
	def decode(self, string, loc=0, r=None):
		curr = r if r else self.__root
		out = curr.character
		if loc < len(string):
			# if current bit is a 0 and there is a child to the left
			if curr.left and string[loc] == '0':
				out = self.decode(string, loc + 1, curr.left)
				
			# if current bit is a 1 and there is a child to the right
			elif curr.right and string[loc] == '1':
				out = self.decode(string, loc + 1, curr.right)
				
			# if current node is a leaf
			if not curr.left and not curr.right:
				d = self.decode(string, loc)
				if d:
					out += d
				else:
					out = d
		return out
		
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
	
	'''
	# print the input
	print 'input:'
	for f in frequencies:
		print f, frequencies[f]['freq']
	print ''
	'''
	
	# create Huffman tree
	huffTree = HuffTree(frequencies)
	
	'''
	# print Huffman codes
	huffTree.printMap()
	'''
	
	# output Huffman codes to file
	ofile = open('hcodes.txt', 'w')
	ofile.write('Average: '+str(huffTree.getAvg())+'\n')
	map = huffTree.getMap()
	for c in map:
		ofile.write(c+' '+map[c]['code']+'\n')
	
	# get string to encode
	text = str(raw_input('type in a string to encode: '))
	print huffTree.encodeString(text)
	print ''
	
	# get string to decode
	text = str(raw_input('type in a string to decode: '))
	output = huffTree.decode(text)
	if output:
		print output
	else:
		print text, 'is not decodable'