from irc import *
from time import sleep

channel = "#BitchBot"
server = "irc.7chan.org"
port = 6697
nickname = "goddammit"

irc = IRC()
print(irc.connect(server, port))
sleep(3)
print(irc.set_user(nickname))
print(irc.set_nick(nickname))
sleep(2)
print(irc.join(channel))

while 1:
    text = irc.get_msg()
    print(text)

    if "PRIVMSG" in text and channel in text and "hello" in text:
        irc.send_msg(channel, "Hello!")
    if "PRIVMSG" in text and channel in text and "quit" in text:
        break

irc.disconnect("Lick my balls!")
