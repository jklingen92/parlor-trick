import random
from dataclasses import dataclass, field

@dataclass
class Card:
    pass

@dataclass
class CardList:

    cards: list[Card] = field(default_factory=list)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def sort(self) -> None:
        self.cards.sort()

    def fan(self) -> None:
        for card in self.cards:
            print(card)

    def pick(self, n) -> Card:
        return self.cards.pop(n)
    
    def remove(self, card) -> None:
        self.cards.pop(self.cards.index(card))
    
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
    
    def flip(self) -> Card | None:
        if not self.empty:
            return self.cards[0]
        else:
            return None
    
    def generate_cards(self) -> list[Card]:
        raise NotImplemented

    @classmethod
    def get_deck_size(cls):
        self = cls()
        self.generate_cards()
        return self.size


@dataclass
class Rank:

    value: int
    name: str | None = None

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
    
    def __post_init__(self):
        if self.name is None:
            self.name = str(self.value)


@dataclass
class Suit:

    name: str

    def __repr__(self) -> str:
        return self.name


FRENCH_SUITS = [Suit("Diamonds"), Suit("Clubs"), Suit("Hearts"), Suit("Spades")]
FRENCH_RANKS = [*[Rank(n) for n in range(2, 11)], Rank(11, "Jack"), Rank(12, "Queen"), Rank(13, "King"), Rank(14, "Ace")]


@dataclass
class FrenchSuitedCard(Card):

    rank: Rank
    suit: Suit

    def __str__(self):
      return f"{self.rank.name} of {self.suit.name}"
    
    def __repr__(self) -> str:
        return f"{self.rank.name} of {self.suit.name}"
    
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

    def generate_cards(self) -> list[Card]:
        return [FrenchSuitedCard(rank, suit) for rank in FRENCH_RANKS for suit in FRENCH_SUITS]
    
class SmallFrenchSuitedDeck(Deck):

    def generate_cards(self) -> list[Card]:
        return [FrenchSuitedCard(rank, suit) for rank in FRENCH_RANKS[6:] for suit in FRENCH_SUITS]