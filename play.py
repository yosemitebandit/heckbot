"""Plays Oh Hell."""

import random


players = 5
cards_to_deal = 9

suits = ('club', 'spade', 'diamond', 'heart')
values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
deck = ['%s-%s' % (v, s) for s in suits for v in values]

random.shuffle(deck)

hands = []
for player in range(players):
  hand = [deck.pop() for _ in range(cards_to_deal)]
  hands.append(hand)
