import json

from irc import *
from commands import *
from time import sleep


def conf_reader():
    """

    :return:
    """
    with open('config.json', 'r') as json_conf:
        cfg = json.load(json_conf)

    return cfg


def main():
    """
    The main bot connection and run loop
    :return: None
    """
    cfg = conf_reader()
    b_cfg = cfg['bot_config']
    cmd_char = b_cfg['cmd_char']
    irc = IRC()
    irc.connect(b_cfg['server'], b_cfg['port'])
    sleep(2)
    irc.set_user(b_cfg['bot_nick'])
    irc.set_nick(b_cfg['bot_nick'])
    sleep(2)
    for channel in b_cfg['channels']:
        irc.join(channel)

    while 1:
        msg = irc.get_msg()

        if "PRIVMSG" in msg or "NOTICE" in msg:
            msg = irc.parse_msg(msg)
            if msg['msg_type'] == "PRIVMSG" and msg['chatter'] == b_cfg['owner']:
                if msg['txt'].split()[0] == "quit":
                    if len(msg['txt'].split()) > 1:
                        print(" ".join(msg['txt'].split()[1:]))
                        irc.disconnect(" ".join(msg['txt'].split()[1:]))
                        exit()
                    else:
                        irc.disconnect()
                        exit()
                elif msg['txt'].split()[0].lower() == "nick":
                    irc.set_nick(msg['txt'].split()[1])
                elif msg['txt'].split()[0].lower() == "join":
                    irc.join(msg['txt'].split()[1])
                elif msg['txt'].split()[0].lower() == "part":
                    if len(msg['txt'].split()) > 2:
                        irc.part(msg['txt'].split()[1], " ".join(msg['txt'].split()[2:]))
                    irc.part(msg['txt'].split()[1])
            if msg['msg_type'] == "PRIVMSG":
                if "thinking emoji" in msg['txt'].lower():
                    irc.send_msg(msg['target'], "🤔")
                if msg['txt'][0] == cmd_char and len(msg['txt']) > 1:
                    s_msg = msg['txt'].lower()[1:].split()
                    if s_msg[0] == "h":
                        Commands.h(irc, msg)
                    elif s_msg[0] == "r" and len(s_msg) > 1:
                        Commands.roller(irc, msg, s_msg[1])
                    elif s_msg[0] == "s" and len(s_msg) > 1:
                        Commands.roller(irc, msg, s_msg[1], savage=True)
                    elif s_msg[0] == "flip":
                        Commands.flip(irc, msg)
                    elif s_msg[0] == "d":
                        Commands.draw(irc, msg)
                    elif s_msg[0] == "help":
                        irc.send_msg(msg['target'], f"Yeah...you do need help...")  # TODO: add real help


if __name__ == '__main__':
    main()
