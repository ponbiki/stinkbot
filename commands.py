from random import randint
from pprint import pprint


class Commands:

    @staticmethod
    def h(conn, msg):
        """
        Literally prints a big 'h'
        :param conn: IRC connection instance
        :return: None
        """
        conn.send_msg(msg['target'], "hh")
        conn.send_msg(msg['target'], "hh")
        conn.send_msg(msg['target'], "hh")
        conn.send_msg(msg['target'], "hh")
        conn.send_msg(msg['target'], "hhhhhhh")
        conn.send_msg(msg['target'], "hh   hh")
        conn.send_msg(msg['target'], "hh   hh")
        conn.send_msg(msg['target'], "hh   hh")
        conn.send_msg(msg['target'], "hh   hh")

    @staticmethod
    def roller(conn, msg, to_roll):
        """
        Dice roller functionality
        :param conn: IRC connection instance
        :param to_roll: roll parameters (e.g. 2#1d20, number of totals and number of dice are optional)
        :return: None
        """
        to_roll = to_roll.lower()

        def roll():
            pass

        if "#" in to_roll:
            multi = to_roll.split("#")
            pprint(f"Multi: {multi}")
            broke = multi[1].split("d")
            pprint(f"Broke: {broke}")
            total = ""
        else:
            split_nums = to_roll.split("d") if "d" in to_roll else [1, to_roll]
            total = 0
            roll_list = []
            for die in range(int(split_nums[0])):
                roll = randint(1, int(split_nums[1]))
                roll_list.append(roll)
                total += roll

            conn.send_msg(msg['target'], f"{total} {roll_list}")
