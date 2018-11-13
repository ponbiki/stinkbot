from irc import *
from time import sleep

channels = ["#BitchBot", "#dungeoneers"]
server = "irc.7chan.org"
port = 6697
nickname = "goddammit"
owner = "ponbiki!asdf@I.is.confused"

irc = IRC()
print(irc.connect(server, port))
sleep(2)
print(irc.set_user(nickname))
print(irc.set_nick(nickname))
sleep(2)
for channel in channels:
    print(irc.join(channel))

while 1:
    text = irc.get_msg()
    print(text)

    if "PRIVMSG" in text and "hello" in text:
        irc.send_msg(channel, "Hello!")
    if "PRIVMSG" in text and owner in text and "quit" in text:
        break

irc.disconnect("Lick my balls!")
