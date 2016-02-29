import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import random,os
from config import server,channelname,nick,channel,password


queue = 13 #sets variable for anti-spam queue functionality

irc = socket.socket()
irc.connect((server, 6667)) #connects to the server

#sends variables for connection to twitch chat
irc.send('PASS ' + password + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')

rafflelist = []


beginraffle = "Entries for the raffle have started. Type !raffle to join now!!"
print beginraffle
irc.send('PRIVMSG ' + channel + ' :' + beginraffle + '\r\n')

def rafflesave():
    rafflelist.append(user)


def run_raffle():
    print rafflelist
    winner = random.choice(rafflelist)
    rafflewinner = winner + " is the winner!! :)"
    irc.send('PRIVMSG ' + channel + ' :' + rafflewinner + '\r\n')
    print winner + ' won the raffle!!!'
    os._exit(0)


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

while True:
    tilthack = irc.recv(1204) #gets output from IRC server
    user = tilthack.split(':')[1]
    user = user.split('!')[0] #determines the sender of the messages
    

    if tilthack.find('PING') != -1:
        irc.send(tilthack.replace('PING', 'PONG')) #responds to PINGS from the server


    if tilthack.find('!raffle') != -1: 
            if any(word in user for word in rafflelist):
                message(user + ' has already entered :)')
            else:
                rafflesave()
                message(user + ' has been added to the raffle :) '+ str(len(rafflelist)) + ' user(s) have joined the raffle.')
                print rafflelist 
                print len(rafflelist), 'user(s) have joined'

    if tilthack.find('!runraffle') != -1:
        run_raffle()
