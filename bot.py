from irc import *
from commands import *
from time import sleep

# Will probably read these variables out of a config file later
channels = ["#BitchBot", "#dungeoneers"]
server = "irc.7chan.org"
port = 6697
nickname = "Quartz"
owner = "ponbiki!asdf@I.is.confused"
command_char = "."


def main():
    irc = IRC()
    irc.connect(server, port)
    sleep(2)
    irc.set_user(nickname)
    irc.set_nick(nickname)
    sleep(2)
    for channel in channels:
        irc.join(channel)

    while 1:
        msg = irc.get_msg()

        if "PRIVMSG" in msg or "NOTICE" in msg:
            msg = irc.parse_msg(msg)
            if msg['msg_type'] == "PRIVMSG" and msg['chatter'] == owner:
                if msg['txt'] == "quit":
                    irc.disconnect("Lick my @#$%!")
                    exit()
                elif msg['txt'].split()[0].lower() == "nick":
                    irc.nick(msg['txt'].split()[1])
            if msg['msg_type'] == "PRIVMSG":
                if msg['txt'][0] == command_char:
                    s_msg = msg['txt'][1:].split()
                    if s_msg[0] == "h":
                        Commands.h(irc, msg)
                    elif s_msg[0] == "r":
                        Commands.roller(irc, msg, s_msg[1])
                    elif s_msg[0] == "sick":
                        irc.send_msg(msg['target'], "barf")
                    elif s_msg[0] == "flip":
                        Commands.flip(irc, msg)
                    else:
                        irc.send_msg(msg['target'], f"I don't understand the command \"{s_msg[0]}\"")


if __name__ == '__main__':
    main()
