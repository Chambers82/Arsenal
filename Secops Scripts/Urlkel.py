# Programmer: q0m
# Date: 1/23/2014
# Filename: Urlkel.py
# Description:  A foundation class for web functions for web attacks.
# CyberCorps DST Jackal***

# Usage:
#
# >>> import Urlkel
# >>> page = Urlkel.Urlkel("http://www.rootsecure.net")
# >>> page.url
# 'http://www.rootsecure.net'
# >>> page.fetchLinkTags()
# >>> page.dumpURLs()

# Additional work:
#  1) Build a fuzz function for url arguments
#  2) Build a data structure for recursive spidering
#  3) Build a spidering engine



import urllib
from BeautifulSoup import *
import string

class Urlkel:
	url = ''
	httpResponse = ''
	base_url = ''
	args = []
	#httpResponse = urllib.urlopen(url)
	
	def __init__(self, url):
		self.url = url
		self.httpResponse = urllib.urlopen(self.url) #grab it upon init, shouldn't be manual
	
	def fetchPage(self):
		self.httpResponse = urllib.urlopen(self.url)
		return self.httpResponse
	
	def fetchHeaders(self):
		headers = self.httpResponse.headers.items()
		return headers
		
		#for link in master
		# dump the source code
		# for each line in source code
		#		if "<form method=" in line:
		#			form_sites.append(link)   save the URL that has the form
		#searchResults = [t for t in master if "<form method=" in t]
		
	
	#techniqueSearchResults = [t for t in self.dump_techniques() if query in t]
	#techniqueSearchResults = [t for t in self.dump_techniques() if query in t]
	def fetchHeaderKeys(self):
		keys = self.httpResponse.headers.keys()
		return keys
		
	def snap(self):
		try:
			snappedURL = string.split(self.url, "?")
			if len(snappedURL) > 1:
				self.base_url = snappedURL[0]
				self.args = snappedURL[1:]
		except:
			self.base_url = snappedURL
		print "Self.base_url= ", self.base_url
		print "Self.args[]= ", self.args
		
	def fetchLinkTags(self):
		self.fetchPage()
		soup = BeautifulSoup(self.httpResponse.read())
		links = soup.findAll('a')
		return links
		
	def dumpURLs(self):
		self.fetchPage()
		soup = BeautifulSoup(self.httpResponse.read())
		links = soup.findAll('a')
		for link in links:
			print link['href']
			
			
def searchForms(url):
	master = []
	form_sites = []
	test = Urlkel(url)
	try:
		for link in test.dumpURLs():
			master.append(link)			#master list of URLs
	except:
		pass
	return master
