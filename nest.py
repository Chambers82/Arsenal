import webbrowser
from sets import Set


def remove_dupes(jaja):
	uniqueList = Set(jaja)
	return uniqueList

def cp_collect(): #copy and paste a list of items and it will kick it out as a unique list
	master = []
	while 1:
		host = raw_input("Item: ")
		if host == "done":
			unique_master = remove_dupes(master)
			return unique_master
		master.append(host)
	unique_master = remove_dupes(master)
	return unique_master
	
def httpServers(jaja):
	file = open("HTTPservers.htm", "w")
	#create the header file
	opener = "<html><head></head><body>"
	file.write(opener)
	file.write("<h3> HTTP web servers </h3>")
	#feed in the web server list
	for line in jaja:
		url = "http://" + line + ":80" + "</a>\n"
		link = "<a href=\"http://" + line + ":80" + "\">" + url + "</a>"
		file.write(link + "</br>")
	#close the html file
	closer = "</body></html>"
	file.write(closer)
	file.close()
	webbrowser.open("HTTPservers.htm")


def httpsServers(jaja):
	file = open("HTTPSservers.htm", "w")
	#create the header file
	opener = "<html><head></head><body>"
	file.write(opener)
	file.write("<h3> HTTP web servers </h3>")
	#feed in the web server list
	for line in jaja:
		url = "https://" + line + ":443" + "</a>\n"
		link = "<a href=\"https://" + line + ":443" + "\">" + url + "</a>"
		file.write(link + "</br>")
	#close the html file
	closer = "</body></html>"
	file.write(closer)
	file.close()
	webbrowser.open("HTTPSservers.htm")
	
	
def httpServer_collect():
	ipaddresses = cp_collect()
	grab_ips = []
	for item in ipaddresses:
		grab_ips.append(item)
	webbrowser.open_new("http://"+grab_ips[0])
	ip_addys = grab_ips[0:]
	for item in ip_addys:
		url = "http://" + item
		webbrowser.open_new_tab(url)
	#httpServers(ipaddresses)
	
def httpServer_collect_open():
	ipaddresses = cp_collect()
	webbrowser.open("http://planetblue.azblue.com/Pages/default.aspx")
	for item in ipaddresses:
		webbrowser.open_new_tab("http://"+item)
		
	
	
def httpsServer_collect():
	ipaddresses = cp_collect()
	httpsServers(ipaddresses)
