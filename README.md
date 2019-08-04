<h1> The Iliad Analysis </h1>

This project does [some interesting analysis on a Project Gutenberg](http://www.gutenberg.org/cache/epub/6130/pg6130.txt)-provided copy of Homer's _The Iliad_. This includes the total number of words, the total number of unique words, the most frequent words, the most frequent *interesting* words, the least frequent words, the progression of the frequency of certain words throughout the chapters, finding chapter numbers of interesting quotes, and even, **generating strange-sounding nonsensical sentences that are nonetheless written in the language of _Homer_**. 

The results are in the attached PDF, and the code can be run by running "analysis.py". Furthermore, analysis.py is written to be rather reusable, such that as long as you have the full text file of a certain book, a set of common words you want to exclude from being "interesting" words, and an array of strings that represent chapter dilineators, you can run the code on any text you want. Example of this reusability in action is going to the /test folder and running analysis2.py on Adam Smith's _The Wealth of Nations_. 
