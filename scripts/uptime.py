import time
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import urllib,json,os
from config import server,channelname,nick,channel,password
from datetime import datetime, timedelta, date, time


queue = 13 
irc = socket.socket()
irc.connect((server, 6667)) #connects to the server
#sends variables for connection to twitch chat
irc.send('PASS ' + password + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')

def message(msg): #function for sending messages to the IRC chat
    global queue
    queue = 5
    #print queue
    if queue < 20: #ensures does not send >20 msgs per 30 seconds.
        irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
    else:
        print 'Message deleted'

def queuetimer(): #function for resetting the queue every 30 seconds
    global queue
    #print 'queue reset'
    queue = 0
    threading.Timer(30,queuetimer).start()
queuetimer()


url = "https://api.twitch.tv/kraken/streams/"+ channelname
response = urllib.urlopen(url)
data = json.load(response)
broadcastck = data['stream']
if broadcastck == None:
	irc.send('PRIVMSG ' + channel + ' :' + channelname + " is not streaming" + '\r\n')
else:
	broadcast = data['stream']['created_at']
	timeFormat = "%Y-%m-%dT%H:%M:%SZ"
	startdate = datetime.strptime(broadcast, timeFormat)
	currentdate = datetime.utcnow()
	combineddate = currentdate - startdate - timedelta(microseconds=currentdate.microsecond)		
	irc.send('PRIVMSG ' + channel + ' :' + channelname +  " has been streaming for " + str(combineddate) + '\r\n')
		
os._exit(0)
