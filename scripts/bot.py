import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import random,urllib,json
from datetime import datetime, timedelta, date, time
from time import gmtime, strftime, localtime
from config import server,channelname,nick,channel,password,psnuname


queue = 13 #sets variable for anti-spam queue functionality

irc = socket.socket()
irc.connect((server, 6667)) #connects to the server

greetword = ["hello", "Hello", "hey", "Hey", "hallo", "Hallo","Hi"]
slanggreet = ["sup", "wazzup", "Whats up", "Wat up", "whats up", "wat up"]
departword = ["bye", "cya","adios","ciao","im out", "peace", "Peace", "Later", "later","good night","Good night" ]
psnword = ["psn","PSN", "join","inv me"]
funnyword = ["Haha", "haha", "lol", "Lol","lel", "Lel", "rofl", "Rofl", "Hahaha", "hahaha", "Hahahaha", "hahahaha", "Hehe", "hehe", "Funny", "funny", "Hehehe", "hehehe"  ]
tyword = ["thank you","Thank you","Thanks","thanks"]
connectcheck = ["maze of twisty passages"]
botQ = ["a bot"]
feelingq = ["How are you", "how are you", "how are u","How are u","whats going on","Whats going on", "hows it going", "whats goin on", "Whats goin on"]
feeling = ["I feel a little sick","I am happy and you?","I feel tired...","I am soo annoyed with this game","Sad :(","Hungry for tacos","Tired of being bot :( I wish I was a real boy lol psych :)","So freaking happy","My creator says I am not allowed to have feelings","Help my creator never lets me out of this chatbox","How am I? How do you think I feel living in a chatbox"]


#sends variables for connection to twitch chat
irc.send('PASS ' + password + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')


def followname():
    url = 'https://api.twitch.tv/kraken/channels/'+channelname+'/follows?direction=Desc&limit=1&offset=0'
    response = urllib.urlopen(url)
    data = json.load(response)
    fname = data['follows'][0]['user']['display_name']
    followcmd = fname + " was the last to follow this channel :)"
    irc.send('PRIVMSG ' + channel + ' :' + followcmd + '\r\n')

def message(msg): #function for sending messages to the IRC chat
    global queue
    queue = 5
    #print queue
    if queue < 20: #ensures does not send >20 msgs per 30 seconds.
        irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
    else:
        print 'Message deleted'

def uptime():
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


def queuetimer(): #function for resetting the queue every 30 seconds
    global queue
    #print 'queue reset'
    queue = 0
    threading.Timer(30,queuetimer).start()
queuetimer()

while True:
    tilthack = irc.recv(1204) #gets output from IRC server
    user = tilthack.split(':')[1]
    user = user.split('!')[0] #determines the sender of the messages
    print  tilthack

    if tilthack.find('PING') != -1:
        irc.send(tilthack.replace('PING', 'PONG')) #responds to PINGS from the server

    if any(word in tilthack for word in connectcheck):
        message("Connected")

    if any(word in tilthack for word in greetword):
        message(random.choice(greetword)+' :-D ' + user + ' hope you enjoy the stream :)')

    if any(word in tilthack for word in slanggreet):
        message(random.choice(slanggreet)+' ' + user + ' hope you enjoy the stream :)')

    if any(word in tilthack for word in departword):
        message('cya later ' + user + ' thanks for watching :)')        

    if any(word in tilthack for word in psnword): 
        message('You can join anytime... Click that Follow button and send a friend request to  '+psnuname)

    if any(word in tilthack for word in tyword):
        message('your welcome')


    if any(word in tilthack for word in feelingq):
        message(random.choice(feeling))        

    if any(word in tilthack for word in funnyword):
        message('Haha rofl :)')

    if any(word in tilthack for word in botQ):
        message('Yes I am a bot and my name is '+nick+'. It is nice to meet you '+ user +' :P If you would like help setting me up on your channel follow this channel. :)')

    if tilthack.find('!follow') != -1: 
        message(str(followname()))

    if tilthack.find('!uptime') != -1: 
        message(str(uptime()))

    if tilthack.find('time') != -1: 
        message(strftime("Local time is  " + "%a, %d %b %Y %H:%M:%S", localtime())+ ", " + user)
