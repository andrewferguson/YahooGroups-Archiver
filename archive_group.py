'''
Yahoo-Groups-Archiver Copyright 2015 Andrew Ferguson

YahooGroups-Archiver, a simple python script that allows for all
messages in a public Yahoo Group to be archived.


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json #required for reading various JSON attributes from the content
import urllib2 #required for fetching the raw messages
import os #required for checking if a file exists locally
import time #required if Yahoo blocks access temporarily (to wait)
import sys #required to cancel script if blocked by Yahoo

def archive_group(groupName):
	if not os.path.exists(groupName):
		os.makedirs(groupName)
	max = group_messages_max(groupName)
	for x in range(1,max+1):
		if not os.path.isfile(groupName + '/' + str(x) + ".json"):
			log("Archiving message " + str(x) + " of " + str(max))
			archive_message(groupName, x)
		

def group_messages_max(groupName):
	resp = urllib2.urlopen('https://groups.yahoo.com/api/v1/groups/' + groupName + '/messages?count=1&sortOrder=desc&direction=-1')
	pageJson = json.loads(resp.read())
	return pageJson["ygData"]["totalRecords"]

def archive_message(groupName, msgNumber, depth=0):
	global failed
	failed = False
	try:
		resp = urllib2.urlopen('https://groups.yahoo.com/api/v1/groups/' + groupName + '/messages/' + str(msgNumber) + '/raw')
	except urllib2.HTTPError, e:
		#some other problem, perhaps being refused access by Yahoo?
		#retry for a max of 3 times anyway
		if depth < 3:
			print "Cannot get message " + str(msgNumber) + ", attempt " + str(depth+1) + " of 3"
			time.sleep(0.1)
			archive_message(groupName,msgNumber,depth+1)
		else:
			if str(e) == "HTTP Error 500: Server Error":
				#we are most likely being blocked by Yahoo
				log("Archive halted - it appears Yahoo has blocked you.")
				log("Check if you can access the group's homepage from your browser. If you can't, you have been blocked.")
				log("Don't worry, in a few hours (normally less than 3) you'll be unblocked and you can run this script again - it'll continue where you left off.")
				sys.exit()
			log("Failed to retrive message " + str(msgNumber) )
			failed = True
	
	if failed == True:
		return
	
	msgJson = resp.read()
	writeFile = open((groupName + "/" + str(msgNumber) + ".json"), "wb")
	writeFile.write(msgJson)
	writeFile.close()
			

def log(msg):
	print msg
	logF = open("log.txt", "a")
	logF.write("\n" + msg)

archive_group(sys.argv[1])