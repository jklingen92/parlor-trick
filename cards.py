import random
from dataclasses import dataclass, field

@dataclass
class Card:
    pass

@dataclass
class CardList:

    cards: list[Card]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def sort(self) -> None:
        self.cards.sort()

    def fan(self) -> None:
        for i, card in enumerate(self.cards):
            print(f"({i}) - {card}")

    def pick(self, n) -> Card:
        return self.cards.pop(n)
    
    def add(self, card) -> None:
        self.cards.append(card)
        self.sort()

    @property
    def size(self):
        return len(self.cards)

    @property
    def remaining_cards(self) -> int:
        return len(self.cards)
    
    @property
    def empty(self) -> bool:
        return self.remaining_cards == 0
    

class Deck(CardList):

    def __init__(self) -> None:
        cards = self.generate_cards()
        return super().__init__(cards)

    def draw(self) -> Card:
        return self.pick(0)
    
    def flip(self) -> Card:
        if not self.empty:
            return self.cards[0]
        else:
            return None
    
    def generate_cards(self) -> [Card]:
        pass

    @classmethod
    def get_deck_size(cls):
        self = cls()
        self.generate_cards()
        return self.size


@dataclass
class Rank:

    name: str
    value: int


    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Rank) and other.name == self.name
    
    def __lt__(self, other):
        if isinstance(other, Rank):
            return self.value < other.value
        return self.value < int(other)
    
    def __gt__(self, other):
        if isinstance(other, Rank):
            return self.value > other.value
        return self.value > int(other)


class Jack(Rank):
    name = "Jack"
    value = 11


class Queen(Rank):
    name = "Queen"
    value = 12


class King(Rank):
    name = "King"
    value = 13


class Ace(Rank):
    name = "Ace"
    value = 14



FRENCH_SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
FRENCH_RANKS = [Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(), '8', '9', '10', Jack(), Queen(), King(), Ace()]

class FrenchSuitedCard(Card):

    def __init__(self, rank, suit, *args, **kwargs) -> None:
        self.rank = rank
        self.suit = suit
        super().__init__(*args, **kwargs)
        return

    def __str__(self):
      return f"{self.rank.name if isinstance(self.rank, Rank) else self.rank} of {self.suit}"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        else:
            return FRENCH_SUITS.index(self.suit) < FRENCH_SUITS.index(other.suit)
    
    def __gt__(self, other):
        if self.suit == other.suit:
            return self.rank > other.rank
        else:
            return FRENCH_SUITS.index(self.suit) > FRENCH_SUITS.index(other.suit)


class FrenchSuitedDeck(Deck):

    def generate_cards(self) -> [Card]:
        return [FrenchSuitedCard(rank, suit) for rank in FRENCH_RANKS for suit in FRENCH_SUITS]
    
class SmallFrenchSuitedDeck(Deck):

    def generate_cards(self) -> [Card]:
        return [FrenchSuitedCard(rank, suit) for rank in FRENCH_RANKS[6:] for suit in FRENCH_SUITS]