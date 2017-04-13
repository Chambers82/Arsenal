# Title: VMEX Vulnerability Management Engine X
# Description:  Nessus/Metasploit + WSUS Data Correlator for Risk Analysis
# Functions:
#  generateIndex:          Produces a reference Index from Nessus report_host_list output
#  generateInventory:      Produces a reference Index from WSUS inventory output
#  checkInventory:         Cross references the nessus output with the inventory list, generating a list of registered servers
#                          servers that aren't references aren't within the patch cycle.
#  runInventoryReference:  creates a reference table for the inventory list items
#  runCorrelation:         Correlation engine that produces the filtered and usable xls data structure
#  generateWorksheet       Generates an excel worksheet from the correlation data




import string
import xlwt
import os

def generateIndex():  #produces a referenceable index of current vulnerabilities
	file = open("c:\\python27\\vulnerabilityIndex.txt")
	lineIndex = []
	intIndex = []
	mainIndex = []
	for a in file:
		lineIndex.append(a) #creates a list of objects in lineIndex
	for b in lineIndex:
		intIndex.append(string.split(`b`)) #filter out the tabs in lineIndex
	for c in intIndex:
		c[-1] = c[-1][:1]     
	for d in intIndex:
		d[0] = d[0][1:]
	for e in intIndex:
		mainIndex.append(e)
	return mainIndex

def generateIndex2():
	import string
	file = open("c:\\python27\\vulnerabilityIndex.txt")
	lineIndex = []
	intIndex = []
	mainIndex = []
	for line in file:
		lineIndex.append(line) #creates a list of objects in lineIndex
	for item in lineIndex:
		item = string.split(`item`)
	for record in lineIndex:
		mainIndex.append(string.split(record))
	#for c in intIndex:
	#	c = string.split(c)
	return mainIndex
#build a correlation to identify the hostname, role, tier and os


def generateInventory():  #produces an refernceable index of servers
    file = open("c:\\python27\\systemIndex.txt")
    lineIndex = []
    #filterIndex = []
    for item in file:
        lineIndex.append(string.split(item, "\t"))
    for item in lineIndex:
        item[-1] = item[-1][:-1]
    return lineIndex


def checkInventory():#checks the vulnerability host list to the inventory to see what's registered
    #clone this function to find hosts that aren't in the registered inventory
    invt = generateInventory()
    vulns = generateIndex()
    inventoryList = []
    registeredVulns = []
    for inventoryItem in invt:
        inventoryList.append(inventoryItem[1])  #compare list for the discovered vulns (just IP addresses)
    for vulnerabilityItem in vulns:
        if vulnerabilityItem[0] in inventoryList:
            print vulnerabilityItem[0], "is registered!"
            registeredVulns.append(vulnerabilityItem[0])
        else:
            pass
    return registeredVulns


def runInventoryReference():  #creates a table consisting of tuples that match the address with the line number in the inventoryIndex
    invt = generateInventory()
    vulns = generateIndex()
    refTable = {}
    for item in invt:
        #print item[1], "\t\t", invt.index(item)
        addr, ref = item[1], invt.index(item)
        refTable[str(addr)] = ref
    return refTable

def runCorrelation():       #generates a clean list of servers and their discovered vulnerabilities
    invt = generateInventory()
    vulns = generateIndex()
    refTable = runInventoryReference()
    correlationList = []
    for item in vulns:
        if item[0] in `invt[:]`:
            try:
                #print item + invt[refTable[item[0]]]
                correlationList.append(item + invt[refTable[item[0]]])
            except:
                pass
        else:
            pass
    vulnerabilityOutput = []
    #print correlationList
    for i in correlationList:
        try:
             vulnerabilityOutput.append((i[0], i[-2], i[8], i[1], i[3], i[4], i[5], i[-1]))
            #vulnerabilityOutput.append((i[0], i[8], i[6], i[1], i[3], i[4], i[5], i[9]))
        except:
            pass
    print "Vulnerability Output"
    print vulnerabilityOutput
    #print (i[0], i[8], i[6], i[1], i[3], i[4], i[5], i[9])
    return vulnerabilityOutput


 
# INDEX REFERENCE VALUES
# IPADDRESS     = 0
# HOSTNAME      = 8
# ROLE          = 6
# TOTALVULNS    = 1
# LOWS          = 3
# MEDIUMS       = 4
# HIGHS         = 5
# OS            = 9

def generateWorksheet():
    worksheetData = runCorrelation()
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("Vulnerability Data")
    sheet.write(0,0,"IPADDRESS") 
    sheet.write(0,1,"HOSTNAME")
    sheet.write(0,2,"ROLE")
    sheet.write(0,3,"TOTALVULNS")
    sheet.write(0,4,"LOWS")
    sheet.write(0,5,"MEDIUMS")
    sheet.write(0,6,"HIGHS")
    sheet.write(0,7,"OS")
    columnIndex = 1
    rowIndex = 0
    for entry in worksheetData:
        while rowIndex <= 2:
            sheet.write(columnIndex, rowIndex, entry[rowIndex])
            rowIndex = rowIndex + 1
        while rowIndex <= 6:
            sheet.write(columnIndex, rowIndex, int(entry[rowIndex]))
            rowIndex = rowIndex + 1
        sheet.write(columnIndex, rowIndex, entry[rowIndex])
        columnIndex = columnIndex + 1
        rowIndex = 0
    wbk.save("c:\\python27\\Vulnerability_Worksheet.xls")
    os.system("start c:\\python27\\Vulnerability_Worksheet.xls")
        

if __name__=="__main__":
    print "Updating vulnerabilityIndex..."
    print "Updating systemIndex..."


























