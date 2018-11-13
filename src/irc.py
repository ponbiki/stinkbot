import socket
import ssl


class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    def send_msg(self, chan, out_msg):
        self.irc.send(bytes(f"PRIVMSG {chan} {out_msg} \n", "UTF-8"))

    def get_msg(self):
        in_msg = self.irc.recv(2040).decode("UTF-8")

        if in_msg.find('PING') != -1:
            self.irc.send(bytes(f"PONG {in_msg.split()[1]} \r\n", "UTF-8"))

        return in_msg

    def connect(self, server, port):
        print(f">>>>>> Connecting to: {server}")
        self.irc.connect((server, port))

        return self.get_msg()

    def set_user(self, botnick):
        print(f">>>>>> Setting user: {botnick}")
        self.irc.send(bytes(f"USER {botnick} {botnick} {botnick} :broken bot \n", "UTF-8"))

        return self.get_msg()

    def set_nick(self, botnick):
        print(f">>>>>> Setting nick: {botnick}")
        self.irc.send(bytes(f"NICK {botnick} \n", "UTF-8"))

        return self.get_msg()

    def join(self, channel):
        print(f">>>>>> Joining {channel}")
        self.irc.send(bytes(f"\n\n\n\nJOIN {channel} \n", "UTF-8"))
        return self.get_msg()

    def disconnect(self, q_msg):
        self.irc.send(bytes(f"QUIT :{q_msg}\n", "UTF-8"))
