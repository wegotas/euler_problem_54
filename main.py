from classes import *

round_playment = RoundPlayment()

with open("poker.txt") as input_data:
    for line in input_data.readlines():
        round_playment.set_new_players(line)
        round_playment.play()
    print('player {0} won {1} times'.format(round_playment.first_player_name,
                                            round_playment.first_player_winning_count))
    print('player {0} won {1} times'.format(round_playment.second_player_name,
                                            round_playment.second_player_winning_count))
