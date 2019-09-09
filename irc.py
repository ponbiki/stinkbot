import socket
import ssl
from pprint import pprint


class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.myname = ''  # set later

    def send_msg(self, chan, out_msg):
        o_head = f"PRIVMSG {chan} "
        msg = out_msg
        #pprint("INDEX OF R N: {ind}".format(ind = msg.find('\r\n')))
        while msg:
            maxl = 200  # not robust since utf8 is variable length! UNICOOODE!
            if len(msg) < maxl:
                msgchunk = msg
                msg = ''
            else:
                spindex = msg.rfind(" ", 0, maxl)
                msgchunk = msg[:spindex]
                msg = msg[spindex+1:]

            o_msg = f"PRIVMSG {chan} {msgchunk} \n"
            pprint("OUT >>> " + o_msg)
            self.irc.send(bytes(o_msg, "UTF-8"))

    def send_notice(self, chan, out_notice):
        o_ntc = f"NOTICE {chan} :{out_notice} \n"
        pprint("OUT >>> " + o_ntc)
        self.irc.send(bytes(o_ntc, "UTF-8"))

    def get_msg(self):
        try:
            in_msg = self.irc.recv(2040).decode("UTF-8")
            pprint("IN >>> " + in_msg)
        except Exception as e:
            print(f"Caught exception: {e}")
            in_msg = "Hmmm?"
        if in_msg.find('PING') != -1:
            self.irc.send(bytes(f"PONG {in_msg.split()[1]} \r\n", "UTF-8"))

        return in_msg

    def connect(self, server, port):
        self.irc.connect((server, port))

        return self.get_msg()

    def set_user(self, botnick):
        self.irc.send(bytes(f"USER {botnick} {botnick} {botnick} :broken bot \n", "UTF-8"))

        return self.get_msg()

    def set_nick(self, botnick):
        self.irc.send(bytes(f"NICK {botnick} \n", "UTF-8"))
        self.myname = botnick
        return self.get_msg()

    def join(self, channel):
        self.irc.send(bytes(f"\n\n\n\nJOIN {channel} \n", "UTF-8"))
        return self.get_msg()

    def part(self, channel, part_msg=None):
        self.irc.send(bytes(f"\n\n\n\nPART {channel} {part_msg if part_msg else 'Goodbye'}\n", "UTF-8"))
        return self.get_msg()

    def disconnect(self, q_msg=None):
        self.irc.send(bytes(f"QUIT :{q_msg if q_msg else 'Lick my @#$%!'}\n\n", "UTF-8"))

    # no longer static. needs self.myname
    def parse_msg(self, msg):
        stripped = msg[1:].strip("\n")
        expanded = stripped.split(" :", 1)
        info = expanded[0].split()
        txt = expanded[1].strip("\r")

        sender = info[0].split('!', 1)[0]    # discard email-username, host
        if self.myname.lower() == info[2].lower():
            target = sender
        else:
            target = info[2]

        return {
            'chatter': info[0],
            'msg_type': info[1],
            'target': target,
            'txt': txt
        }

    def __del__(self):
        pass
