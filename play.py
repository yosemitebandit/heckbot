"""Plays "Oh Hell," the bidding and trumping card game.

Usage:
  python play.py

Todo:
 * don't play randomly :|
 * follow the lead
 * adjust who leads
"""

import random
import sys


# Take the input params.
number_of_players = int(raw_input('number of players?\n'))
my_cards = [c.upper() for c in raw_input('your cards?\n').split(' ')]
trump_card = raw_input('trump card?\n').upper()
trump_suit = trump_card[-1]
my_distance_from_leader = int(raw_input('distance from leader?\n'))


# Shuffle the deck.
all_values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
all_suits = ('C', 'S', 'D', 'H')
deck = [v + s for v in all_values for s in all_suits]
remaining_deck = []
for card in deck:
  if card not in my_cards and card != trump_card:
    remaining_deck.append(card)


# Simulate random rounds.
iterations, total_tricks_won, previous_average_tricks_won = 0, 0, 0
while True:
  # Deal to the other players.
  random.shuffle(remaining_deck)
  hands = []
  for player_index in range(number_of_players - 1):
    start_index = player_index * len(my_cards)
    end_index = (player_index + 1) * len(my_cards)
    hands.append([c for c in remaining_deck[start_index:end_index]])

  # Setup each trick.
  my_tricks_won = 0
  for hand_index, my_card in enumerate(my_cards):
    trick = []
    next_opposing_player = 0
    for player_index in range(number_of_players):
      if player_index == my_distance_from_leader:
        trick.append(my_card)
      else:
        trick.append(hands[next_opposing_player][hand_index])
        next_opposing_player += 1

    # Determine who wins the trick.
    trump_cards = [card for card in trick if trump_suit in card]
    if len(trump_cards) == 1:
      winning_card = trump_cards[0]
    elif len(trump_cards) > 1:
      trump_values = [c[:-1] for c in trump_cards]
      indices = [all_values.index(v) for v in trump_values]
      sorted_cards = sorted(zip(trump_values, indices), key=lambda v: v[1])
      winning_value = sorted_cards[-1][0]
      winning_card = (winning_value + trump_suit).upper()
    else:
      suit_lead = trick[0][-1]
      suited_cards = [card for card in trick if suit_lead in card]
      if len(suited_cards) == 1:
        winning_card = suited_cards[0]
      else:
        suited_values = [c[:-1] for c in suited_cards]
        indices = [all_values.index(v) for v in suited_values]
        sorted_cards = sorted(zip(suited_values, indices), key=lambda v: v[1])
        winning_value = sorted_cards[-1][0]
        winning_card = (winning_value + suit_lead).upper()
    if my_distance_from_leader == trick.index(winning_card):
      my_tricks_won += 1

  # Tally all the tricks won so far and the average.
  total_tricks_won += my_tricks_won
  iterations += 1
  if iterations % 100 == 0:
    current_average_tricks_won = float(total_tricks_won) / iterations
    delta =  abs(previous_average_tricks_won - current_average_tricks_won)
    if delta < 1e-6:
      break
    previous_average_tricks_won = float(total_tricks_won) / iterations

print 'estimated tricks you will take: %0.4f' % current_average_tricks_won
