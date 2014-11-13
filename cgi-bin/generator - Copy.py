#!/usr/bin/python

import os
import fileinput
import random

class Helper(object):
	def __init__(self):
		pass
	
	def getLongest(self, array):
		longest = ""
		for i in array:
			if len(i) > len(longest):
				longest = i 
		return array.index(longest)

class Generator(object):
	
	# Constructor
	def __init__(self, query):
		#self.dictionary_path = 'C:\\Users\\Joshua\\Documents\\GitHub\\School\\joshuamjaxon.github.io\\cgi-bin\\words.txt'
		self.dictionary_path = 'cgi-bin\\words.txt'
		self.getDictionary(self.dictionary_path)
		self.setOptions(query)
		self.helper = Helper()
		self.words = []
	
	def setOptions(self, query):
		# Create an empty dictionary to hold options
		self.options = {}
		# Split query into key-value pairs
		temp = query.split('&')
		# Split key-value pairs
		for pair in temp:
			self.options[pair.split('=')[0]] = pair.split('=')[1]
	
	def getDictionary(self, path):
		# Create dictionary for generator
		self.dictionary = []
		# Open file
		f = open(path);
		# Count lines
		for line in f:
			temp = f.readline()
			if temp.find('\'') == -1:
				self.dictionary.append(temp.strip('\n'))
		# Close the file
		f.close()
	
	def chooseWord(self):
		# Loop 'forever' if necessary
		while True:
			# Get random line
			num = random.randrange(len(self.dictionary))	
			# Return word in that line if it matches user selected options
			if len(self.dictionary[num]) >= int(self.options['minlength']) and len(self.dictionary[num]) <= int(self.options['maxlength']):
				break
		# Return a word that works
		return self.dictionary[num]
					
	def choosePassword(self):
		# Reset word length
		self.words = []
	
		# Choose four random words
		for i in range(4):
			self.words.append(self.chooseWord())
		
		# Check password length
		pass_length = 0
		while True:
			for i in self.words:
				pass_length += len(i)
			if pass_length > int(self.options['length']):
				self.words[self.helper.getLongest(self.words)] = self.chooseWord()
			else:
				break
				
		# Optimize for typing speed
		
		
		# Concatenate password
		password = '{0}{1}{2}{3}'.format(self.words[0], self.words[1], self.words[2], self.words[3])
		
		# Replace special characters
		revised_password = ""
		for char in password:
			if char == 'a':
				revised_password += '4'
			else:
				revised_password += char
		
		return revised_password

def parseQuery(query):
	# Create an empty dictionary to hold options
	options = {}
	
	# Split query into key-value pairs
	query = query.split('&')
	
	# Split key-value pairs
	for pair in query:
		options[pair.split('=')[0]] = pair.split('=')[1]
	
	return options	

def main():
	pass_gen = Generator(os.environ['QUERY_STRING'])

	print (
	'''Content-type: text/html\n
	<html>
		<head>
			<title>Results</title>
			<link rel="stylesheet" type="text/css" href="\\style.css">
		</head>
		<body>
			<header>
				<h1>XKCD Password Generator</h1>
			</header>
			<section>
				<h1>Results</h1>
				<ul>''')
	
	for i in range(10):
		print ('<li>' + pass_gen.choosePassword() + '</li>')
	
	print (
	'''			</ul>
			</section>
			<footer>
				<p>&copy; Copyright 2014, Joshua Jackson.</p>
			</footer>
		</body>
	</html>''')

main()