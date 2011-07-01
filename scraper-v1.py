#import libraries needed to make web queries
import urllib2
#make sure you download and install BeautifulSoup from http://www.crummy.com/software/BeautifulSoup/
from BeautifulSoup import BeautifulSoup

#the next version of the program will be able to taken multiple securities from a file
#at the moment you need to change these varibales to get different securities
#Also the algo is not smart enough to detect the last page of historical data. This needs to be manually updated in the program for now
#For example, in the case of NSE:ACC, the first url ends with 'start=0'
#If you click >>| on the webpage, it will take you to the last page. Look for 'start=x'. In the case of NSE:ACC it is 1350, which I have set below
#Also the program can be updated to change the dates. For now I am querting all data from Jan 1, 2006 - Jun 28, 2011
#This algo also assumes that you are showing 30 rows per page, as defined in the url under num=30


#CHANGE THESE VARIABLES IF YOU WANT ANOTHER SECURITY'S DATA
googleSecurityIdentifier = "NSE:ACC"
filename = googleSecurityIdentifier.replace(":","") + ".csv"
lastPageNumber = 1350
rowsPerPage = 30

#Opens the file to write data
FILE = open(filename, "w")

#Loops through all the pages of historical data available
for i in range(0,lastPageNumber+rowsPerPage,rowsPerPage):
	urlStr = "http://www.google.com/finance/historical?q=" + googleSecurityIdentifier + "&startdate=Jan%201%2C%202006&enddate=Jun%2028%2C%202011&num=" + str(rowsPerPage) +"&start="+str(i)
	print "Accessing ..." + urlStr
	#Query the url and store the html data in page
	page = urllib2.urlopen(urlStr)
	
	#Using Beautiful Soup to store the html structure in soup
	soup = BeautifulSoup(page)

	#find all the table tags and then pick the third tag from the beginning
	dataTable = soup.findAll('table')[2]

	#These variables are used to determine when to write a line in the FILE
	pos = 0
	li = []

	#Loop through each 'td' tag in the third 'table'
	for rows in dataTable.findAll('td'):
		#Extract the contents of each td. The contents are Date, Open, High, Low, Close and Volume
		val = rows.contents[0]
		val = val.replace('\n','')
		
		#Only write to file when you have a complete line of Date, Open, High, Low, Close and Volume
		if pos < 5:
			#Keep storing the contents until there is a complete line
			li.append(val)
			pos = pos + 1
		else:
			#Write to file all the contents
			rowStr = ""
			for element in li:
				rowStr = rowStr + element + "," 
			#String containing a line to write to file
			rowStr = rowStr + val + "\n"
			FILE.write(rowStr)
			#Empty the variables to start building the next line
			li = []
			pos = 0
			print "String written to FILE: " + rowStr

#Close the file
FILE.close()