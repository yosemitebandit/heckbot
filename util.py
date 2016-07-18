"""Various functions.."""


all_values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
all_suits = ('C', 'S', 'D', 'H')


def build_full_deck():
  return [v + s for v in all_values for s in all_suits]


def evaluate_trick(trick, leader_index, trump_suit):
  """Evaluate a trick and return the index of the winning card."""
  # Check first for trump.
  if trump_suit:
    trump_cards = [card for card in trick if trump_suit in card]
    if len(trump_cards) == 1:
      winning_card = trump_cards[0]
    elif len(trump_cards) > 1:
      trump_values = [c[:-1] for c in trump_cards]
      indices = [all_values.index(v) for v in trump_values]
      sorted_cards = sorted(zip(trump_values, indices), key=lambda v: v[1])
      winning_value = sorted_cards[-1][0]
      winning_card = (winning_value + trump_suit).upper()
  # No trump present.
  if not trump_suit or not trump_cards:
    suit_lead = trick[leader_index][-1]
    suited_cards = [card for card in trick if suit_lead in card]
    if len(suited_cards) == 1:
      winning_card = suited_cards[0]
    else:
      suited_values = [c[:-1] for c in suited_cards]
      indices = [all_values.index(v) for v in suited_values]
      sorted_cards = sorted(zip(suited_values, indices), key=lambda v: v[1])
      winning_value = sorted_cards[-1][0]
      winning_card = (winning_value + suit_lead).upper()
  # Return the index
  return trick.index(winning_card)
