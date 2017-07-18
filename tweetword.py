import sqlite3
import time
import urllib
import zlib
import string

#conn = sqlite3.connect('tweetindex.sqlite')
#conn.text_factory = str
#cur = conn.cursor()

#cur.execute('''CREATE TABLE Tweets (number INTEGER , Cleaned_Messages TEXT)''')

conn2 = sqlite3.connect('tweetsearch.sqlite')
conn2.text_factory = str
cur2 = conn2.cursor()

counts = dict()
cur2.execute('''SELECT quote from Tweets''')
for message_row in cur2:
	text = message_row[0]			#get tweet from table
	text = text.translate(None, string.punctuation) #deal with punctuation
	text = text.translate(None, '1234567890')  #deal with numbers
	text = text.strip()  
	text = text.lower()   #everything lowercase for matching purposes
	words = text.split()	#pull words out of the text for counting
	for word in words:
		if len(word) < 5 : continue  #takes care of most articles and prepositions
		if word.startswith('http'): continue #eliminates links from the word count
		counts[word] = counts.get(word,0) + 1
# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for w in words[:100]:
	if highest is None or highest < counts[w] :
		highest = counts[w]
	if lowest is None or lowest > counts[w] :
		lowest = counts[w]
print 'Range of counts:',highest,lowest

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('tweetword.js','w')
fhand.write("tweetword = [")
first = True
for k in words[:100]:
	if not first : fhand.write( ",\n")
	first = False
	size = counts[k]
	size = (size - lowest) / float(highest - lowest)
	size = int((size * bigsize) + smallsize)
	fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print "Output written to tweetword.js"
print "Open tweetword.htm in a browser to view"