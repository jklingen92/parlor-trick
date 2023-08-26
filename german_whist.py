from dataclasses import dataclass, field, asdict
import os
import time

from parlor_trick.cards import Card, CardList, FrenchSuitedCard, SmallFrenchSuitedDeck, Suit
from parlor_trick.core import Game, Heuristic, Player
from parlor_trick.heuristic import ShowHandUserInput, RandomDecision
from parlor_trick.utils import message



@dataclass
class GermanWhistRoundPlayer(Player):

    score: int = field(init=False, default=0)
    hand: CardList = field(default_factory=CardList)
    opposing_hand: CardList = field(default_factory=CardList)
    leading: bool = False

    def lead(self, game: Game) -> Card:
        self.leading = True
        return self.hand.pick(self.heuristic.decision(game, self, self.hand.cards))

    def follow(self, game: Game) -> Card:
        self.leading = False
        valid_plays = [card for card in self.hand.cards if card.suit == game.lead.suit]
        if len(valid_plays) > 0:
            play = valid_plays[self.heuristic.decision(game, self, valid_plays)]
            self.hand.remove(play)
            return play
        else:
            return self.hand.pick(self.heuristic.decision(game, self, self.hand.cards))


@dataclass
class Round(Game):

    player_class = GermanWhistRoundPlayer

    deck: SmallFrenchSuitedDeck = field(default_factory=SmallFrenchSuitedDeck)
    total_tricks: int = 14
    current_trick: int = 1
    trump: Suit | None = None
    prize: FrenchSuitedCard | None = None
    lead: FrenchSuitedCard | None = None
    played: CardList = field(default_factory=CardList)
    leader: Player | None = None
    follower: Player | None = None
    
    def setup(self):
        self.deck.shuffle()
        self.leader, self.follower = self.players.random_order()
        for _ in range(self.deck.size // 4):
            self.leader.hand.add(self.deck.draw())
            self.follower.hand.add(self.deck.draw())
        self.prize = self.deck.flip()
        self.trump = self.prize.suit
        self.display()

    @property
    def game_over(self):
        return self.current_trick > self.total_tricks
    
    def turn(self):
        if not self.deck.empty:
            return self.foreplay_turn()
        else:
            return self.scoring_turn()
        
    def basic_turn(self, leader_wins, follower_wins):
        self.lead = self.leader.lead(self)
        self.display()
        follow = self.follower.follow(self)

        message(f"{self.lead} vs {follow}")
        if self.lead.suit == follow.suit:
            if self.lead.rank > follow.rank:
                leader_wins()
            else:
                follower_wins()

        elif follow.suit == self.trump:
            follower_wins()

        else:
            leader_wins()

        self.current_trick += 1
        self.played.add(self.lead)
        self.played.add(follow)
        self.lead = None
        self.prize = self.deck.flip()
        self.display()
        return

    def foreplay_turn(self):

        def leader_wins():
            self.leader.hand.add(self.deck.draw())
            self.follower.opposing_hand.add(self.prize)
            self.follower.hand.add(self.deck.draw())
            message(f"{self.leader.name} wins the {self.prize}")
            message(f"{self.follower.name} draws a card")

        def follower_wins():
            self.follower.hand.add(self.deck.draw())
            self.leader.opposing_hand.add(self.prize)
            self.leader.hand.add(self.deck.draw())
            message(f"{self.follower.name} wins the {self.prize}")
            message(f"{self.leader.name} draws a card")
            winner = self.follower
            self.follower = self.leader
            self.leader = winner

        return self.basic_turn(leader_wins, follower_wins)
        
    
    def scoring_turn(self):

        def leader_wins():
            self.leader.score += 1
            message(f"{self.leader.name} wins the trick")

        def follower_wins():
            self.follower.score += 1
            message(f"{self.follower.name} wins the trick")
            winner = self.follower
            self.follower = self.leader
            self.leader = winner

        return self.basic_turn(leader_wins, follower_wins)

    @property
    def winner(self):
        if self.game_over:
            return self.leader if self.leader.score > self.follower.score else self.follower

    def display(self):
        os.system('clear')
        print(f"""Trick {self.current_trick} of {self.total_tricks}
{''.join([f'{player.name}: {player.score}          ' for player in self.players.all()])}
Trump: {self.trump}
Cards remaining: {self.deck.size}
Prize: {self.prize or 'score'}
{f'{self.leader.name} led {self.lead}' if self.lead else f'{self.leader.name} will lead'}
""")


@dataclass
class GermanWhistGamePlayer(Player):

    score: int = field(init=False, default=0)


@dataclass
class GermanWhist(Game):

    player_class = GermanWhistGamePlayer

    goal: int

    @property
    def game_over(self):
        return self.winner is not None
    
    def wins(self, player: Player) -> bool:
        return player.score >= self.goal

    @property
    def winner(self):
        for player in self.players.all():
            if self.wins(player):
                return player

    def turn(self):
        r = Round()
        r.add_players(self.players.all())
        r.play()
        winner = r.winner
        round_score = r.winner.score
        print(round_score)
        self.score_game(self.players.get_by_uuid(winner.uuid), round_score)
        message(''.join([f'{player.name}: {player.score}          ' for player in self.players.all()]))
        time.sleep(3)

    def score_game(self, player: Player, round_score: int) -> None:
        if round_score == 7:
            player.score += 6
        else:
            player.score += round_score - 3


if __name__ == "__main__":
    os.system("clear")
    player_name = input("Enter your name: ")
    message("Let's play German whist!")
    os.system("clear")
    game = GermanWhist(7)
    players=[
        Player(player_name, ShowHandUserInput()), 
        Player("Computer", RandomDecision())
    ]
    game.add_players(players)
    game.play()
    message(f"{game.winner.name} wins!")
