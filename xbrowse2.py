#Programmer:  Brent E. Chambers
#Date: 4/24/2015
#Filename:  xbrowse.py
#Description:  Browsing through the XML contents of panorama configurations

import xmltodict
import os
import string
import time
#import Pan

class xlBrowse:
    xdata = {}

    def __init__(self, xdata):
        self.xdata = xdata

    def root(self):
        for item in self.xdata:
            print

class xbrowse:
	labpano = ''                   # The instance of the class OR filename
	xdata = ''                     # The configuration dump
	cmd = ''
	context = ''
	contextString = ''
	contextStringArray = []
	availableCommands = []
	
	def __init__(self):#, xmlfilename):
		pass
		'''self.labpano = xmlfilename
		xmlfile = open(xmlfilename)
		data = xmlfile.read()
		self.xdata = xmltodict.parse(data)
		for item in self.xdata:                                           #generate the context
			self.contextStringArray.append(item)
			self.contextSTring = "[\'" + item + "\']"
			'''
		
	
	@classmethod
	def panInstance(self, panInstance):
		#Initializing with a pan instance
		self.labpano = panInstance                                        #copies the instance to the stored instance
		self.xdata = xlBrowse(self.labpano.global_config)                 #pulls the full config from subroutine global_config and creates instance
		for item in self.xdata:                                           #generate the context
			print type(self.xdata)
			self.contextStringArray.append(item)
			self.contextSTring = "[\'" + item + "\']"
		
	@classmethod
	def hostname(self, hostname):
		#Initializing with a hostname
		self.labpano = Pan.PanoramaAccess(hostname)                       #login to the pan and get the instance
		self.xdata = xlBrowse(self.labpano.global_config)                 #stores xata from 
		print type(self.xdata)
		for item in self.xdata:                                           #generate the context
			self.contextStringArray.append(item)
			self.contextSTring = "[\'" + item + "\']"
		
	
	@classmethod
	def xmlfile(self, xmlfilename):
		#Initializing with a xmlfile
		self.labpano = xmlfilename
		xmlfile = open(xmlfilename)
		data = xmlfile.read()
		self.xdata = xmltodict.parse(data)
		for item in self.xdata:                                           #generate the context
			self.contextStringArray.append(item)
			self.contextSTring = "[\'" + item + "\']"
	
	def console(self):
		print "\n [+] XBrowser v1.0"
		try:
			print "Resource:  ", self.labpano.hostname
		except:
			print "Resource:  ", self.labpano
		print "Timestamp: ", time.ctime()
		cmd = ''
		while string.upper(cmd) != "QUIT" or "EXIT":
			try:
				promptString = "\n"+self.labpano.hostname+":"+str(self.contextStringArray)+"> "        
			except:
				promptString = "\n"+self.labpano+":"+str(self.contextStringArray)+"> "
			cmd = raw_input(str(promptString))
			command = string.split(cmd, " ")
			
			if string.upper(command[0]) == "ROOT":
				for item in self.xdata:                 #Make the root of the file the root of the context
					self.contextStringArray = []
					self.contextStringArray.append(item)
					self.contextString = "[\'" + item + "\']"
			
			elif string.upper(command[0]) == "VIEW":
				#Needs to check for the existence of ['entry'] as the last item in context
				#in order to neatly display the items within that entry context.  
				
				#Also needs to evolve into a mechanism to cache the items, order them, and put
				#them into a format that will be easy to migrate
				self.availableCommands = []
				print "\nContext: ", str(self.contextString)
				try:
					exec("for item in self.xdata"+ self.contextString +": self.availableCommands.append(item)")
					exec("for item in self.xdata"+ self.contextString +": print item")
				except TypeError:
					pass			
			
			elif string.upper(command[0]) == "BACK":
				self.contextString = ""
				self.contextStringArray = self.contextStringArray[:-1]
				for item in self.contextStringArray:
					self.contextString = self.contextString + "[\'" + item + "\']"

			elif string.upper(command[0]) == "CONTEXT":
				print self.contextString
			
			
			elif command[0] in self.availableCommands:
				commandString = "[\'" + command[0] + "\']"              			#store command as string
				self.contextString = self.contextString + commandString           	#tack on commandString to context
				self.contextStringArray.append(command[0])                   		#add commandString to string Array
			
			elif string.upper(command[0]) == "HELP":					#move back to the
				print_help()

			elif string.upper(command[0]) == "DUMP":
				#Build the xml string to perform the dump
				#Dump the contents of the context
				#Format the data so it matches with the apply function
				pass
			
			elif (string.upper(command[0]) == "QUIT") or (string.upper(command[0]) == "EXIT"):
				return
			
			else:
				print "Command not recognized."
			
			
			
def print_help():
	print '''
	root		Display the root tag of the contruct
	back		Go back one step in the xpath context
	view		List the available children in the context
	context		Show the current context 
	help		Display help and commands
	dump		Display the items in the current context
	quit		Duh
	'''
	
			
			
			
