import feedparser
import Tkinter as tk
import ftplib
import time

class RSS:
	current_feed = ""
	#headlineDict = {"Security Focus News":"http://www.securityfocus.com/rss/news.xml",
	#"Security Focus Bugs":"http://www.securityfocus.com/rss/vulnerabilities.xml",
	#headlineDict = {"Corelan Standard":"https://www.corelan.be/index.php/feed/",
	headlineDict = {"SANS AppSec":"http://software-security.sans.org/blog/feed/",
	"SANS PenTesting":"https://pen-testing.sans.org/blog/pen-testing/feed/",
	"Schneier":"https://www.schneier.com/blog/atom.xml",
	"F-Secure":"http://safeandsavvy.f-secure.com/feed/",
	"BH_Consulting":"http://bhconsulting.ie/securitywatch/?feed=rss2",
	"Krebs":"http://krebsonsecurity.com/feed/",
	"Darkreading News":"http://www.darkreading.com/rss_simple.asp",
	"Darkreading_Attacks":"http://www.darkreading.com/rss_simple.asp?f_n=644&f_ln=Attacks/Breaches"}

	def __init__(self, url="http://www.darkreading.com/rss_simple.asp?f_n=662&f_ln=Advanced%20Threats"):
		self.current_feed = url
		
	def advance_feed(self):
		pass

	def all_headlines(self):
		for item in self.headlineDict.keys():
			self.current_feed = self.headlineDict[item]
			print "\n[+] " + item + "news feeds ---~~~{+]\n"
			self.headlines()
			
	def returnHeadlines(self):
		''' Returns leadlines from the currently selected news feed '''
		feed = feedparser.parse(self.current_feed)
		master = []
		for item in feed['entries']:
			master.append(item['title'])
		return master		


	def headlines(self):
		''' Returns leadlines from the currently selected news feed '''
		feed = feedparser.parse(self.current_feed)
		#feed = feedparser.parse(self.current_feed)
		#feed = {}							
		#feed['entries'] = <list_type>
		#feed['entries'][x] = {}
		#feed['entries'][x].keys()  		['summary_detail', 'links', 'title', 'summary', 'title_detail', 'link']
		#feed['entries'][x]['title']
		master = []
		for item in feed['entries']:
			master.append(item['title'])

	def returnHeadlines(self):
		''' Returns leadlines from the currently selected news feed '''
		feed = feedparser.parse(self.current_feed)
		master = []
		for item in feed['entries']:
			master.append(item['title'])
		return master

	def links(self):
		feed = feedparser.parse(self.current_feed)
		master = []
		for item in feed['entries']:
			#print item['links'][0]['href']
			master.append(item['links'][0]['href'])
		return master

        #Returns a tuple object of a Headline/URL pair

	def getLinkContent(self):
		pass

	def get_dates(self):  		#grab the dates of the publication or what have you...
		pass
	
	def get_stories(self):		#return both headlines and links in a tuple or even add the dates
		pass
		
	#Research playing videos... look to C# for this?  Maybe?  Ehh...  could be fun.  CodersneverCrash

	
def all_headlines(self):
	for item in self.headlineDict.keys():
		self.current_feed = self.headlineDict[item]
		print "\n[+] " + item + "news feeds ---~~~{+]\n"
	self.headlines()


'''
##  GUI Ticker Tape Generator
collection = RSS()
tickerTapeMaterial = ''
tickerBuffer = []
for item in collection.headlineDict.keys():
        collection.current_feed = collection.headlineDict[item]
        tickerBuffer.append(collection.returnHeadlines())
        
for item in tickerBuffer:
        tickerTapeMaterial += `item`

'''



def generateNewsPage():
	file1 = open("c:\\Python27\\AIC_Links_Bot\\topPage.txt")
	file2 = open("c:\\Python27\\AIC_Links_Bot\\bottomPage.txt")
	mainpage = open('links.html', 'w')
	collection = RSS()
	dynText = ''
	NewsStories = []
	for item in collection.headlineDict.keys():						#for each RSS url in the class
		collection.current_feed = collection.headlineDict[item]		#change the feed
		headline_titles = collection.returnHeadlines()				#get headlines for the current RSS url
		#print item
		headline_links  = collection.links()
		for item in collection.returnHeadlines():
		#print item
			print "Retrieved " + `item`
			NewsStories.append((item, headline_links[headline_titles.index(item)]))
	
	dynText += '<b>Last updated: </b>'+time.ctime()+'<br>'
	dynText += '<blockquote>'
	for i in NewsStories:
			#dynText += '<h1>'+item+'</h1>'
		try:
			dynText += '<li><a href=\"' + i[1] + '\">' + i[0] + "</a></li>"
		except:
			pass

	#build the page
	print "Building the HTML file..."
	mainText = ''
	for item in file1:
		mainText += item
	for item in dynText:
		mainText += item
	for item in file2:
		try:                        
			mainText += item
		except:
			pass
	print "Done."

	mainText.encode('ascii', 'ignore')
	for item in mainText:					# Combine all links, discard those that error out
		try:
			mainpage.write(item)
		except:
			pass
	mainpage.close()
	
	print "Uploading file..."
	session = ftplib.FTP('ftp.brentchambers.net', 'bchambers1221', 'Penelope7721!')
	file = open('links.html', 'rb')
	session.cwd('/')
	session.storbinary('STOR links.html', file)
	file.close()
	session.quit()

if __name__=="__main__":
	generateNewsPage()