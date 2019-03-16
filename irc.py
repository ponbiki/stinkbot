import socket
import ssl


class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    def send_msg(self, chan, out_msg):
        o_msg = f"PRIVMSG {chan} {out_msg} \n"
        self.irc.send(bytes(o_msg, "UTF-8"))

    def send_notice(self, chan, out_notice):
        o_ntc = f"NOTICE {chan} :{out_notice} \n"
        self.irc.send(bytes(o_ntc, "UTF-8"))

    def get_msg(self):
        in_msg = self.irc.recv(2040).decode("UTF-8")

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

        return self.get_msg()

    def join(self, channel):
        self.irc.send(bytes(f"\n\n\n\nJOIN {channel} \n", "UTF-8"))
        return self.get_msg()

    def disconnect(self, q_msg):
        self.irc.send(bytes(f"QUIT :{q_msg}\n\n", "UTF-8"))

    def nick(self, new_nick):
        self.irc.send(bytes(f"NICK {new_nick} \n", "UTF-8"))

    @staticmethod
    def parse_msg(msg):
        stripped = msg[1:].strip("\n")
        expanded = stripped.split(" :", 1)
        info = expanded[0].split()
        txt = expanded[1].strip("\r")
        return {
            'chatter': info[0],
            'msg_type': info[1],
            'target': info[2],
            'txt': txt
        }

    def __del__(self):
        pass
