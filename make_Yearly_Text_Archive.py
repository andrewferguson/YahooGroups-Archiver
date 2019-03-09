#!/usr/local/bin/python
import email
import HTMLParser
import json
import os
import sys
from datetime import datetime
from natsort import natsorted, ns

#To avoid Unicode Issues
reload(sys)
sys.setdefaultencoding('utf-8')

def archiveYahooMessage(file, archiveFile, messageYear, format):
     try:
          f = open(archiveFile, 'a')
          f.write(loadYahooMessage(file, format))
          f.close()
          print 'Yahoo Message: ' + file + ' archived to: archive-' + str(messageYear) + '.txt'
     except Exception as e:
          print 'Yahoo Message: ' + file + ' had an error:'
          print e

def loadYahooMessage(file, format):
    f1 = open(file,'r')
    fileContents=f1.read()
    f1.close()
    jsonDoc = json.loads(fileContents)
    emailMessageID = jsonDoc['ygData']['msgId']
    emailMessageSender = HTMLParser.HTMLParser().unescape(jsonDoc['ygData']['from']).decode(format).encode('utf-8')
    emailMessageTimeStamp = jsonDoc['ygData']['postDate']
    emailMessageDateTime = datetime.fromtimestamp(float(emailMessageTimeStamp)).strftime('%Y-%m-%d %H:%M:%S')
    emailMessageSubject = HTMLParser.HTMLParser().unescape(jsonDoc['ygData']['subject']).decode(format).encode('utf-8')
    emailMessageString = HTMLParser.HTMLParser().unescape(jsonDoc['ygData']['rawEmail']).decode(format).encode('utf-8')
    message = email.message_from_string(emailMessageString)
    messageBody = getEmailBody(message)
    
    messageText = '-----------------------------------------------------------------------------------\n'
    messageText += 'Post ID:' + str(emailMessageID) + '\n'
    messageText += 'Sender:' + emailMessageSender + '\n'
    messageText += 'Post Date/Time:' + emailMessageDateTime + '\n'
    messageText += 'Subject:' + emailMessageSubject + '\n'
    messageText += 'Message:' + '\n\n'
    messageText += messageBody
    messageText += '\n\n\n\n\n'
    return messageText
    
def getYahooMessageYear(file):
    f1 = open(file,'r')
    fileContents=f1.read()
    f1.close()
    jsonDoc = json.loads(fileContents)
    emailMessageTimeStamp = jsonDoc['ygData']['postDate']
    return datetime.fromtimestamp(float(emailMessageTimeStamp)).year

def getEmailBody(message):
    body = ''
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body += part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body += message.get_payload(decode=True)
    return body

if len(sys.argv) < 2:
     sys.exit('You need to specify your group name')

groupName = sys.argv[1]
oldDir = os.getcwd()
if os.path.exists(groupName):
    archiveDir = os.path.abspath(groupName + '-archive')
    if not os.path.exists(archiveDir):
         os.makedirs(archiveDir)
    os.chdir(groupName)
    for file in natsorted(os.listdir(os.getcwd())):
         messageYear = getYahooMessageYear(file)
         archiveFile = archiveDir + '/archive-' + str(messageYear) + '.txt'
         archiveYahooMessage(file, archiveFile, messageYear, 'utf-8')
else:
     sys.exit('Please run archive-group.py first')

os.chdir(oldDir)
print('Complete')


