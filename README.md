# TweetCollector
Collects and analyzes tweets from a searched user
This collection of programs uses a series of Python programs via command line to collect tweets.
At this point, the user must download all the files and run TweetCollector.py to begin collection.
The user will have to be logged into Twitter and set up a Twitter app in order to get proper authentication codes and keys for the program to work.
The user will also have to use these key from Twitter to edit the hidden.py file in order for the search to happen.
Once all that is set up, the user runs TweetCollector.py, which prompts the user for a twitter name to search and a number of times to run the search.  You can edit the file in order to run continuously, but eventually the TwitterAPI service will shut you down for excessive searches.
TweetCollector.py creates an SQLite file to store Tweet information.
Then Tweetword.py runs through the SQLite file and creates an html file that presents a wordcloud of the top 100 words found in the tweets. 
