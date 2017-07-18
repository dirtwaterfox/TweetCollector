import urllib
import twurl
import oauth
import json
import sqlite3
import unicodedata
conn = sqlite3.connect('tweetsearch.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Tweets;
CREATE TABLE Tweets (number INTEGER, quote TEXT, retweeted INTEGER, sent_at TEXT, favorited INTEGER)''')
tweetcount = 0
#Resource URL for searching tweets	
TWITTER_URL='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='
acct = 'JoshDeyton'
#Enter search topic - must be URI encoded
person=raw_input('Who would you like to search? ')
x=int(raw_input('How many times? '))
#add search parameters to resource url



API_limit = 180
count=0
max_id=0
url = twurl.augment(TWITTER_URL,{'screen_name': person})
print 'Searching ',url
connection = urllib.urlopen(url)
data = connection.read()
headers = connection.info().dict
#See number of searches left
API_limit=headers['x-rate-limit-remaining']
print 'Remaining: ', API_limit
js = json.loads(data)
#print json.dumps(js, indent=4)
	
#in the json data we need to find the screen name, user location, and the tweeted text we
#we only want to print tweets that have text and avoid other media

for u in js:
	 
		#some tweets had unicode characters that were causing errors in printing so all the unicode
		# were changed to string using unicodedata function
	if type(u['text'])== unicode:
		tweet = unicodedata.normalize('NFKD', u['text']).encode('ascii','ignore')
	else:
		tweet = u['text']
	
	if tweet[0]!='R' and tweet[1]!='T':	#don't want to include retweets in my data set

		retweet_count = u['retweet_count'] #number of times it was retweeted
		favorites_count = u['favorite_count'] #number of times it was liked
		created_at = u['created_at'] #date created (text) example 'Sun Feb 07 22:23:34 +0000 2010"
			
		tweetcount +=1
		cur.execute('''INSERT OR IGNORE INTO Tweets (number,quote,retweeted,sent_at,favorited) 
				VALUES (?,?,?,?,?)''' , (tweetcount,tweet,retweet_count,created_at,favorites_count ))
	
		
		print tweet
	max_id=u['id']	
cur.executescript('SELECT number,quote FROM Tweets ORDER BY number') #for some reason I had to add this line
#to get the info to store in the table.  They should already be inserted by number anyway
conn.commit
count+=1
print 'Tweets collected: ',tweetcount
while count < x:
	url = twurl.augment(TWITTER_URL,{'screen_name': person, 'max_id': max_id-1})
	print 'Searching ',url
	connection = urllib.urlopen(url)
	data = connection.read()
	headers = connection.info().dict
#See number of searches left
	API_limit=headers['x-rate-limit-remaining']
	print 'Remaining: ', API_limit
	js = json.loads(data)
	#print json.dumps(js, indent=4)
	
#in the json data we need to find the screen name, user location, and the tweeted text we
#we only want to print tweets that have text and avoid other media

	for u in js:
	 
		#some tweets had unicode characters that were causing errors in printing so all the unicode
		# were changed to string using unicodedata function
		if type(u['text'])== unicode:
			tweet = unicodedata.normalize('NFKD', u['text']).encode('ascii','ignore')
		else:
			tweet = u['text']
	
		if tweet[0]!='R' and tweet[1]!='T':	#don't want to include retweets in my data set
	
			retweet_count = u['retweet_count'] #number of times it was retweeted
			favorites_count = u['favorite_count'] #number of times it was liked
			created_at = u['created_at'] #date created (text) example 'Sun Feb 07 22:23:34 +0000 2010"
			tweet_id = u['id']
			tweetcount +=1
			cur.execute('''INSERT OR IGNORE INTO Tweets (number,quote,retweeted,sent_at,favorited) 
				VALUES (?,?,?,?,?)''' , (tweet_id,tweet,retweet_count,created_at,favorites_count ))
			print tweet
		max_id=u['id']	
	cur.executescript('SELECT number,quote FROM Tweets ORDER BY number')
	conn.commit
	count+=1
	print 'Tweets collected: ',tweetcount
