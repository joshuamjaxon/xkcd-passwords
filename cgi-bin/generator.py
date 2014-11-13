#!/usr/bin/python


import os			# Import os for environment variables
import fileinput	# Import fileinput to read dictionary
import random		# Import random to generate random numbers


# Class containing helper functions and variables
class Helper(object):
	# Constructor
	def __init__(self):
		# Create list containing all characters on left hand side of keyboard
		self.leftHandChars = ['1', '2', '3', '4', '5', 'q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c']
	
	# From  a list of strings, returns the index of the longest string
	def getLongest(self, array):
		# Create empty string
		longest = ""
		# Iterate through list elements
		for i in array:
			# If new string is longer than current longest, replace it
			if len(i) > len(longest):
				longest = i 
		# Return index of longest string
		return array.index(longest)

		
# Class containing functions and variables for generating random passwords
class Generator(object):
	
	# Constructor
	def __init__(self, query):
		self.dictionary_path = 'cgi-bin\\words.txt'	# Path to dictionary to use
		self.getDictionary(self.dictionary_path)	# Get dictionary from path
		self.setOptions(query)						# Parse query string
		self.helper = Helper()						# Object containing helper functions
		self.words = []								# Words in password
	
	# Parses query string into dictionary format
	def setOptions(self, query):
		# Create an empty dictionary to hold options
		self.options = {}
		# Split query into key-value pairs
		temp = query.split('&')
		# Split key-value pairs
		for pair in temp:
			self.options[pair.split('=')[0]] = pair.split('=')[1]
	
	# Reads dictionary file into python dictionary from path
	# Words are sorted by their length
	def getDictionary(self, path):
		# Create dictionary for generator
		self.dictionary = {}
		# Open file
		f = open(path);
		# Iterate through lines
		for line in f:
			# Read next line in file
			temp = f.readline()
			# Only add to dictionary if word has no apostrophes
			if temp.find('\'') == -1:
				# Add new key for word length if it doesn't already exist
				if (len(temp) - 1) not in self.dictionary:
					self.dictionary[len(temp) - 1] = []
				# Add new word to dictionary
				self.dictionary[len(temp) - 1].append(temp.strip('\n'))
		# Close the file
		f.close()
	
	# Given a minimum and maximum length per word, as well as an overall limit,
	# generates a list containing the lengths each word in the password should have
	def getWordLengths(self, min, max, limit):
		# Create empty list
		lengths = []
		# Get excess characters based on minimum word length
		leftovers = limit - 4 * min
		# Loop until an appropriate configuration is found
		while len(lengths) < 4:
			# Generate a random positive integer less than or equal to excess characters
			addend = random.randint(0, leftovers)
			# As long as the minimum plus the addend is not greater than the maximum,
			# append that number as the length of the word and subtract the addend from the excess
			if (min + addend) <= max:
				lengths.append(min + addend)
				leftovers -= addend
		# Return a list containing the lengths of each word in the password
		return lengths
	
	# Given a string, replaces certain characters in string based on user preferences
	def substitute(self, word):
		letters = ['a', 'e', 'i', 'l', 's', 'o']	# List of letters to possibly substitute
		numbers = ['4', '3', '1', '1', '5', '0']	# List of numbers to substitute for letters
		new_word = ""								# Blank string for revised word
		# Iterate through each character in string
		for char in word:
			# If the character is to be substituted, substitute it
			if char in self.options:
				new_word += numbers[letters.index(char)]
			# Otherwise append the original character to the new word
			else:
				new_word += char
		# Return the new word
		return new_word
						
			
	# Checks to see if a given string is optimized for typing
	def isOptimized(self, word):
		left = False	# Indicates if a character is on the left of the keyboard
		right = False	# Indicates if a character is on the right of the keyboard
		last = ""		# Last character
		# Optimization point total
		total = 0
		
		# Iterate through word and tally up points
		for char in word:
			# If first character, only assign side of keyboard
			if last == "":
				if char in self.helper.leftHandChars:
					left = True
				else:
					right = True
			# Else if the character is b, it is optimized for both sides of keyboard
			elif char == 'b':
				total += 1
				left = not left
				right = not right
			# Else if the last character was on the left and new character is on the right, add a point
			elif left:
				if char not in self.helper.leftHandChars:
					total += 1
					left = False
					right = True
			# Else if the last character was on the right and new character is on the left, add a point
			elif right:
				if char in self.helper.leftHandChars:
					total += 1
					left = True
					right = False
			# Otherwise three possibilities
			else:
				# Possibility 1: Add a point if letter is a duplicate
				if char == last:
					total += 1
				
				# elif char in self.helper.leftHandChars:
					# left = True
					# right = False
				# else:
					# left = False
					# right = True
			# Reassign last character to most recent character
			last = char
		# Find ratio of optimization points to word length
		total /= len(word)
		# Return true that word is optimized if ratio is at least 0.8
		if total >= 0.8:
			return True
		# Otherwise return false
		else:
			return False
	
	# Given a length, randomly pick a word from the dictionary of that length
	def chooseWord(self, chars):
		# Return a random word of length chars
		return self.dictionary[chars][random.randrange(len(self.dictionary[chars]))]
	
	# When called, returns a generated password
	def choosePassword(self):
		# Loop until password is generated
		while True:
			# Reset word length
			self.words = []
		
			# Get length of each word
			lengths = self.getWordLengths(int(self.options['minlength']), int(self.options['maxlength']), int(self.options['length']))
		
			# Choose four distinct random words
			for i in range(4):
				random_word = self.chooseWord(lengths[i]).lower()
				while random_word in self.words:
					random_word = self.chooseWord(lengths[i])
				self.words.append(random_word)
			
			# Capitalize necessary words
			if 'first' in self.options:
				self.words[0] = self.words[0].title()
			if 'second' in self.options:
				self.words[1] = self.words[1].title()
			if 'third' in self.options:
				self.words[2] = self.words[2].title()
			if 'fourth' in self.options:
				self.words[3] = self.words[3].title()
			
			# Concatenate password
			password = '{0}{1}{2}{3}'.format(self.words[0], self.words[1], self.words[2], self.words[3])
			
			# Replace special characters
			revised_password = self.substitute(password)
			
			# Break if word is optimized for typing speed
			if 'optimize' in self.options:
				if self.isOptimized(revised_password.lower()):
					return revised_password
			else:
				return revised_password

# Main function that generates and returns a webpage when called
def main():
	# Instantiate password generator using the query string
	pass_gen = Generator(os.environ['QUERY_STRING'])

	# Print the first portion of the webpage
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
	
	# Generate 10 passwords and add them to page as list elements
	for i in range(10):
		print ('<li>' + pass_gen.choosePassword() + '</li>')
	
	# Print the rest of the webpage
	print (
	'''			</ul>
			</section>
			<footer>
				<p>&copy; Copyright 2014, Joshua Jackson.</p>
			</footer>
		</body>
	</html>''')

# Run the main program 
main()