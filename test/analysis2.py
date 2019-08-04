import sys
sys.path.append("..")

import analysis
TEXT = "adamsmith.txt"
common_words_file = open('../mostcommon.txt', 'r')
common_words = common_words_file.read().split("\n")
TOP_500 = set(common_words[:500])
CHAPTER_FINDER =\
["INTRODUCTION AND PLAN OF THE WORK.", 
"BOOK I.", 
"BOOK II.", 
"BOOK III." 
"BOOK IV.", 
"BOOK V.", 
"End of the Project Gutenberg EBook"] 

adamsmith = analysis.Analyzer(TEXT, CHAPTER_FINDER, TOP_500)
print("Number of words: %d"%adamsmith.getTotalNumberOfWords())
print("Number of unique words: %d"%adamsmith.getTotalUniqueWords())
print("20 most frequent words:\n %s\n"%adamsmith.get20MostFrequentWords())
print("20 most frequent interesting words:\n%s\n"%adamsmith.get20MostInterestingFrequentWords())
print("20 least frequent words:\n%s\n"%adamsmith.get20LeastFrequentWords())
print("Generated sentences: ")
print(adamsmith.generateSentence("The"))
print(adamsmith.generateSentence("From"))
print(adamsmith.generateSentence("The"))
print(adamsmith.generateSentence("From"))
