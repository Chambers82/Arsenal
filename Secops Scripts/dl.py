def download( URL ) :
	"""Copies the contents of a file from a given URL
	to a local file.
	"""
	import urllib
	keyword = {'putty':"http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe",
		   'insecure':"http://www.insecuremagazine.com/INSECURE-Mag-8.pdf",
		   'netcat':"http://brent.chambers.googlepages.com/nc.exe",
		   'nmap':"http://brent.chambers.googlepages.com/nmap-4.00.tar.bz2",
		   'tcpview':"http://brent.chambers.googlepages.com/tcpview.exe",
		   'qwinroot.exe':"http://brent.chambers.googlepages.com/qwinroot.exe",
		   'pcap':"http://brent.chambers.googlepages.com/pcap-1.1.win32-py2.5.exe",
		   'dpkt':"http://brent.chambers.googlepages.com/dpkt-1.6.win32.exe",
		   'windump':"http://brent.chambers.googlepages.com/windump.exe",
		   'winfo':"http://brent.chambers.googlepages.com/winfo.exe",
		   'etherchange':"http://brent.chambers.google.com/etherchange.exe",
		   'dumpusers':"http://brent.chambers.google.com/dumpusers.exe",
		   'scan':"http://brent.chambers.google.com/scan.exe",
		   "kiwi":"http://blog.gentilkiwi.com/downloads/mimikatz_trunk.zip",
		   'trunk':"http://blog.gentilkiwi.com/downloads/mimikatz_trunk.zip"}

	if URL in keyword.keys():
		URL = keyword[URL]
		WebFile = urllib.urlopen( URL )
		print "Please wait.  Downloading..."
		LocalFile = open( URL.split( '/' )[ - 1 ] , 'w' )
		LocalFile.write( WebFile.read() )
		WebFile.close()
		LocalFile.close()
		print "Download complete."
		print LocalFile
	else:
		try:
			WebFile = urllib.urlopen( URL )
			print "Please wait.  Downloading..."
			LocalFile = open( URL.split( '/' )[ - 1 ] , 'w' )
			LocalFile.write( WebFile.read() )
			WebFile.close()
			LocalFile.close()
			print "Download complete."
			print LocalFile
		except:
			print "Location unidentified"
			sys.exit[1]

def kiwi():
	kiwi="http://blog.gentilkiwi.com/downloads/mimikatz_trunk.zip"
	return kiwi

def windump():
	windump="http://brent.chambers.googlepages.com/windump.exe"
	return windump

def winfo():
	winfo="http://brent.chambers.googlepages.com/winfo.exe"
	return winfo

def etherchange():
	etherchange = "http://brent.chambers.googlepages.com/etherchange.exe"
	return etherchange

def dumpusers():
	dumpusers = "http://brent.chambers.googlepages.com/dumpusers.exe"
	return dumpusers

def scan():
	scan = "http://brent.chambers.googlepages.com/scan.exe"
	return scan

def putty():
	putty= "http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe"
	return putty

def insecure():
	insecure = "http://www.inscuremagazine.com/INSECURE-Mag-8.pdf"
	return insecure

def qwinroot():
	qwinroot = "http://brent.chambers.googlepages.com/qwinroot.exe"
	return qwinroot

def netcat():
	netcat = "http://brent.chambers.googlepages.com/nc.exe"
	return netcat

def nmap():
	nmap = "http://brent.chambers.googlepages.com/nmap-4.00.tar.bz2"
	return nmap

def tcpview():
	tcpview = "http://brent.chambers.googlepages.com/tcpview.exe"
	return qwinroot

def pcap():
	pcap = "http://brent.chambers.googlepages.com/pcap-1.1.win32.py2.5.exe"
	return pcap

def dpkt():
	dpkt = "http://brent.chambers.googlepages.com/dpkt-1.6.win32.exe"
	return dpkt


if __name__ == '__main__' :
	import sys
	if len( sys.argv ) == 2 :
		try :
			Download( sys.argv[ 1 ] )
		except IOError :
			print 'Filename not found.'
	else :
		import os
		print 'usage: %s http://server.com/path/to/filename' % os.path.basename( sys.argv[ 0 ] )

