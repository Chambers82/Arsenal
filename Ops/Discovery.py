#Programmer: Brent E. Chambers
#Date: 3/7/2017
#Filename: Discovery.py
#Description:

descript = """
Discovery module that consolidates techniques for network and vulnerability discovery.
"""


import os
import xmltodict
from sets import Set


global RESULTS_FILE
RESULTS_FILE = './nmap_results.xml'


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

class discovery:
    host = ''
    port = ''
    results = RESULTS_FILE

    def __init__(self):
	pass

    def common_services(self, targets):
	cmd = "nmap -sS -sU  -p U:53,T:22,T:23,T:25,T:79,T:80,134-139 " + targets + " -oX common_services.xml"
	print cmd
	os.system(cmd)

    def enum_http(self, targets):
	cmd = "nmap --script http-enum,http-headers,http-methods,http-php-version -p80 " + targets + " -oX http_enum.xml"
	print cmd
	os.system(cmd)

    def windows_vuln_ports(self, targets):
	cmd = "nmap -sS -sU -p T:25,U:69,T:80,134-139,T:445,1025,1434,2745,3127-3198,4899,5000,6129 " + targets + " -oX windows_vulns.xml"
	print cmd
	os.system(cmd)

    def linux_vuln_ports(self, targets):
	cmd = "nmap -sS -sU -p 21,20,69,23,T:25,110,143,513,514,80 " + targets + " -oX linux_vulns.xml"
	print cmd
	os.system(cmd)

    def web_vuln_scan_setup(self):
	cmd = "cd /usr/share/nmap/scripts/"
	os.system(cmd)
	cmd = "wget http://www.computec.ch/projekte/vulscan/download/nmap_nse_vulscan-2.0.tar.gz && tar xzf nmap_nse_vulscan-2.0.tar.gz"
	os.system(cmd)

    def web_vuln_scan(self, targets):
	cmd = "nmap -vv -sS -sV --script=vulscan/vulscan.nse " + targets + " -oN vulnscan_results.n"
	os.system(cmd)
	cmd = "nmap -vv -sS -sV --script=vulscan/vulscan.nse -script-args vulscandb=scipvuldb.csv -p80 " + targets + " -oN vulnscabdb_results.n"
	os.system(cmd)
	cmd = "nmap -vv -PN -sS -sV --script=vulscan -script-args vulscancorrelation=1 -p80 " + targets + " -oN correlation_results.n"
	os.system(cmd)		
	cmd = "nmap -vv -sV --script=vuln " + targets + " -oN vuln_resulsts.n"
	os.system(cmd)
	cmd = "nmap -vv -PN -sS -sV --script=all -script-args vulscancorrelation=1 " + targets + " -oN vuln_scan_all_results.n"
	os.system(cmd)

    def fingerprint_web(self, target):
	cmd = "xprobe2 -v -p tcp:80:open " + target + " > http_fingerprint.rsc"
	os.system(cmd)
	cmd = "xprobe2 -v -p tcp:443:open " + target + " > https_fingerprint.rsc"
	os.system(cmd)

    def enum_snmp(self, target, strang="public"):
	cmd = "snmpget -v 1 -c " + strang + " " + target + " > snmpget_"+target+".rsc"
	os.system(cmd)
	cmd = "snmpwalk -v 1 -c " + strang + " " + target + " > snmpwalk_"+target+".rsc"
	os.system(cmd)
	cmd = "snmpbulkwalk -v2c -c " + strang + " -Cn0 -Cr10 " + target + " > snmpbulk_"+target+".rsc"
	os.system(cmd)

    def identify_waf(self, targets):
	cmd = "nmap -p 80,443 --script=http-waf-detect " + targets + " > waf_detect_"+targets+".rsc"
	os.system(cmd)
	cmd = "nmap -p 80,443 --script=http-waf-fingerprint " + targets + " > waf_fingerprint_"+targets+".rsc"
	os.system(cmd)

    def smart_nmap_scan(self, network):
	cmd = "nmap -sn -oG Discovery.gnmap " + network
	os.system(cmd)
	cmd = "grep \"Status: Up\" Discovery.gnmap | cut -f 2 -d ' ' > LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -sS -Pn -oG TopTCP -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -sU -Pn -oN TopUDP -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -sS -Pn --top-ports 3674 -oG 3674 -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -sS -Pn -p 0-65535 -oN FullTCP -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "grep \"open\" FullTCP|cut -f 1 -d ' ' | sort -nu | cut -f 1 -d '/' |xargs | sed 's/ /,/g'|awk '{print \"T:\"$0}'"
	os.system(cmd)
	#cmd = "grep \"open\" FullUDP|cut -f 1 -d ' ' | sort -nu | cut -f 1 -d '/' |xargs | sed 's/ /,/g'|awk '{print "U:"$0}'"
	#os.system(cmd)
	cmd = "nmap -sV -Pn -oG ServiceDetect -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -O -Pn -oG OSDetect -iL LiveHosts.txt"
	os.system(cmd)
	cmd = "nmap -O -sV -Pn -p U:53,111,137,T:21-25,80,139,8080 -oG OS_Service_Detect -iL LiveHosts.txt"
	os.system(cmd)


