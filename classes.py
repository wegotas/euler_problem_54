class RoundPlayment:

    def __init__(self):
        self.first_player_name = 'John Doe'
        self.first_player_hand = None
        self.first_player_winning_count = 0
        self.second_player_name = 'Jane Doe'
        self.second_player_hand = None
        self.second_player_winning_count = 0

    def set_new_players(self, card_string):
        card_string_array = card_string.strip().replace('ï', '').replace('»', '').replace('¿', '').split(' ')
        self.first_player_hand = PlayerHand(
            player_name=self.first_player_name,
            first_card_string=card_string_array[0],
            second_card_string=card_string_array[1],
            third_card_string=card_string_array[2],
            fourth_card_string=card_string_array[3],
            fifth_card_string=card_string_array[4]
        )
        self.second_player_hand = PlayerHand(
            player_name=self.second_player_name,
            first_card_string=card_string_array[5],
            second_card_string=card_string_array[6],
            third_card_string=card_string_array[7],
            fourth_card_string=card_string_array[8],
            fifth_card_string=card_string_array[9]
        )


    def play(self):
        for method_to_call in PlayerHand.methods_to_call:
            winner_found, winner = self._compare_combo(method_to_call)
            if winner_found:
                if winner:
                    if winner.player_name == self.first_player_name:
                        self.first_player_winning_count += 1
                    elif winner.player_name == self.second_player_name:
                        self.second_player_winning_count +=1
                break

    def _compare_combo(self, method_to_call):
        # shortenings - fp(first player), sp(second player)
        fp_is, fp_first_value, fp_second_value, fp_third_value, fp_fourth_value, fp_fifth_value = getattr(
            self.first_player_hand, method_to_call)()
        fp_values = [fp_first_value, fp_second_value, fp_third_value, fp_fourth_value, fp_fifth_value]
        sp_is, sp_first_value, sp_second_value, sp_third_value, sp_fourth_value, sp_fifth_value = getattr(
            self.second_player_hand, method_to_call)()
        sp_values = [sp_first_value, sp_second_value, sp_third_value, sp_fourth_value, sp_fifth_value]
        if fp_is and sp_is:
            # combo tie braker
            for fp_value, sp_value in zip(fp_values, sp_values):
                if fp_value and sp_value:
                    if fp_value > sp_value:
                        return True, self.first_player_hand
                    elif sp_value > fp_value:
                        return True, self.second_player_hand
            return False, None
        elif fp_is and not sp_is:
            return True, self.first_player_hand
        elif not fp_is and sp_is:
            return True, self.second_player_hand
        # No one wins this combo comparison
        return False, None

class PlayerHand:

    '''
    methods_to_call = [
        'is_royal_flush',
        'is_straight_flush',
        'is_four_of_a_kind',
        'is_full_house',
        'is_flush',
        'is_straight',
        'is_three_of_a_kind',
        'is_two_pairs',
        'is_pair'
    ]
    '''
    methods_to_call = [
        'check_royal_flush',
        'check_straight_flush',
        'check_four_of_a_kind',
        'check_full_house',
        'check_flush',
        'check_straight',
        'check_three_of_a_kind',
        'check_two_pairs',
        'check_pair',
        'check_high_card'
    ]

    def __init__(self, first_card_string, second_card_string, third_card_string,
                 fourth_card_string, fifth_card_string, player_name='Unnamed player'):
        self.player_name = player_name
        self.hand = [
            Card(first_card_string),
            Card(second_card_string),
            Card(third_card_string),
            Card(fourth_card_string),
            Card(fifth_card_string)
        ]

    def is_royal_flush(self):
        royal_flush_combo = ['A', 'K', 'Q', 'J', 'T']
        for card in self.hand:
            if card.value in royal_flush_combo:
                royal_flush_combo.remove(card.value)
            else:
                return False
        return True

    def check_royal_flush(self):
        return self.is_royal_flush(), None, None, None, None, None

    def is_straight_flush(self):
        sorted_hand =self.sorted_value_list
        for indx in range(len(sorted_hand)-1):
            if abs(sorted_hand[indx].value_as_int - sorted_hand[indx + 1].value_as_int) != 1 \
                    or sorted_hand[indx].symbol != sorted_hand[indx + 1].symbol:
                return False
        return True

    def check_straight_flush(self):
        return self.is_straight_flush(), self.values_list_as_ints[0], None, None, None, None

    def is_four_of_a_kind(self):
        return 4 in self._get_value_pairs().values()

    def check_four_of_a_kind(self):
        four_of_a_kind_value_as_int = None
        sigleton_int = None
        four_of_a_kind_value_key = None
        is_four_of_a_kind = self.is_four_of_a_kind()
        if is_four_of_a_kind:
            value_pairs = self._get_value_pairs()
            for key, value in value_pairs.items():
                if value==4:
                    four_of_a_kind_value_key = key
                    four_of_a_kind_value_as_int = Card.values_as_ints[key]
            value_pairs.pop(four_of_a_kind_value_key)
            sigleton_int = Card.values_as_ints[list(value_pairs.keys())[0]]
        return is_four_of_a_kind, four_of_a_kind_value_as_int, sigleton_int, None, None, None

    def is_full_house(self):
        value_pairs = self._get_value_pairs()
        return 3 in value_pairs.values() and 2 in value_pairs.values()

    def check_full_house(self):
        three_of_a_kind_value_as_int = None
        two_of_a_kind_value_as_int = None
        three_of_a_kind_value_key = None
        is_full_house = self.is_full_house()
        if is_full_house:
            value_pairs = self._get_value_pairs()
            for key, value in value_pairs.items():
                if value==3:
                    three_of_a_kind_value_key = key
                    three_of_a_kind_value_as_int = Card.values_as_ints[key]
            value_pairs.pop(three_of_a_kind_value_key)
            two_of_a_kind_value_as_int = Card.values_as_ints[list(value_pairs.keys())[0]]
        return is_full_house, three_of_a_kind_value_as_int, two_of_a_kind_value_as_int, None, None, None

    def is_flush(self):
        symbol = self.hand[0].symbol
        for card in self.hand[2:]:
            if symbol != card.symbol:
                return False
        return True

    def check_flush(self):
        values_list_as_ints = self.values_list_as_ints
        return self.is_flush(), values_list_as_ints[0], values_list_as_ints[1], values_list_as_ints[2], \
               values_list_as_ints[3], values_list_as_ints[4]

    def is_straight(self):
        values_list_as_ints = self.values_list_as_ints
        for indx in range(len(values_list_as_ints) - 1):
            if abs(values_list_as_ints[indx] - values_list_as_ints[indx + 1]) != 1:
                return False
        return True

    def check_straight(self):
        return self.is_straight(), self.values_list_as_ints[0], None, None, None, None

    def is_three_of_a_kind(self):
        return 3 in self._get_value_pairs().values()

    def check_three_of_a_kind(self):
        three_of_a_kind_value_as_int = None
        three_of_a_kind_value_key = None
        higher_value = None
        lower_value = None
        is_three_of_a_kind = self.is_three_of_a_kind()
        if is_three_of_a_kind:
            value_pairs = self._get_value_pairs()
            for key, value in value_pairs.items():
                if value == 3:
                    three_of_a_kind_value_key = key
                    three_of_a_kind_value_as_int = Card.values_as_ints[key]
            value_pairs.pop(three_of_a_kind_value_key)
            if Card.values_as_ints[list(value_pairs.keys())[0]] > Card.values_as_ints[list(value_pairs.keys())[1]]:
                higher_value = Card.values_as_ints[list(value_pairs.keys())[0]]
                lower_value = Card.values_as_ints[list(value_pairs.keys())[1]]
            else:
                higher_value = Card.values_as_ints[list(value_pairs.keys())[1]]
                lower_value = Card.values_as_ints[list(value_pairs.keys())[0]]
        return is_three_of_a_kind, three_of_a_kind_value_as_int, higher_value, lower_value, None, None

    def is_two_pairs(self):
        counter = 0
        for value in self._get_value_pairs().values():
            if value == 2:
                counter += 1
        return counter == 2

    def check_two_pairs(self):
        is_two_pairs = self.is_two_pairs()
        higher_pair_value = None
        lower_pair_value = None
        singleton = None
        if is_two_pairs:
            values_of_pairs = []
            for value, qty in self._get_value_pairs().items():
                if qty == 2:
                    values_of_pairs.append(value)
            if Card.values_as_ints[values_of_pairs[0]] > Card.values_as_ints[values_of_pairs[1]]:
                higher_pair_value = Card.values_as_ints[values_of_pairs[0]]
                lower_pair_value = Card.values_as_ints[values_of_pairs[1]]
            else:
                higher_pair_value = Card.values_as_ints[values_of_pairs[1]]
                lower_pair_value = Card.values_as_ints[values_of_pairs[0]]
        return is_two_pairs, higher_pair_value, lower_pair_value, singleton, None, None

    def is_pair(self):
        for value in self._get_value_pairs().values():
            if value == 2:
                return True
        return False

    def check_pair(self):
        def singletons_as_ints(singletons_values):
            return sorted([Card.values_as_ints[singleton] for singleton in singletons], reverse=True)

        is_pair = self.is_pair()
        pair_value_as_int = None
        higher_value = None
        mid_value = None
        lower_value = None
        if is_pair and not self.is_full_house() and not self.is_two_pairs():
            singletons = []
            for value, qty in self._get_value_pairs().items():
                if qty == 2:
                    pair_value_as_int = Card.values_as_ints[value]
                elif qty == 1:
                    singletons.append(value)
            higher_value, mid_value, lower_value = singletons_as_ints(singletons)
        return is_pair, pair_value_as_int, higher_value, mid_value, lower_value, None

    def is_high_card(self):
        return True

    def check_high_card(self):
        values_list_as_ints = self.values_list_as_ints
        return self.is_high_card(), values_list_as_ints[0], values_list_as_ints[1], values_list_as_ints[2], \
               values_list_as_ints[3], values_list_as_ints[4]

    @property
    def winning_text(self):
        return "{0} has won the round".format(self.player_name)

    def _get_value_pairs(self):
        value_pairs = {}
        for card in self.hand:
            if card.value in value_pairs:
                value_pairs[card.value] += 1
            else:
                value_pairs[card.value] = 1
        return value_pairs

    @property
    def values_list(self):
        return [card.value for card in self.sorted_value_list]

    @property
    def values_list_as_ints(self):
        return [card.value_as_int for card in self.sorted_value_list]

    @property
    def sorted_value_list(self):
        return sorted(self.hand, key=lambda x: x.value_as_int, reverse=True)

    def __repr__(self):
        return "First card: {0},\r\nSecond card: {1},\r\nThird card: {2},\r\nFourth card: {3},\r\nFifth card: {4}"\
            .format(self.hand[0], self.hand[1], self.hand[2], self.hand[3], self.hand[4])

class Card:
    """
    Expected
    values: A - Ace, K - King, Q - Queen, J - Jack, T - Ten, 9, 8, 7, 6, 5, 4, 3, 2
    symbols: C - Club, D - Diamond, H - Heart, S - Spade
    """
    values_as_ints = {'A': 14, 'K': 13,'Q': 12,'J': 11,'T': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}

    def __init__(self, card_string):
        self.value = card_string[0]
        self.symbol = card_string[1]

    @property
    def value_as_int(self):
        return self.values_as_ints[self.value]

    def __repr__(self):
        return "Card class, Value: {0}, Symbol: {1}".format(self.value, self.symbol)