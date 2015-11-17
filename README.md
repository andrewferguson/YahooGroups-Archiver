#YahooGroups-Archiver

####A simple python script that archives all messages from a public Yahoo Group

YahooGroups-Archiver allows you to make a backup copy of all the messages in a public group. (Currently there is no support for groups that require a sign in before viewing messages, but this may change). Not only is all the message content downloaded, but also all other raw data that Yahoo uses to display the messages.

Messages are downloaded in a JSON format.

##Usage
**`python archive_group.py <groupName> [options]`**
where *`<groupName>`* is the name of the group you wish to archive (e.g: hypercard)

**Options**
* *`update`* - the default., Archive all new messages since the last time the script was run
* *`retry`* - Archive any new messages, and attempt to archive any messages that could not be downloaded last time
* *`restart`* - Delete all previously archived messages and archive again from scratch

##Note
This script uses a Yahoo API, which may be removed at any time.

Yahoo also activly tries to block connections that it deems to be "spamming", and so after around 15,000 messages have been downloaded it is highly likely that Yahoo will block you. This is OK, the script will automatically stop, and Yahoo should unblock you after around two hours. Running the script again once you have been unblocked will just continue where it left off.

##Credits
Thanks to the [Archive Team](http://archiveteam.org/) for making [information about the Yahoo Groups API](http://www.archiveteam.org/index.php?title=Yahoo!_Groups) available.
