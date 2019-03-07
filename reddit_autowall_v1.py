import feedparser
import urllib2
import os
import code
import datetime


############### Settings ################
Subreddit = "wallpapers"
ImageDir = "/Users/darrenj/Pictures/reddit_autowall/"
EraseOldPics = True
#########################################


Log = open( ImageDir+ "reddit_autowall.log", 'a' )
Log.write( datetime.datetime.now().strftime("%x %X") + "\n" )
Log.close()

print "Parsing feed from r/" + Subreddit + "..."
RedditFeed = feedparser.parse('http://www.reddit.com/r/' + Subreddit + '/.rss')
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


