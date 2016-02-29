from Tkinter import *
import os
import tkMessageBox

root = Tk()

root.title("TILT's Bots")
top = Frame(root)
top.pack(side=TOP)
center = Frame(root)
center.pack(side=TOP)
bottom = Frame(root)
bottom.pack(side=BOTTOM)

def run_chatbot():
	os.system("start python scripts/bot.py")
def run_followbot():
	os.system("start python scripts/follow.py")
def run_rafflebot():
	os.system("start python scripts/raffle.py")
def run_uptime():
	os.system("start python scripts/uptime.py")		
def run_cmdhelp():
	tkMessageBox.showinfo("Bot Chat Commands", "ChatBots Commands\n  !follow - shows last follower \n  !uptime - shows stream time \n\nRaffleBot \n  !raffle - Users use this to join raffle\n  !runraffle - will pick the raffle winner \n\nUptime button will send your streams uptime to chat.")
def run_readme():
	tkMessageBox.showinfo("Bot Help", "Read the READ ME FIRST.txt file\n\nMake sure config.py is setup properly \n\n - VLC must be installed to use FollowBot \n\nMake sure you can call vlc from command prompt.\nIf VLC is installed and it is still not working check your path in environment variables. \n\n FollowBot is still in beta so it might crash, just close it and push button again. ")

#First Button
chatbot = Button(center, width=10 , bg='#0303FF',activebackground='#0303FF', text = "ChatBot")
chatbot["command"] = run_chatbot
chatbot.pack(side=LEFT)
#second button
followbot = Button(center, width=10, bg='#0303FF',activebackground='#0303FF', text = "FollowBot")
followbot["command"] = run_followbot
followbot.pack(side=LEFT)

rafflebot = Button(center, width=10, bg='#0303FF',activebackground='#0303FF', text = "RaffleBot")
rafflebot["command"] = run_rafflebot
rafflebot.pack(side=LEFT)

uptime = Button(bottom, width=10, bg='#0303FF',activebackground='#0303FF', text = "Uptime")
uptime["command"] = run_uptime
uptime.pack(side=LEFT)

cmdhelp = Button(bottom, width=10, bg='#0303FF',activebackground='#0303FF', text = "Commands")
cmdhelp["command"] = run_cmdhelp
cmdhelp.pack(side=LEFT)

readme = Button(bottom, width=10, bg='#0303FF',activebackground='#0303FF', text = "Readme")
readme["command"] = run_readme
readme.pack(side=RIGHT)

label = Label(top, bg='#0303FF', text = "All bots run indpendently so run what you need")
label.pack(side=TOP)
root.configure(bg='#0303FF')

root.mainloop()
