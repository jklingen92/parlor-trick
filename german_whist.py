from dataclasses import dataclass
import random
import time
import os

from cards import CardList, FrenchSuitedDeck, SmallFrenchSuitedDeck
from game import GameState, TwoPlayerGame, VariableDeckGameMixin, TargetScoreGameMixin
from player import HumanPlayer, Player, RandomPlayer






@dataclass
class SmallGermanWhistState(GameState):

    score: int = 0
    trump: 
    

    
@dataclass
class 



class GermanWhist(VariableDeckGameMixin, TargetScoreGameMixin, TwoPlayerGame):

    deck_class = FrenchSuitedDeck
    
    def get_target_score(self):
        return (self.scoring_tricks // 2) * 3

    def setup(self):
        if self.deck_size % 4 != 0:
            raise ValueError("Deck must contain multiple of 4 number of cards.")
        self.scoring_tricks = self.deck_size / 4
        
        self.round_count = 0
        class DynamicRoundClass(GermanWhistRound):
            deck_class = self.deck_class

        self.round_class = DynamicRoundClass

    def get_header(self):
         return (
            f"""
{self.players[0].name:>20}{self.players[1].name:>20}               
{self.scores[self.players[0]]:20}{self.scores[self.players[1]]:20}               

-----------------------------------------------------------
Round {self.round_count}
"""
        )

    def play(self):
        while not self.winner:
            self.round_count += 1
            round = self.round_class(header=self.get_header(), players=self.players)
            round.play()
            base_score = round.scores[round.winner] - (self.scoring_tricks // 2)
            if round.scores[round.loser] == 0:
                self.score(round.winner, base_score + base_score // 2)
            else:
                self.score(round.winner, base_score)
        print(f"{self.winner} wins!")

    def determine_winner(self):
        for player in self.players:
            if self.scores[player] >= self.target_score:
                return player
        return None
            

class GermanWhistRound(VariableDeckGameMixin, TwoPlayerGame):
    
    def __init__(self, *args, **kwargs) -> None:
        self.header = kwargs.pop("header", "")
        return super().__init__(*args, **kwargs)

    def setup(self):
        self.scoring_tricks = self.deck_size // 4
        self.deck = self.deck_class()
        self.deck.shuffle()

        # Choose dealer
        self.dealer = random.choice(self.players)
        print(f"{self.dealer.name} is selected as the dealer")
        self.leader = self.players[0] if self.players[0] != self.dealer else self.players[1]
        print(f"{self.players[0].name} will play first")

        # Deal and sort hands
        hand0 = []
        hand1 = []
        for _ in range(self.scoring_tricks):
            hand0.append(self.deck.draw())
            hand1.append(self.deck.draw())

        self.hands = {
            self.leader: CardList(hand0),
            self.dealer: CardList(hand1)
        }

        for hand in self.hands.values():
            hand.sort()

        self.top_card = self.deck.flip()
        print(f"{self.dealer.name} flips the {self.top_card}")
        self.trump = self.top_card.suit
        print(f"Trump is set to {self.trump}")

        self.trick_count = 0
        self.current_trick = None
        return
    
    def determine_winner(self):
        if sum(self.scores.values()) == self.scoring_tricks and self.deck.empty and all(hand.empty for hand in self.hands.values()):
            return self.point_leader
        return None

    def print_game(self):
        os.system("clear")
        print(self.header)
        print(
            f"""
{self.players[0].name:>20}{self.players[1].name:>20}               
{self.scores[self.players[0]]:20}{self.scores[self.players[1]]:20}               

Trump: {self.trump}
-----------------------------------------------------------
Trick {self.trick_count}

Top Card: {self.top_card}
"""
        )

    def play(self):
        leader = self.leader
        follower = self.dealer
        self.print_game()

        # Foreplay
        for i in range(1, self.scoring_tricks + 1):
            self.trick_count = i
            trick = GermanWhistTrick(self.hands, self.trump, players=[leader, follower])
            trick.play()
            leader = trick.winner
            follower = trick.loser
            self.hands[leader].add(self.deck.draw())
            self.hands[follower].add(self.deck.draw())
            print(f"{trick.winner.name} wins the trick")
            time.sleep(1)
            self.top_card = self.deck.flip()
            self.print_game()

        for i in range(self.scoring_tricks + 1, self.scoring_tricks * 2 + 1):
            self.trick_count = i
            trick = GermanWhistTrick(self.hands, self.trump, players=[leader, follower])
            trick.play()
            leader = trick.winner
            follower = trick.loser
            self.score(leader)
            print(f"{trick.winner.name} wins the trick and scores")
            time.sleep(1)
            self.print_game()
        return

        
class GermanWhistTrick(TwoPlayerGame):

    def __init__(self, hands, trump, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hands = hands
        self.trump = trump

    def determine_winner(self):
        for player in self.players:
            if self.scores[player] == 1:
                return player
        return None

    def play(self):
        lead_hand = self.hands[self.players[0]]
        follow_hand = self.hands[self.players[1]]

        lead = lead_hand.pick(self.players[0].choose_play(lead_hand))
        print(f"{self.players[0].name} plays {lead}")

        legal_plays = CardList([card for card in follow_hand.cards if card.suit == lead.suit])
        if legal_plays.empty:
            legal_plays = follow_hand
        follow = legal_plays.cards[self.players[1].choose_play(legal_plays)]
        follow = follow_hand.pick(follow_hand.cards.index(follow))
        print(f"{self.players[1].name} plays {follow}")

        if lead.suit == follow.suit:
            if lead.rank > follow.rank:
                self.score(self.players[0])
            else:
                self.score(self.players[1])
        elif follow.suit == self.trump:
            self.score(self.players[1])
        else:
            self.score(self.players[0])
        return

    
class SmallDeckGermanWhist(GermanWhist):

    deck_class = SmallFrenchSuitedDeck


if __name__ == "__main__":
    os.system("clear")
    player_name = input("Enter your name: ")
    print("Let's play German whist!")
    # time.sleep(2)
    os.system("clear")
    SmallDeckGermanWhist(players=[HumanPlayer(player_name), RandomPlayer("Computer")]).play()
