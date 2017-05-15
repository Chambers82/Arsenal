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
	# -------------------- Don't scan for ports, scan for vulns!!! ------------------------

	def enum_http(self, targets):
		cmd = "nmap -n -sV -Pn -p 80,8080,9090 --script=http-enum,http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-robots.txt,http-iis-webdav-vuln,http-vuln-cve2009-3960,http-vuln-cve2010-0738,http-vuln-cve2011-3368,http-vuln-cve2012-1823,http-vuln-cve2013-0156,http-waf-detect,http-waf-fingerprint,ssl-enum-ciphers,ssl-known-key -oA http_enumeration " + targets
		print cmd
		os.system(cmd)

	def enum_ftp(self, targets):
		cmd = "nmap -sV -Pn -n -p 21 --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 -oA ftp_enumeration " + targets
		print cmd
		os.system(cmd)
		
	def enum_mssql(self, targets):
		cmd = "nmap -n -sV -sT -Pn -p 1433 --script=ms-sql-brute,ms-sql-config,ms-sql-dac,ms-sql-dump-hashes,ms-sql-empty-password,ms-sql-hasdbaccess,ms-sql-info,ms-sql-query,ms-sql-tables,ms-sql-xp-cmdshell -oA mysql_enumeration" + targets
		print cmd
		os.system(cmd)

	def enum_mysql(self, targets):
		cmd = "nmap -n -sV -sT -Pn -p 3306 --script=mysql-empty-password,mysql-vuln-cve2012-2122 -oA mysql_enumeration " + targets
		print cmd
		os.system(cmd)

	def enum_ntp(self, targets):
		cmd = "nmap -n -Pn -sU -p 123 --script=ntp-info -oA ntp_enumeration " + targets 
		print cmd
		os.system(cmd)
		
	def enum_oracle(self, targets):
		cmd = "nmap -n -sV -sT -Pn -p 1521 --script=oracle-brute.nse,oracle-brute-stealth.nse,oracle-enum-users.nse,oracle-sid-brute -oA oracle_enum " + targets
		print cmd
		os.system(cmd)
		
	def enum_rdp(self, targets):
		cmd = "nmap -Pn -sV -p 3389 --script=rdp-enum-encryption,rdp-vuln-ms12-020.nse -oA rdp_enumeration "  + targets
		print cmd
		os.system(cmd)
		
	def enum_smb(self, targets):
		cmd = "nmap -n -sV -sU -sS -Pn -pT:139,445,U:137 --script=nbstat,smb-enum-domains,smb-enum-groups,smb-enum-processes,smb-enum-sessions,smb-ls,smb-mbenum,smb-os-discovery,smb-print-text,smb-security-mode,smb-server-stats,smb-system-info,smb-vuln-conficker,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067,smb-vuln-ms10-054,smb-vuln-ms10-061 -oA smb_enumeration %s" + targets
		print cmd
		os.system(cmd)
		
	def enum_smtp(self, targets):
		cmd = "nmap -n -sV -sT -Pn -p 25,465,587 --script=smtp-commands,smtp-vuln-cve2010-4344,smtp-vuln-cve2011-1764 -oA smtp_enumeration %s" + targets
		print cmd
		os.system(cmd)
		
	def enum_snmp(self, targets):
		cmd = "nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes " + targets
		print cmd
		os.system(cmd)
		
	def enum_vnc(self, targets):
		cmd = "nmap -n -sV -sT -Pn -p 5900 --script=realvnc-auth-bypass,vnc-brute,vnc-info --script-args=unsafe=1 -oA " + targets + "/" + targets + "_vnc " + targets
		print cmd
		os.system(cmd)

	def fingerprint_web(self, target):
		cmd = "xprobe2 -v -p tcp:80:open " + target + " > http_fingerprint.rsc"
		os.system(cmd)
		cmd = "xprobe2 -v -p tcp:443:open " + target + " > https_fingerprint.rsc"
		os.system(cmd)

	def enum_snmp_public(self, target, strang="public"):
		cmd = "snmpget -v 1 -c " + strang + " " + target + " > snmpget_"+target+".rsc"
		os.system(cmd)
		cmd = "snmpwalk -v 1 -c " + strang + " " + target + " > snmpwalk_"+target+".rsc"
		os.system(cmd)
		cmd = "snmpbulkwalk -v2c -c " + strang + " -Cn0 -Cr10 " + target + " > snmpbulk_"+target+".rsc"
		os.system(cmd)

	def identify_waf(self, targets):
		cmd = "nmap -p 80,443 --script=http-waf-detect,http-waf-fingerprint -oA waf_ident " + targets
		print cmd
		os.system(cmd)

	def nikto_scan(self, target, port):
		cmd = "nikto -host " + target + " -p " + port + " -C all | tee " + target + "_nikto_scan"
		print cmd
		os.system(cmd)