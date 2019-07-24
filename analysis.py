import re
from collections import defaultdict
class Analyzer:
	def __init__(self, filename):
		try:
			our_file = open(filename, "r")
			self.text = our_file.read()
			our_file.close()
			self.words = self.getWords()
			self.unique = self.getUniqueWords()
		except Exception as ex:
			print("Cannot open file : " + filename)
			print(ex)
			self.text = ""
	def print_text(self):
		print(self.text)

	def getWords(self):
		start = "THE ILIAD." #get rid of this guy's introduction
		end = "END OF THE ILLIAD" #get rid of this guy's footnotes
		s = self.text.find(start)
		e = self.text.find(end) + len(end)
		relevant = self.text[s:e]
		answer = re.split("[^a-zA-Z’]+", relevant)
		return answer

	def getNumberOfWords(self):
		return len(self.words)

	def getUniqueWords(self):
		#case insensitive; but "allowed" can be different than "allow'd"
		answer = defaultdict(int)
		for i in self.words:
			answer[i.lower()] += 1
		return answer
	def getTotalUniqueWords(self):
		return len(self.unique)


iliad = Analyzer('iliad.txt')
print(iliad.unique)
print(iliad.getNumberOfWords())
print(iliad.getTotalUniqueWords())