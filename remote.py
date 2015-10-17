"""
This module is for remote administration and investigation of hosts within a windows network
Dependencies here are Sys Internals Tools

This module should accompany the Artilery Collection for the PENTRN program.  
These wrappers are used to perform quick, responsive actions on remote and local systems
when responding to confirmed and suspected security incidents.  

ASPIRATIONS:
   Change the proxy remotely
   Change the account to -> "DSFCUSECOPS::9iVyhXp)ddN_FM!eaWvq?d5?k7:J["


Programmer: q0m
Date: April 4, 2012
Description:  Word up mofo.  Don't sleep on the offensive.  

"""

import os
import string
import random
import time

def waitkill():
	time.sleep(3300)
	os.system("pskill communicator")
	time.sleep(900)
	os.system("start communicator")
	waitkill()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

randomfilename= id_generator()
filesave = " > " + str(randomfilename) + ".rsc"
filesave_cont = " >> " + str(randomfilename) + ".rsc"
#print filesave
#print filesave_cont

def index():
	import remote
	for item in dir(remote):
		print item
		
def nuke(host):
	nuke_string = "shutdown /m " + host + " /r /f /t 1"
	print nuke_string
	os.system(nuke_string)

def view_proxy(host):
	registry_string ="psexec \\\\" + host + " reg query \"HKCU\\SOFTWARE\\MICROSOFT\\Windows\\CurrentVersion\\Internet Settings\""
	print registry_string
	os.system(registry_string)
	
def update_proxy(host):
	add_reg_string = "psexec \\\\" + host + " reg add \"HKCU\\SOFTWARE\\WINDOWS\\CurrentVersion\\Internet Settings\" /v ProxyEnable /t reg_dword /d 00000001 /f"
	print add_reg_string
	os.system("psexec \\\\" + host + " reg add \"HKCU\\SOFTWARE\\WINDOWS\\CurrentVersion\\Internet Settings\" /v ProxyEnable /t reg_dword /d 00000001 /f")
	os.system("psexec \\\\" + host + " reg add \"HKCU\\SOFTWARE\\WINDOWS\\CurrentVersion\\Internet Settings\" /v ProxyServer /t reg_sz /d proxyaddress:8080 /f")
	
def view_exe(host):
	exe_string = "reg query HKLM /s /d /f \"C:\* *.exe\" | find /I \"C:\\v\" | find /V \"\"\"\""
	print exe_string
	os.system("psexec \\\\" + host + " " + exe_string)

def remote_shell(host):
    os.system("psexec \\\\" + host + " cmd.exe")

def install_date(host):
    '''grabs the install date of the operating system'''
    os.system("psexec \\\\" + " wmic os getinstalldate")

def list_startups(host):
    '''grabs the startup applications on the host'''
    execute_string = "psexec \\ppr-lem01 wmic startup list brief"
    os.system("psexec \\\\" + host + " wmic startup list brief")

def list_installed(host):
    execute_string = "psexec \\ppr-lem01 wmic product list brief"
    os.system("psexec \\\\" + host + " wmic product list brief")

def get_mac(host):
    os.system("psexec \\\\" + host + " wmic nic get macaddress")

def usb_history(host):
    #print "reg query \\\\" + host + "\\HKLM\\SYSTEM\\CurrentControlSet\\Enum\USBSTOR"
    os.system("reg query \\\\" + host + "\\HKLM\\SYSTEM\\CurrentControlSet\\Enum\USBSTOR")

def list_users(host):
    os.system("psloggedon \\\\" + host)

def list_services(host):
    os.system("psexec \\\\" + host + " wmic service list brief")

def list_processes(host):
    #os.system("psexec \\\\" + host + " wmic process get Name, Executable path, CommandLine, ProcessID /format:list")
    os.system("psexec \\\\" + host + " wmic process list brief")

def list_netstat(host):
	os.system("psexec \\\\" + host + " netstat -ano " + filesave)

def investigate(host):
	list_startups(host + filesave)
	list_installed(host + filesave_cont)
	get_mac(host + filesave_cont)
	usb_history(host + filesave_cont)
	list_users(host + filesave_cont)
	list_services(host + filesave_cont)
	list_processes(host + filesave_cont)
	os.system("notepad.exe " + filesave)


if __name__=='__main__':
	print "Remote Access Module for Incident Response"
	print "Programmer: q0m"
	print "cmdjunkie@gmail.com"
	print __builtins__
	
