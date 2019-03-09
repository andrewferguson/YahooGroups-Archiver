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
          print 'Yahoo Message: ' + file + ' archived to: archive-' + str(messageYear) + '.html'
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
    
    messageText = '-----------------------------------------------------------------------------------<br>'
    messageText += 'Post ID:' + str(emailMessageID) + '<br>'
    messageText += 'Sender:' + emailMessageSender + '<br>'
    messageText += 'Post Date/Time:' + emailMessageDateTime + '<br>'
    messageText += 'Subject:' + emailMessageSubject + '<br>'
    messageText += 'Message:' + '<br><br>'
    messageText += messageBody
    messageText += '<br><br><br><br><br>'
    return messageText
    
def getYahooMessageYear(file):
    f1 = open(file,'r')
    fileContents=f1.read()
    f1.close()
    jsonDoc = json.loads(fileContents)
    emailMessageTimeStamp = jsonDoc['ygData']['postDate']
    return datetime.fromtimestamp(float(emailMessageTimeStamp)).year

# Thank you to the help in this forum for the bulk of this function
# https://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
def getEmailBody(message):
    body = ''
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body += '<pre>'
                body += part.get_payload(decode=True)  # decode
                body += '</pre>'
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        ctype = message.get_content_type()
        if ctype != 'text/html':
             body += '<pre>'
        body += message.get_payload(decode=True)
        if ctype != 'text/html':
             body += '</pre>'
    return body

## This is where the script starts

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
         archiveFile = archiveDir + '/archive-' + str(messageYear) + '.html'
         archiveYahooMessage(file, archiveFile, messageYear, 'utf-8')
else:
     sys.exit('Please run archive-group.py first')

os.chdir(oldDir)
print('Complete')


