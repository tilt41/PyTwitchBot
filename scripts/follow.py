import time
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import random,urllib,json,os
from config import server,channelname,nick,channel,password



queue = 13 
numck = 0



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

url = 'https://api.twitch.tv/kraken/channels/'+channelname+'/follows?direction=Desc&limit=1&offset=0'

def savefollower():
	response = urllib.urlopen(url)
	data = json.load(response)
	fname = data['follows'][0]['user']['display_name']
	print "Grabbing new info from api.twitch.tv"

	def followname():
		global numck
		response2 = urllib.urlopen(url)
		data2 = json.load(response2)
		fname2 = data2['follows'][0]['user']['display_name']
		if fname2 != fname:
			numck = numck + 1
			print "New Follow: " + fname2
			os.system("start vlc --qt-start-minimized --play-and-exit sound.wav") #sound for new follow
			irc = socket.socket()
			irc.connect((server, 6667)) 
			irc.send('PASS ' + password + '\r\n')
			irc.send('NICK ' + nick + '\r\n')
			irc.send('JOIN ' + channel + '\r\n')
			tilthack = irc.recv(1204)
			if tilthack.find('PING') != -1:
				irc.send(tilthack.replace('PING', 'PONG'))
			followcmd = " :-D Thank you "+ fname2 + " for following!! :)"
			irc.send('PRIVMSG ' + channel + ' :' + followcmd + '\r\n')
			time.sleep(20)
			savefollower()
		elif fname2 == fname:
			numck = numck + 1
			print "Check " + str(numck)+":  " + fname 
			time.sleep(20) # delays for 20 seconds
			followname()
		else:
			followname()

	followname()		
	
if __name__ == '__main__':
    savefollower()

