#Programmer: Brent E. Chambers
#Date: 7/28/2014
#Filename: red_team.py
#Description:  Module collection to aide in quickly identifying the threat landscape of target object
#Takes a second to generate and download the resource files, but it's worth it for the quick
#Analysis capabilities.  
'''
# NOTES
1) All resource content is based on the default format of the Nessus reports produced after a nessus scan.  
--Meaning to get updated information, you have to manually 
2) After each scan, FIVE reports need to be created and placed in the VM directory:
	Server_Asset_Zone_July.csv
	Branch_Office_Asset_Zone_July.csv
	DMZ_Asset_Zone_July.csv
	User_Asset_Zone_July.csv

3) Resource files create problems because of the first three columns: PluginID, CVE, and CVSS.  If these can be eliminated, duplicates will be reduced 
and reporting will be far more accurate.  Unfortunately, taking them out would mess up the row mappings, this can be fixed however with some clever import 
techniques. 

4.) Figure out a way to progamatically remove the first three columns and see if that makes a difference when reporting

5.) Add the remaining commands to the interactive mode

6.) Expand the functionality by adding search

7.) Expand the reporting capability by allowing the user to export to a web report (think interactive pyreports) yeah!

8.) Brainstorm how using this pentest console, Internal pentesting can be improved and made easier

9.) How to separate by zone, not business system (too hard to keep track of)


vulnrecords.py commands (brainstorm)
SEARCH
	search_vulns()         searchs vulnerabilities for a given string -- broken becasue it doesn't return everything :(
	search_vuln_descript() searches vulnerability descriptions for a given string - works, but it's ugly
	search_ports()         searchs for vulnerabilities based on provided port number (WORKS!) || separate the dump from the export
	search_hostd(string)   searches hosts for a given string and returns a list of hostnames || (WORKS!!) very nice
	host_search()          searches for a specific host and dumps it's vuln data
	
MGMT
	manageDir()            manages the resource directory by renaming and moving some files around, needs tracking and trending
	
LISTS
	dump_ips()             dumps all IPs that don't resolve
	dump_hosts()           dumps all hosts in the resource file
	dump_group_assets()    dumps a resolved list of hosts and assets in a supplied group
	
	
	
BREAK DOWN BY ASSET ZONE
THEN BREAK DOWN BY BUSINESS SYSTEM (CORELATION)
	
	
*****************Resource File Update Procedures******************

1. Log in to the Nessus Console
2. Access the appropriate Asset Zone scan results (DMZ | Server | User | Branch)
3. Export the file to CSV 
4. Save over the existing file and add the current month.
e.g.  C:\python27\vm\User_Asset_Zone_Sept.csv
5. Change the resource file in the source \|/  

******************************************************************
	

'''

#Vulnrecords Imports
import csv
#import core, 
import socket, string
from sets import Set
import os
import sys


#Manadatory Remove Dupes Function
def remove_dupes(list):
	uniqueList = Set(list)
	return uniqueList


# Basic vulnscan class for pulling vulnerability records
class VulnScan:
	
	current_zone = ""
	server = "c:\\python27\\vm\\Server_Asset_Zone_Aug.csv"
	branch = "c:\\python27\\vm\\Branch_Office_Asset_Zone_Aug.csv"
	dmz    = "c:\\python27\\vm\\DMZ_Asset_Zone_Aug.csv"
	user   = "c:\\python27\\vm\\User_Asset_Zone_Aug.csv"

	def __init__(self):  #defaults to the server asset zone
		self.current_zone = "c:\\python27\\vm\\Server_Asset_Zone_Aug.csv"

##### CHANGING THE ENVIRONMENT

	def change_zone(self, zone):	#function to change the asset zone      COMMAND: zone [arg]
		if zone.upper() == "SERVER":
			self.current_zone = self.server
		elif zone.upper() == "BRANCH":
			self.current_zone = self.branch
		elif zone.upper() == "DMZ":
			self.current_zone = self.dmz
		elif zone.upper() == "USER":
			self.current_zone = self.user
		else:
			print "Zone specification error."
		print "Current zone changed to: ", self.current_zone
		
	def print_zone(self):
		print "Current zone: ", self.current_zone

#####  GETTING HOST DATA

	def export_zone_hosts(self):		#function to export the hosts in the current asset zone  CMD: hosts
	#dump all hosts in the given asset zone
		scan = open(self.current_zone)
		master = []
		hosts = []
		scanreader = csv.reader(scan)
		for row in scanreader:
			master.append(row[4])
		master_hosts = remove_dupes(master)
		return master_hosts
	
	def dump_zone_hosts(self):		#function to merely print hosts in the current asset zone   CMD: hosts
		hosts = self.export_zone_hosts()
		for item in hosts:
			print item

#####	GETTING VULNERABILITY DATA

	def export_zone_vulns(self):  #function to export the vulnerabilities in the current asset zone   CMD: vulns
		scan = open(self.current_zone)
		master = []
		hosts = []
		scanreader = csv.reader(scan)
		for row in scanreader:
			master.append((row[4], row[7]))
		master.sort()
		master_hosts = remove_dupes(master)
		return master_hosts
		
	def dump_zone_vulns(self):	# function to print the vulnerabilities in the current asset zone CMD: vulns
		vulns = self.export_zone_vulns()
		for item in vulns:
			print item[0], " "*(35-int(len(item[0]))), item[1]
			
	def export_zone_vulns_impact(self, impact): #function to export vulns in the current asset zone of the specified impact level -- CMD: "exporti [arg]"
		scan = open(self.current_zone)
		master = []
		hosts = []
		scanreader = csv.reader(scan)
		for row in scanreader:
			if string.upper(row[3]) == string.upper(impact):
				master.append((row[4]+":"+row[6], row[7]))
			else:
				pass
		master.sort()
		master_hosts = remove_dupes(master)
		return master_hosts
	
	def dump_zone_vulns_impact(self, impact):  #function to print the vulns in the current asset zone of the specified impact level -- CMD: vulns [arg]
		scan = open(self.current_zone)
		master = []
		hosts = []
		scanreader = csv.reader(scan)
		for row in scanreader:
			if string.upper(row[3]) == string.upper(impact):
				master.append((row[4]+":"+row[6], row[7]))
			else:
				pass
		master.sort()
		sorted_results = []
		master_hosts = remove_dupes(master)
		for item in master_hosts:
			sorted_results.append(item)
		sorted_results.sort()
		for item in sorted_results:
			print item[0], " "*(40-int(len(item[0]))), item[1]

	
		
		
		
#### #GETTING HOST SEARCH DATA

	def search_hosts(self, host):		#raw text string search for the hosts to group systems
		scan = open(self.current_zone)
		master = []
		deliver = []
		reader = csv.reader(scan)
		for row in reader:
			master.append(row[4])
		unq_master = [t for t in master if host in t] #performs raw string search
		unique_master = remove_dupes(unq_master)
		for item in unique_master:
			deliver.append(item)
		deliver.sort()
		return deliver
	
	def search_port(self, portnum):		#Performs a port search, matching only service detection
		scan = open(self.current_zone)
		master_ports = []
		master_hosts = []
		master_socket = []
		master = []
		description = []
		reader = csv.reader(scan)
		for row in reader:
			if ((row[6] == portnum) and (row[3] == "None") and ("Detection" in string.split(row[7]))):
			#if ((row[6] == portnum) and (row[3] == "None") and (row[7] <> "Nessus SYN scanner" or row[7] <> "Netstat Portscanner (WMI)")):
				master_socket.append((row[4], row[6], row[7]))
		unique_sockets = remove_dupes(master_socket)
		for item in unique_sockets:
			print item[1], " "*(7-int(len(item[1]))), item[0], " "*(41-(int(len(item[1]))+int(len(item[0])))), `item[2]`
			master.append((item[1], item[0], `item[2]`))
		print "Host count: ", len(unique_sockets)
		return master
			
	def host_vquery(self, host):			#Returns Critical, High, Medium and Low vulnerabilties of the given host
		scan= open(self.current_zone)
		master = []
		deliver = []
		buffer = []
		reader = csv.reader(scan)
		for row in reader:
			if ((row[4] == host and row[3] <> "None")):
			#if string.upper(row[4]) == string.upper(string.split(host, ".")):
				master.append((row[3], row[6], row[7]))
		unique_master = remove_dupes(master)
		for item in unique_master:
			buffer.append((item[0], item[1], item[2]))
		buffer.sort()
		for item in buffer:
			print item[0], "\t\t", item[1], "\t\t", item[2]
			#deliver.append((item[0], item[1], item[2]))
			#deliver.sort()
		return buffer

	def host_squery(self, host):			#Display open services on the supplied host, no duplicates
		scan = open(self.current_zone)
		master = []
		deliver = []
		buffer = []
		reader = csv.reader(scan)
		for row in reader:
			if ((row[4] == host) and (row[3] == "None") and ("Detection" in string.split(row[7]))):#and (row[7] == "Service Detection")):
			#if ((row[4] == host) and (row[3] <> "None") and (row[7] == "Service Detection")):
				master.append((row[3], row[6], row[7]))
		unique_master = remove_dupes(master)
		for item in unique_master:
			buffer.append((item[0], item[1], item[2]))
		buffer.sort()
		for item in buffer:
			print item[0], "\t\t", item[1], "\t\t", item[2]
		return buffer
		
	def stats(self):
		scan = open(self.current_zone)
		master = []
		deliver = []
		impact_levels = []
		critical_hosts = []
		reader = csv.reader(scan)
		
		# Group all Critical_Levels | Hostnames | Title
		for row in reader:
			master.append((row[3], row[4], row[7]))
		unique_master = remove_dupes(master)  # Unique list of findings for that zone
		
		#Pull the impact level statistics
		for item in unique_master:
			impact_levels.append(item[0])
			critical_hosts.append(item[1])

		#Pull the host level statistics
		Critical_hosts = []
		High_hosts = []
		Medium_hosts = []
		Low_hosts = []
		for item in unique_master:
			if item[0] == "Critical":
				Critical_hosts.append(item[1])
			elif item[0] == "High":
				High_hosts.append(item[1])
			elif item[0] == "Medium":
				Medium_hosts.append(item[1])
			elif item[0] == "Low":
				Low_hosts.append(item[1])
			else:
				pass
		cHosts = remove_dupes(Critical_hosts)
		hHosts = remove_dupes(High_hosts)
		mHosts = remove_dupes(Medium_hosts)
		lHosts = remove_dupes(Low_hosts)
		host_count = self.export_zone_hosts()
		
		print "\n"
		print "[+] Vulnerability statistics for asset zone: " + string.upper(string.split(string.split(self.current_zone, "\\")[-1], "_")[0])
		print "Criticals: ", " "*(25-int(len("Criticals:"))), impact_levels.count("Critical")
		print "Highs: ", " "*(25-int(len("Highs:"))), impact_levels.count("High")
		print "Mediums: ", " "*(26-int(len("Mediums: "))), impact_levels.count("Medium")
		print "Lows: ", " "*(25-int(len("Low: "))), impact_levels.count("Low")
		print "\n\n"
		print "[+] Host statistics for asset zone: " + string.upper(string.split(string.split(self.current_zone, "\\")[-1], "_")[0])
		print "TOTAL HOSTS: ", " "*(25-int(len("Total hosts: "))), len(host_count)
		print "Hosts w/ criticals: ", " "*(25-int(len("Hosts w/ criticals: "))), len(cHosts), len(cHosts)/len(host_count)
		print "Hosts w/ highs: ", " "*(25-int(len("Hosts w/ highs: "))), len(hHosts), len(hHosts)/len(host_count)
		print "Hosts w/ mediums: ", " "*(25-int(len("Hosts w/ mediums: "))), len(hHosts), len(mHosts)/len(host_count)
		print "Hosts w/ lows: ", " "*(25-int(len("Hosts w/ lows: "))), len(lHosts), len(lHosts)/len(host_count)
		
	
	def all_stats(self):
		print "Dumping all stats..."
		self.change_zone("DMZ")
		self.stats()
		self.change_zone("Server")
		self.stats()
		self.change_zone("Branch")
		self.stats()
		self.change_zone("User")
		self.stats()
		
		


#### INTERACTIVE MODE

def console():
	print r"  DSFCU        _          _  IT Security Operations _     "
	print r" _ __  ___ _ _| |_ ___ __| |_   __ ___ _ _  ___ ___| |___ "
	print r"| '_ \/ -_) ' \  _/ -_|_-<  _| / _/ _ \ ' \(_-</ _ \ / -_)"
	print r"| .__/\___|_||_\__\___/__/\__| \__\___/_||_/__/\___/_\___|"
	print r"|_|                                          version 1.0  "
	
	vulns = VulnScan()
	cmd = raw_input("\ndsvulns> ")
	
	while string.upper(cmd) <> "QUIT" or "EXIT" :
		cmd = raw_input("\ndsvulns> ")
		command = string.split(cmd, " ")
		if string.upper(command[0]) == "ZONE" and len(command) <= 1:
			vulns.print_zone()
		elif string.upper(command[0]) == "ZONE" and len(command) >= 2:
			vulns.change_zone(command[1])
		elif string.upper(command[0]) == "SEARCH" and len(command) <= 1:
			print "Syntax: search [host|port]"
		
		elif string.upper(command[0]) == "SEARCH" and len(command) >= 2:
			try:
				int(command[1])		#tries to convert it to an integer, if not, searches for a hostname
				collect = vulns.search_port(command[1])
				
			except:
				collect = vulns.search_hosts(command[1])
				
			
		elif string.upper(command[0]) == "VQUERY" and len(command) <= 1:
			print "\nHost vulnerability query. \nSyntax: vquery [host]"
		
		elif string.upper(command[0]) == "VQUERY" and len(command) >= 2:
			collect = vulns.host_vquery(command[1])
			collect.sort()
		
		elif string.upper(command[0]) == "SQUERY" and len(command) <= 1:
			print "Host service query. \nSyntax: squery [host]"
		
		elif string.upper(command[0]) == "SQUERY" and len(command) >= 2:
			collect = vulns.host_squery(command[1])
			collect.sort()
			
		elif string.upper(command[0]) == "CLEAR":
			os.system("cls")
		
		elif (string.upper(command[0]) == "QUIT" or string.upper(command[0]) == "EXIT"):
			print "DSFCU Red Team Penetration Testing Module - 2014"
			print "\nCopyright 2014 Cocksure Security LLC."
			print "\nSupport the Free Information Movement.\n Peace."
			return
		elif (string.upper(command[0]) == "EXPORT"):			#Take a cue from pyreports and generate an HTML, CSV, XML, or what have you... could be tight
			#Export the last ran list to do something.  For now, just print it
			try:
				for item in collect:
					print item
				return collect
				#this should ensure that all commands can be exported and there's no repetition for the console output
			except:
				print "No vulnerability content available."
		
		elif (string.upper(command[0]) == "HOSTS"):
			vulns.dump_zone_hosts()
		
		elif (string.upper(command[0]) == "VULNS"):
			try:
				vulns.dump_zone_vulns_impact(command[1])
				
			except:
				print "Dumping all vulnerabilities..."
				vulns.dump_zone_vulns()
				
		elif (string.upper(command[0]) == "EXPORTI"):
			try:
				collect = vulns.export_zone_vulns_impact(command[1])
			except:
				print "Export content unavailable."		
		
		elif (string.upper(command[0]) == "STATS"):
				try:
					test = command[1]
					if test == "all":
						vulns.all_stats()
				except:
					vulns.stats()
			
		elif (string.upper(command[0]) == "HELP"):
			print "Current commands: "
			print help_file
		else:
			print "Command not recognized."
		
			
	
#" "*(35-int(len(row[0]))),

# This module needs a stats command so you can quickly generate statistics on the zones that were assessed
#


#to celebrate!
'''
	print r"  DSFCU        _          _  IT Security Operations _     "
	print r" _ __  ___ _ _| |_ ___ __| |_   __ ___ _ _  ___ ___| |___ "
	print r"| '_ \/ -_) ' \  _/ -_|_-<  _| / _/ _ \ ' \(_-</ _ \ / -_)"
	print r"| .__/\___|_||_\__\___/__/\__| \__\___/_||_/__/\___/_\___|"
	print r"|_|                                          version 1.0  "
'''


help_file = """

Red Team Penetration Testing console is an interactive program that allows you to quickly identify vulnerable services and network devices.  
This program was written by Brent E. Chambers (q0m).  



Management Commands
-------------------
  zone    	           Show current zone
  zone [arg] 	           Switch to different zone [server|branch|dmz|user]
  stats [all]              Prints vulnerability statistics for the current asset zone

 
Vuln Commands
-------------
  vulns                    Print all vulns in the current asset zone
  vulns [arg]	           Print all vulns in the current asset zone matching the impact level provided [Critical|High|Medium|Low|Info]
  exportv [arg]            Export all vulnerabilities in the current asset zone


Host Commands
-------------
  hosts [arg]	           Print all hosts in the current asset zone
  export_hosts             Export all hosts in current asset zone
  search [host|port]       Searches the current asset zone for records matching the given host or port number
  vquery [host]            Displays the discovered vulnerabilities for the supplied host in the current zone
  squery [host]            Displays the discovered vulnerabilities for the supplied host in the current zone


Attack Intelligence
-------------------
  (Coming Soon)
"""
