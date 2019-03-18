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
                if msg['txt'] == "quit":
                    irc.disconnect("Lick my @#$%!")
                    exit()
                elif msg['txt'].split()[0].lower() == "nick":
                    irc.nick(msg['txt'].split()[1])
            if msg['msg_type'] == "PRIVMSG":
                if "thinking emoji" in msg['txt']:
                    irc.send_msg(msg['target'], "🤔")
                if msg['txt'][0] == cmd_char:
                    s_msg = msg['txt'][1:].split()
                    if s_msg[0] == "h":
                        Commands.h(irc, msg)
                    elif s_msg[0] == "r":
                        Commands.roller(irc, msg, s_msg[1])
                    elif s_msg[0] == "s":
                        Commands.roller(irc, msg, s_msg[1], savage=True)
                    elif s_msg[0] == "flip":
                        Commands.flip(irc, msg)
                    elif s_msg[0] == "d":
                        Commands.draw(irc, msg)
                    else:
                        irc.send_msg(msg['target'], f"I don't understand the command \"{s_msg[0]}\"")


if __name__ == '__main__':
    main()
