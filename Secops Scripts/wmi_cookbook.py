"""WMI Cookbook Module
Programmer: Brent E. Chambers
Date: August 1, 2011
Purpose: To wrap up some WMI examples into a usable module
Eventually putting code of this nature into my DS_LivePosture server
"""
global remote_host
global c
remote_host = "10.1.121.129"
import wmi
c = wmi.WMI(remote_host)


def definehost():
	remote_host = raw_input("Enter remote host: ")
	

def all_notepad_processes(c):
	for process in c.Win32_Process (name="outlook.exe"):
		print process.ProcessId, process.Name
		

def show_autoservices_off(c):
	stopped_services = c.Win32_Service (StartMode="Auto", State="Stopped")
	if stopped_services:
		for s in stopped_services:
			print s.Caption, "service is not running"
	else:
		print "No auto services stopped"
		
def show_percent_free_space(c):
	for disk in c.Win32_LogicalDisk (DriveType=3):
		print disk.Caption, "%0.2f%% free" % (100.0 * long (disk.FreeSpace) / long (disk.Size))
		
def show_notepad_test(c):
	import wmi
	filename = r"c:\rose.txt"
	process = c.Win32_Process
	process_id, result = process.Create (CommandLine="notepad.exe " + filename)
	#process_id, result = process.Create (CommandLine = "echo \"this is how we do it\" > how.txt | notepad.exe how.txt")
	watcher = c.watch_for (
		notification_type="Deletion",
		wmi_class="Win32_Process",
		delay_secs=1,
		ProcessId=process_id
	)

	watcher ()
	print "This is what you wrote:"
	print open (filename).read ()
	
	
def show_new_printjobs(c):
	print_job_watcher = c.Win32_PrintJob.watch_for (
	notification_type="Creation",
	delay_secs=1
	)

	while 1:
		pj = print_job_watcher ()
		print "User %s has submitted %d pages to printer %s" % (pj.Owner, pj.TotalPages, pj.Name)
		

def reboot_machine(c):
	c = wmi.WMI (computer=other_machine, privileges=["RemoteShutdown"])
	os = c.Win32_OperatingSystem (Primary=1)[0]
	os.Reboot ()
	
def show_ipandmac(c):
	for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
		print interface.Description, interface.MACAddress
	for ip_address in interface.IPAddress:
		print ip_address
	print
	
def startup_processes(c):
	for s in c.Win32_StartupCommand ():
		print "[%s] %s <%s>" % (s.Location, s.Caption, s.Command)
	
def event_log_errors(c):
	c = wmi.WMI (privileges=["Security"])

	watcher = c.watch_for (
	notification_type="Creation",
	wmi_class="Win32_NTLogEvent",
	Type="error"
	)
	while 1:
		error = watcher ()
		print "Error in %s log: %s" %  (error.Logfile, error.Message)
	# send mail to sysadmin etc.
	
def list_registry_key(c):
	r = wmi.Registry ()
	result, names = r.EnumKey (
	hDefKey=_winreg.HKEY_LOCAL_MACHINE,
	sSubKeyName="Software"
	)
	for key in names:
		print key
	
def add_registry_key(c):
	r = wmi.Registry ()
	result, = r.CreateKey (
		hDefKey=_winreg.HKEY_LOCAL_MACHINE,
		sSubKeyName=r"Software\TJG"
	)
	
def add_registry_value(c):
	r = wmi.Registry ()
	result, = r.SetStringValue (
	hDefKey=_winreg.HKEY_LOCAL_MACHINE,
	sSubKeyName=r"Software\TJG",
	sValueName="ApplicationName",
	sValue="TJG App"
	)
	
	
def create_new_IIS_site(c):
	#
	# Could as well be achieved by doing:
	#  web_server = c.IISWebService (Name="W3SVC")[0]
	#
	for web_server in c.IIsWebService (Name="W3SVC"):
		break

	binding = c.new ("ServerBinding")
	binding.IP = ""
	binding.Port = "8383"
	binding.Hostname = ""
	result, = web_server.CreateNewSite (
		PathOfRootVirtualDir=r"c:\inetpub\wwwroot",
		ServerComment="My Web Site",
		ServerBindings= [binding.ole_object]
)
	

def show_shared_drives(c):
	for share in c.Win32_Share ():
		print share.Name, share.Path
		
		
def show_print_jobs(c):
	for printer in c.Win32_Printer ():
		print printer.Caption
	for job in c.Win32_PrintJob (DriverName=printer.DriverName):
		print "  ", job.Document
	print

def show_disk_partitions(c):
	for physical_disk in c.Win32_DiskDrive ():
		for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
			for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
				print physical_disk.Caption, partition.Caption, logical_disk.Caption
	
	
def install_msi(c):
	c.Win32_Product.Install (
	PackageLocation="c:/temp/python-2.4.2.msi",
	AllUsers=False
	)


def connect_as(c):
	connection = wmi.connect_server (
	server="other_machine",
	user="tim",
	password="secret"
	)
	c = wmi.WMI (wmi=connection)

	#
	# Using wmi module at least 1.0rc3
	#
	c = wmi.WMI (
		computer="other_machine",
		user="tim",
		password="secret" )

def schedule_job(c):
	c = wmi.WMI ()
	one_minutes_time = datetime.datetime.now () + datetime.timedelta (minutes=1)
	job_id, result = c.Win32_ScheduledJob.Create (
		Command=r"cmd.exe /c dir /b c:\ > c:\\temp.txt",
		StartTime=wmi.from_time (one_minutes_time)
	)
	print job_id

	for line in os.popen ("at"):
		print line


def run_minimized(c):
	SW_SHOWMINIMIZED = 1

	c = wmi.WMI ()
	startup = c.Win32_ProcessStartup.new (ShowWindow=SW_SHOWMINIMIZED)
	pid, result = c.Win32_Process.Create (
	CommandLine="notepad.exe",
	ProcessStartupInformation=startup
	)
	print pid
	
def find_drive_types(c):
	DRIVE_TYPES = {
	0 : "Unknown",
	1 : "No Root Directory",
	2 : "Removable Disk",
	3 : "Local Disk",
	4 : "Network Drive",
	5 : "Compact Disc",
	6 : "RAM Disk"
	}

	c = wmi.WMI ()
	for drive in c.Win32_LogicalDisk ():
		print drive.Caption, DRIVE_TYPES[drive.DriveType]
