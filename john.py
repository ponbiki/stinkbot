class John:

    players = 0

    def __init__(self, player_name):
        """

        :param player_name:
        """
        self.voice = {
            'voice': player_name,
            'willpower': 0,
            'skills': [],
            'obsessions': {
                'level1': '',
                'level2': '',
                'level3': ''
            }
        }

    def add_player(self, player_name):
        pass

    def __del__(self):
        pass
