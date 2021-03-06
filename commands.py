import re
from random import randint, choice, shuffle


class InvalidRollInput(Exception):
    """Roll parameters were invalid"""


class Commands:
    HEADS = "heads"
    TAILS = "tails"
    DECK_A = [  # Unused due to limited isocode support in some Windows versions
        "\x0301,00🂡", "\x0301,00🂢", "\x0301,00🂣", "\x0301,00🂤", "\x0301,00🂥",
        "\x0301,00🂦", "\x0301,00🂧", "\x0301,00🂨", "\x0301,00🂩", "\x0301,00🂪",
        "\x0301,00🂫", "\x0301,00🂬", "\x0301,00🂭", "\x0301,00🂮", "\x0301,00🃑",
        "\x0301,00🃒", "\x0301,00🃓", "\x0301,00🃔", "\x0301,00🃕", "\x0301,00🃖",
        "\x0301,00🃗", "\x0301,00🃘", "\x0301,00🃙", "\x0301,00🃚", "\x0301,00🃛",
        "\x0301,00🃜", "\x0301,00🃝", "\x0301,00🃞", "\x0304,00🂱", "\x0304,00🂲",
        "\x0304,00🂳", "\x0304,00🂴", "\x0304,00🂵", "\x0304,00🂶", "\x0304,00🂷",
        "\x0304,00🂸", "\x0304,00🂹", "\x0304,00🂺", "\x0304,00🂻", "\x0304,00🂼",
        "\x0304,00🂽", "\x0304,00🂾", "\x0304,00🃁", "\x0304,00🃂", "\x0304,00🃃",
        "\x0304,00🃄", "\x0304,00🃅", "\x0304,00🃆", "\x0304,00🃇", "\x0304,00🃈",
        "\x0304,00🃉", "\x0304,00🃊", "\x0304,00🃋", "\x0304,00🃌", "\x0304,00🃍",
        "\x0304,00🃎", "\x0304,00🂿", "\x0301,00🂿"
    ]

    DECK = [
        "\x0301,00A♠", "\x0301,002♠", "\x0301,003♠", "\x0301,004♠", "\x0301,005♠",
        "\x0301,006♠", "\x0301,007♠", "\x0301,008♠", "\x0301,009♠", "\x0301,0010♠",
        "\x0301,00J♠", "\x0301,00Q♠", "\x0301,00K♠", "\x0301,00A♣", "\x0301,002♣",
        "\x0301,003♣", "\x0301,004♣", "\x0301,005♣", "\x0301,006♣", "\x0301,007♣",
        "\x0301,008♣", "\x0301,009♣", "\x0301,0010♣", "\x0301,00J♣", "\x0301,00Q♣",
        "\x0301,00K♣", "\x0304,00A♥", "\x0304,002♥", "\x0304,003♥", "\x0304,004♥",
        "\x0304,005♥", "\x0304,006♥", "\x0304,007♥", "\x0304,008♥", "\x0304,009♥",
        "\x0304,0010♥", "\x0304,00J♥", "\x0304,00Q♥", "\x0304,00K♥", "\x0304,00A♦",
        "\x0304,002♦", "\x0304,003♦", "\x0304,004♦", "\x0304,005♦", "\x0304,006♦",
        "\x0304,007♦", "\x0304,008♦", "\x0304,009♦", "\x0304,0010♦", "\x0304,00J♦",
        "\x0304,00Q♦", "\x0304,00K♦", "\x0304,00★", "\x0301,00★"
    ]

    @staticmethod
    def flip(conn, msg):
        """
        Simple heads/tails coin flip function
        :param conn: IRC connection instance
        :param msg: dictionary of IRC message components
        :return: None
        """
        conn.send_msg(msg['target'], f"(ノಠ益ಠ)ノ彡┻━┻"
                                     f"  {Commands.HEADS if randint(0, 1) == 0 else Commands.TAILS}")

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
    def roller(conn, msg, to_roll, savage=False):  # TODO: limit max dice
        """
        Dice roller functionality
        :param conn: IRC connection instance
        :param msg: JSON string containing chat information
        :param to_roll: roll parameters (e.g. 2#1d20, number of totals and number of dice are optional)
        :param savage: BOOL use "exploding dice" and wild die (default False)
        :return: None
        """

        to_roll = to_roll.lower()

        def roll(num, svg_roll=False):
            if not svg_roll:
                try:
                    return randint(1, int(num))
                except Exception as e:
                    raise InvalidRollInput(e)
            else:
                try:
                    sv_total = []
                    r = randint(1, int(num))
                    sv_total.append(r)
                    sv_sum = r
                    while sv_sum % int(num) == 0:
                        r = randint(1, int(num))
                        sv_total.append(r)
                        sv_sum += r
                    return sv_total
                except Exception as e:
                    raise InvalidRollInput(e)

        mod_operator = None
        mod_amount = None

        def find_mod(num):
            try:
                if "+" in num:
                    temp_num = num.split("+")
                    m_amount = temp_num.pop(1)
                    m_operator = "+"
                    return temp_num[0], m_amount, m_operator
                elif "-" in num:
                    temp_num = num.split("-")
                    m_amount = temp_num.pop(1)
                    m_operator = "-"
                    return temp_num[0], m_amount, m_operator
                elif "*" in num:
                    temp_num = num.split("*")
                    m_amount = temp_num.pop(1)
                    m_operator = "*"
                    return temp_num[0], m_amount, m_operator
                elif "/" in num:
                    temp_num = num.split("/")
                    m_amount = temp_num.pop(1)
                    if m_amount == 0:
                        raise InvalidRollInput("Div by 0")
                    else:
                        m_operator = "/"
                        return temp_num[0], m_amount, m_operator
                else:
                    return num, None, None
            except Exception as e:
                raise InvalidRollInput(e)

        def apply_mod(num):
            try:
                if mod_operator is None:
                    return num, None, None
                elif mod_operator == "+":
                    return num + int(mod_amount), None, None
                elif mod_operator == "-":
                    return num - int(mod_amount), None, None
                elif mod_operator == "*":
                    return num * int(mod_amount), None, None
                elif mod_operator == "/":
                    return num // int(mod_amount), None, None
            except Exception as e:
                raise InvalidRollInput(e)

        if not savage:  # standard RPG rolls
            try:
                if "#" in to_roll:
                    multi = to_roll.split("#")
                    if int(multi[0]) > 500:
                        conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on that.")
                        return
                    broke = multi[1].split("d")
                    if len(broke) <= 1:
                        conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on that.")
                        return
                    broke[1], mod_amount, mod_operator = find_mod(broke[1])

                    # 4d6h3
                    # hilo = (DiceSides, OnlyThisManyDiceCounted, LowestOrHighest [-1|1])
                    hilo = broke[1].split("l")
                    if len(hilo) > 1:
                        hilo.append(-1)
                    else:
                        hilo = broke[1].split("h")
                        if len(hilo) > 1:
                            hilo.append(1)
                        else:
                            hilo.append(broke[0])
                    if hilo[1] > broke[0]:
                        hilo[1] = broke[0]

                    if int(broke[0]) > 500 or int(hilo[0]) > 100000:
                        conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on that.")
                        return
                    final = ""

                    for h, _ in enumerate(range(int(multi[0]))):
                        total = 0
                        roll_list = []
                        for _ in range(int(broke[0])):
                            res = roll(int(hilo[0]))
                            roll_list.append(res)
                        if len(roll_list) < 1:
                            conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on that.")
                            return
                        if len(hilo) > 2 and int(hilo[1]) < int(broke[0]):
                            roll_list.sort(reverse = hilo[2] > 0)
                        for _ in range(int(hilo[1])):
                            total += roll_list[_]
                        total, _, _ = apply_mod(total)
                        roll_list[0] = f"{multi[1]}={roll_list[0]}"
                        final += f"{total} [{', '.join(map(str, roll_list))}]"
                        if h != int(multi[0]) - 1:
                            final += ", "

                    mod_operator = None
                    mod_amount = None

                    conn.send_msg(msg['target'], f"{msg['chatter'].split('!')[0]}, {to_roll}: {final}")
                else:
                    split_nums = to_roll.split("d") if "d" in to_roll else [1, to_roll]
                    total = 0
                    roll_list = []
                    split_nums[1], mod_amount, mod_operator = find_mod(split_nums[1])
                    if int(split_nums[0]) > 500 or int(split_nums[1]) > 100000:
                        conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on that.")
                        return
                    for _ in range(int(split_nums[0])):
                        res = roll(split_nums[1])
                        roll_list.append(res)
                        total += res
                    total, mod_amount, mod_operator = apply_mod(total)
                    conn.send_msg(msg['target'], f"{msg['chatter'].split('!')[0]}, {to_roll}: {total}"
                                                 f" [{to_roll}={', '.join(map(str, roll_list))}]")

            except (ValueError, InvalidRollInput):
                conn.send_msg(msg['target'], f"Sorry, {msg['chatter'].split('!')[0]}. "
                                             f"I could not understand \"{to_roll}\".")
        else:  # SavageWorlds rolls
            try:
                to_roll, mod_amount, mod_operator = find_mod(to_roll)
                try:
                    to_roll = int(to_roll)
                except (ValueError, InvalidRollInput):
                    conn.send_msg(msg['target'], f"Sorry, {msg['chatter'].split('!')[0]}. "
                                                 f"I could not understand \"{to_roll}\".")
                    return
                if int(to_roll) <= 1 or int(to_roll) > 100000:
                    conn.send_msg(msg['target'], f"Nice try, pal. I'm not gonna explode on {to_roll}.")
                    return
                main_res_list = roll(to_roll, svg_roll=True)
                main_total = sum(main_res_list)
                main_total, _, _ = apply_mod(main_total)
                wild_res_list = roll(6, svg_roll=True)
                wild_total = sum(wild_res_list)
                wild_total, _, _ = apply_mod(wild_total)
                conn.send_msg(msg['target'], f"{msg['chatter'].split('!')[0]}, d{to_roll}"
                                             f"{mod_operator if mod_operator else ''}"
                                             f"{mod_amount if mod_amount else ''}:"
                                             f" {main_total}, wild: {wild_total} || d{to_roll}"
                                             f" [{', '.join(map(str, main_res_list))}], wild:"
                                             f" [{', '.join(map(str, wild_res_list))}] ")

            except (ValueError, InvalidRollInput):
                conn.send_msg(msg['target'], f"Sorry, {msg['chatter'].split('!')[0]}. "
                                             f"I could not understand \"{to_roll}\".")

    @staticmethod
    def draw(conn, msg):
        """
        Draws playing cards
        :param conn: IRC connection instance
        :param msg: Number of cards to draw or players to draw a card for
        :return: None
        """

        split_msg = msg['txt'].split()
        if len(split_msg) <= 1:
            conn.send_msg(msg['target'], f"{msg['chatter'].split('!')[0]}, {choice(Commands.DECK)}")
        elif len(split_msg) == 2 and not re.search(r'\D', split_msg[1]) and re.search(r'[0-9]', split_msg[1]):
            num_cards = int(re.match(r'[0-9]', split_msg[1]).string)
            new_deck = Commands.DECK
            shuffle(new_deck)
            joined_cards = ' \x0F, '.join(map(str, [i for i in new_deck[1:num_cards + 1]]))
            conn.send_msg(msg['target'], f"{joined_cards}")
        else:
            player_card_list = []
            new_deck = Commands.DECK
            shuffle(new_deck)
            split_msg.pop(0)
            for i in range(len(split_msg)):
                player_card_list.append(f"{split_msg[i]}: {new_deck.pop()} \x0F")
            conn.send_msg(msg['target'], f"{', '.join(map(str, player_card_list))}")
