# This Script has been Archived

Since Yahoo [announced they were closing Yahoo Groups](https://help.yahoo.com/kb/groups/SLN31010.html), this repo has received quite a lot of attention. I have been working with [Archive Team](https://www.archiveteam.org/index.php/Yahoo!_Groups) to try and archive as much of Yahoo Groups as possible, and during the course of this work others have developed a better script, that downloads files / photos / attachments / links / events, doesn't crash on errors, etc...

This script can be found at: [https://github.com/IgnoredAmbience/yahoo-group-archiver](https://github.com/IgnoredAmbience/yahoo-group-archiver), and I would strongly encourage all future work on Yahoo Groups archiving scripts to happen on this repo.

To those of you who've helped out on this repo, with bug reports, pull requests, ideas and suggestions: thanks. While I'd hoped that Yahoo would renew investment in Groups, the writing was on the wall back in 2015 when I wrote the first version of this script. My focus is now on saving as much of Groups as possible, and focusing work on IgnoredAmbience's script is the best way to do that.

\[Written November 3rd, 2019. Groups is due to be closed December 14, 2019\]

# YahooGroups-Archiver

#### A simple python script that archives all messages from a public Yahoo Group

YahooGroups-Archiver allows you to make a backup copy of all the messages in a public group. Not only is all the message content downloaded, but also all other raw data that Yahoo uses to display the messages.

Messages are downloaded in a JSON format, with one .json file per message.

There is support for private groups, but this requires that you have a Yahoo groups account that has access to the private groups you want to archive. See the 'Private Groups' section for more info.

Works with both Python 2 and Python 3.

## Usage
**`python archive_group.py <groupName> [options] [nologs]`**
where *`<groupName>`* is the name of the group you wish to archive (e.g: hypercard)

**Options**
* *`update`* - the default., Archive all new messages since the last time the script was run
* *`retry`* - Archive any new messages, and attempt to archive any messages that could not be downloaded last time
* *`restart`* - Delete all previously archived messages and archive again from scratch

Please note that you can only have one *Option*, if you specify more than one, only the first will be used, with the others being ignored.

By default a log file called <groupname>.txt is created and stores information such as what messages could not be received. This is entirely for the benefit of the user: it's not needed at all by the script during any re-runs (although re-runs will append new information to the log file). If you don't want a log file to be created or added to, add the `nologs` keyword when you call the script.

## Private Groups
It is possible to archive private groups using this tool, but the way to go about doing this is slighly fiddly at the moment. Rather than simply providing your login information for the Yahoo account that has access to the private groups, you need to provide two pieces of information from Yahoo's login cookies (small files created by web browsers to store data for various uses, such as allowing you to login to websites and then stay logged in for a certain period of time).

Cookie information can be found through the use of a plug-in for your web browser. (I use 'Cookie Manager' on FireFox, although there are many other options for FireFox and other browsers). The two cookies you are looking for are called *Y* and *T*, and they are linked to the domain *yahoo.com*. Extract the data from these cookies, and paste it into the appropriate variables in the *archive_groups.py* script. You should now be able to archive a private group.

Please note that this support is still experimental. One important issue to consider is that a cookie will expire after a certain amount of time, which varies between computers. This means that you may have to re-fetch the *Y* and *T* cookie data every few days, or you will not be able to archive private groups.

## Note
Yahoo attempts to block connections that it deems to be "spamming", and so after around 15,000 messages have been downloaded it is highly likely that Yahoo will block you. This is OK, the script will automatically stop, and Yahoo should unblock you after around two hours. Running the script again once you have been unblocked will just continue where it left off. (Unless you run with the *`restart`* *[option]*, of course!

## Credits
Thanks to the [Archive Team](http://archiveteam.org/) for making [information about the Yahoo Groups API](http://www.archiveteam.org/index.php?title=Yahoo!_Groups) available.
