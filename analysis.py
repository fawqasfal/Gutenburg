import re
from functools import reduce
from random import randrange

TOP_500 = set()
try:
	common_words_file = open('mostcommon.txt', 'r')
	common_words = common_words_file.read().split("\n")
	TOP_500 = set(common_words[:500])
except:
	pass
'''Gives you the top_500 words. 
I put an exception in case anyone tries to import analysis.py 
to analyze a different book and it runs the module trying to find 'mostcommon.txt' or 'iliad.txt'
'''

TEXT = "iliad.txt"
CHAPTERS =\
"""BOOK I.
BOOK II.
BOOK III.
BOOK IV.
BOOK V.
BOOK VI.
BOOK VII.
BOOK VIII.
BOOK IX.
BOOK X.
BOOK XI.
BOOK XII.
BOOK XIII.
BOOK XIV.
BOOK XV.
BOOK XVI.
BOOK XVII.
BOOK XVIII.
BOOK XIX.
BOOK XX.
BOOK XXI.
BOOK XXII.
BOOK XXIII.
BOOK XXIV.
END OF THE ILLIAD"""

CHAPTER_FINDER = [chapter + "\n\n" for chapter in CHAPTERS.split("\n")]

'''
These three variables are what's necessary to run the analyzer class on any text. 
You need a filename that has the text of the book, a list of chapter dilineators 
that can uniquely be found and indexed in the text so as to break up the book into it's chapters,
and you need some kind of iterable, preferably a set, that contains the most common words you want to ignore in generating
the most interesting words.
'''
class Analyzer:
	def __init__(self, filename, chapter_finder, common):
		try:
			our_file = open(filename, "r")
			self.text = our_file.read()
			our_file.close()
			self.chapter_finder = chapter_finder
			self.common = common
		except Exception as ex:
			exception_string = "Cannot open file: " + filename
			raise Exception(exception_string)
			self.text = ""

	def print_text(self):
		print(self.text)

	def getWordsByChapter(self):
		#returns a 2D array that contains the list of words, with each array representing a chapter.
		if not hasattr(self, 'words'):
			self.words = []
			for start, end in self.getChapterIndices():
				relevant = self.text[start:end]
				self.words.append(re.split("[^a-zA-Z’']+", relevant))
				#splits the words on anything that isn't a-z, A-Z, or ' or ’, which is necessary to keep words like 'allow’d'
				#note, we ignore numbers, because i don't want a bunch of page numbers like 'p32' or 'p176' cluttering up my words
		return self.words

	def getNumberOfChapters(self):
		return len(self.getWordsByChapter())

	def getUniqueWords(self):
		'''
		The easiest and quickest way to store data pertaining to this text, given the functions I need to implement, is to have 
		1. a 2D array that contains all the words in the text, broken up by chapter (getWordsByChapter())
		2. a hash map that has  unique words as keys, and arrays that have those unique words' frequencies in each chapter as values
		(the keys are case insensitive, but punctuation sensitive - `allowed' is different from `allow'd')

		So, for example, Map['tRoY'] = [3, 17, 15, 14, 16, 20, 12, 10, 11, 10, 6, 6, 17, 10, 13, 20, 23, 11, 3, 11, 15, 14, 1, 19]
		Because there are 24 chapters, the array has 24 indices, 
		and 'tRoy' (and it's case-altered variants) appears in each chapter as often as that chapter's index in the array. 

		this function builds that hash map
		'''
		#case insensitive; but "allowed" can be different than "allow'd"
		if not hasattr(self, 'unique'):
			self.unique = {}
			num_chaps = self.getNumberOfChapters()
			words = self.getWordsByChapter()
			for chapter in range(num_chaps):
				for word in words[chapter]:
					if word.lower() not in self.unique:
						self.unique[word.lower()] = [0] * num_chaps
					self.unique[word.lower()][chapter] += 1
		return self.unique

	def getChapterIndices(self):
		#returns a list of 2-tuples, each has the start and end index of a chapter
		chapters = [self.text.find(chapter) for chapter in self.chapter_finder]
		return [(chapters[i], chapters[i + 1]) for i in range(len(chapters) - 1)]
	
	#Now we're done with the helper functions - these are the functions that are actually asked of us in the project...
	def getTotalNumberOfWords(self):
		length = 0 
		for chapter in self.getWordsByChapter():
			length += len(chapter)
		return length

	def getTotalUniqueWords(self):
		return len(self.getUniqueWords())

	def get20MostFrequentWords(self):
		unique = self.getUniqueWords()
		u_words = list(unique.keys())
		u_words.sort(key = lambda word: reduce((lambda freq1, freq2 : freq1 + freq2), unique[word]), reverse = True)
		''' 
		we take a list that contains the unique words, and sort them according to the following key function :
		Each Word is mapped on to an integer that represents the sum of all the frequencies in the HashMap[Word] array.
		This is to get the total frequency of the word in the entire text from it's frequencies in each chapter. 
		So, the key takes a Word and returns the result of that function. That function is implemented by reduce(),
		which takes HashMap[Word] and sums up all of the frequency integers in that array.
		Reverse = True because we want the largest frequency words first, not the smallest'''
		with_freq = [(word, reduce(lambda freq1, freq2 : freq1 + freq2, unique[word])) for word in u_words[:20]] 
		#attach frequencies to the word, and get the 20 most common
		return with_freq

	def get20MostInterestingFrequentWords(self):
		unique = self.getUniqueWords()
		ui_words = [word for word in unique if word not in self.common]
		ui_words.sort(key = lambda word: reduce((lambda freq1, freq2 : freq1 + freq2), unique[word]), reverse = True)
		with_freq = [(word, reduce(lambda freq1, freq2 : freq1 + freq2, unique[word])) for word in ui_words[:20]] 
		return with_freq

	def get20LeastFrequentWords(self):
		unique = self.getUniqueWords()
		u_words = list(unique.keys())
		u_words.sort(key = lambda word: reduce((lambda freq1, freq2 : freq1 + freq2), unique[word]))
		with_freq = [(word, reduce(lambda freq1, freq2 : freq1 + freq2, unique[word])) for word in u_words[:20]] 
		return with_freq

	def getFrequencyOfWord(self, word):
		unique = self.getUniqueWords()
		if word.lower() not in unique:
			return [0] * self.getNumberOfChapters()
		return unique[word.lower()]

	def getChapterQuoteAppears(self, quote):
		quote_broken = [word.lower() for word in re.split("[^a-zA-Z’']+", quote) if word != '']
		#breaking up the quote to 'look like' how we formatted our 2D array into words. 
		if len(quote_broken) == 0:
			return -1 #our formatting ruined it...
		words = self.getWordsByChapter()
		num_chaps = self.getNumberOfChapters()
		first_word = quote_broken[0]
		for chapter in range(num_chaps):
			first_matches = [i for i in range(len(words[chapter])) if words[chapter][i].lower() == first_word]
			'''
			found the indices in the current chapter that match the first word in the quote. 
			Now let's see if one of these indices is where the quote actually is.'''
			for pot in first_matches:
				pot_success = words[chapter][pot : pot + len(quote_broken)] 
				pot_success = [word.lower() for word in pot_success] #case-insensitive checks
				if pot_success == quote_broken:
					return chapter
		return -1 

	def generateSentence(self, start_word):
		words = self.getWordsByChapter()
		flattened = [word for chapter in words for word in chapter] 
		#for this specific function, our 2D array structure betrays us, and we need a one-dimensional list of words
		size = self.getTotalNumberOfWords()
		new_start = start_word.lower() #for more case-insensitive checks
		if new_start not in self.getUniqueWords():
			return "Can't generate a sentence with start word %s! It's not in the book."%start_word
		answer = [new_start]
		prev = new_start
		while len(answer) < 20:
			#checking everywhere the last word in the chain shows up in the text, case-insensitive 
			pot_next = [i for i in range(size) if flattened[i].lower() == prev.lower() and i < size - 1]
			''' i < size - 1 is for making sure the word we're looking at is not the last word of the book, 
			otherwise there will be no next word that could continue the chain. 
			'''
			if len(pot_next) == 0:
				#only one instance of the last word in the chain found, and it's the last word of a chapter ... 
				#we can't finish the sentence, so just return what we have
				break
			choice = pot_next[randrange(0,len(pot_next))] #pick an index! 
			prev = flattened[choice + 1] #word after that index 
			answer += [prev]
		answer[0] = answer[0][0].upper() + answer[0][1:] #make the first letter of the first word uppercase
		#adding a little flavor...
		pot_end = ['!', '?', '.']
		end = pot_end[randrange(0,len(pot_end))]
		return ' '.join(answer) + end

try:
	iliad = Analyzer(TEXT, CHAPTER_FINDER, TOP_500)

	printed_quote1 = "We, wretched mortals! lost in doubts below,But guess by rumour, and but boast we know,"
	tested_quote1 = '''(We, wretched mortals! lost in doubts below,
 	 But guess by rumour, and but boast we know,)'''

	printed_quote2 = "What time, deserting Ilion’s wasted plain, his conquering son, Alcides, plough’d the main."
	tested_quote2 = '''
		WhAt time, desErting IliON’s 
		wasted pLaIn,
 	 His conQuering 
 	 son, Alcides, plough’d the


 	  main.
		'''
	print("Number of words: %d"%iliad.getTotalNumberOfWords())
	print("Number of unique words: %d"%iliad.getTotalUniqueWords())
	print("20 most frequent words:\n %s\n"%iliad.get20MostFrequentWords())
	print("20 most frequent interesting words:\n%s\n"%iliad.get20MostInterestingFrequentWords())
	print("20 least frequent words:\n%s\n"%iliad.get20LeastFrequentWords())
	print("Frequency of the word Troy throughout the chapters: %s"%iliad.getFrequencyOfWord('trOy'))
	print("Frequency of the word Achilles throughout the chapters: %s"%iliad.getFrequencyOfWord('AchIlLeS'))
	print('Which chapter the quote "%s" appears in: %d'%(printed_quote1, iliad.getChapterQuoteAppears(tested_quote1)))
	print('Which chapter the quote "%s" appears in: %d'%(printed_quote2, iliad.getChapterQuoteAppears(tested_quote2)))
	print("Generated sentences: ")
	print(iliad.generateSentence("The"))
	print(iliad.generateSentence("Thou"))
	print(iliad.generateSentence("From"))
	print(iliad.generateSentence("The"))
	print(iliad.generateSentence("Thou"))
	print(iliad.generateSentence("From"))
	print(iliad.generateSentence("LittleKittyKats"))
except Exception as ex:
	print(ex)
	pass
	#Again, this is to prevent anyone importing analysis.py for the generally usable Analyzer class from running into problems