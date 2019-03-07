import feedparser
import urllib2
import os
import code
import datetime
import sys


############### Settings ################
#Subreddit = "/user//m/wallpapers"		### Replaced by argument
#ImageDir = "/Users/darrenj/Pictures/reddit_autowall/"	### Replaced by argument
EraseOldPics = True
#########################################

if len(sys.argv) != 3:
	print "Incorrect number of arguments"
	print "Entered " + str(len(sys.argv)) + ", should be 3"
	quit()

Subreddit = sys.argv[1]
print "Subreddit is " + Subreddit
ImageDir = sys.argv[2]
print "Image directory is " + ImageDir

Log = open( ImageDir+ "reddit_autowall.log", 'a' )
Log.write( datetime.datetime.now().strftime("%x %X") + "\n" )
Log.write( Subreddit + "\n" + ImageDir + "\n")
Log.close()

print "Parsing feed from " + Subreddit + "..."
RedditFeed = feedparser.parse('http://www.reddit.com' + Subreddit + '/.rss')
Addresses = []

for Entry in RedditFeed.entries:
	Link = Entry.description[ : Entry.description.find(">[link]")-1 ]
	Addresses.append( Link[ Link.rfind("<a href=")+9 : ] )

print "Found " + str(len(Addresses)) + " total entries."
FileList = []

for Entry in Addresses:
	if Entry.endswith(".jpg") or Entry.endswith(".png"):
		Filename = Entry.split('/')[-1]
		FileList.append( Filename )
		if os.path.exists( ImageDir+Filename ):
			print Filename + " exists"
		else:
			print "Saving " + Filename + "..."
			File = open( ImageDir+Filename, 'wb' )
			Url = urllib2.urlopen( Entry )
			File.write( Url.read() )
			File.close()

if EraseOldPics:
	print "Erasing old pictures..."
	for ExistingFile in os.listdir(ImageDir):
		#code.interact( local= locals() )
		if not ExistingFile in FileList:
			if ExistingFile.endswith(".jpg") or ExistingFile.endswith(".png"):
				os.remove( ImageDir+ExistingFile )
				print ExistingFile + " removed"


