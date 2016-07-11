"""Plays "Oh Hell," the bidding and trumping card game.

Usage:
  python play.py
  python play.py <number_of_players> <my_cards> <trump_card>
                 <distance_from_leader>

Todo:
 * don't play randomly :|
 * multi-deck
"""

import random
import sys

import util


# Take the input params.
if len(sys.argv) == 5:
  number_of_players = int(sys.argv[1])
  my_cards = [c.upper() for c in sys.argv[2].split(' ')]
  trump_card = sys.argv[3].upper()
  my_distance_from_leader = int(sys.argv[4])
else:
  number_of_players = int(raw_input('number of players?\n'))
  my_cards = [c.upper() for c in raw_input('your cards?\n').split(' ')]
  trump_card = raw_input('trump card?\n').upper()
  my_distance_from_leader = int(raw_input('distance from leader?\n'))
trump_suit = trump_card[-1]


# Build the rest of the deck.
deck = util.build_full_deck()
remaining_deck = []
for card in deck:
  if card not in my_cards and card != trump_card:
    remaining_deck.append(card)


class Player(object):
  def __init__(self):
    self.hand = []
    self.is_leader = False
    self.is_me = False

  def __repr__(self):
    return 'Player: is_leader: %s, is_me: %s, hand: %s' % (
      self.is_leader, self.is_me, self.hand)


# Set the initial leader.
players = [Player() for _ in range(number_of_players)]
players[-1].is_me = True
my_index = number_of_players - 1
leader_index = my_index - my_distance_from_leader
players[leader_index].is_leader = True


# Simulate random rounds until the average of won tricks converges.
iterations, total_tricks_won, previous_average_tricks_won = 0, 0, 0
while True:
  # Deal to the other players.
  random.shuffle(remaining_deck)
  card_index = 0
  for i in range(len(my_cards)):
    for player in players:
      if player.is_me:
        continue
      next_card = remaining_deck[card_index]
      player.hand.append(next_card)
      card_index += 1
  # Setup my hand.
  players[-1].hand = list(my_cards)

  # for p in players:
    # print p
  # raw_input()

  # Play through all the tricks in the round.
  my_tricks_won = 0
  for trick_index in range(len(my_cards)):
    # Find the leader.
    for i, p in enumerate(players):
      if p.is_leader:
        current_player_index = i
        leader_index = i
        break
    # Setup the trick.
    trick = [None for _ in range(number_of_players)]
    for _ in range(number_of_players):
      current_player = players[current_player_index]
      if not any(trick):
        # Play the lead card.
        trick[current_player_index] = current_player.hand.pop()
      else:
        # Play the other cards, following suit if possible.
        suit_lead = trick[leader_index][-1]
        suited_cards = [card for card in current_player.hand
                        if suit_lead in card]
        if suited_cards:
          card_to_play = suited_cards[0]
          index = current_player.hand.index(card_to_play)
          current_player.hand.pop(index)
          trick[current_player_index] = card_to_play
        else:
          trick[current_player_index] = current_player.hand.pop()
      current_player_index = (current_player_index + 1) % number_of_players
    winner_index = util.evaluate_trick(trick, leader_index, trump_suit)
    # print leader_index, trick, winner_index
    # raw_input()
    # Tally wins
    if players[winner_index].is_me:
      my_tricks_won += 1
    # Set the new leader.
    for p in players:
      p.is_leader = False
    players[winner_index].is_leader = True

  # Tally all the tricks won so far and take the average.
  total_tricks_won += my_tricks_won
  iterations += 1
  if iterations % 100 == 0:
    current_average_tricks_won = float(total_tricks_won) / iterations
    delta =  abs(previous_average_tricks_won - current_average_tricks_won)
    if delta < 1e-4:
      break
    previous_average_tricks_won = float(total_tricks_won) / iterations

print 'recommended bid: %0.5f' % current_average_tricks_won
print 'rounds simulated: %s' % iterations
