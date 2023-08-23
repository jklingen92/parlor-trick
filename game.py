from dataclasses import dataclass
from player import Player
from utils import ImproperlyConfigured, RequiredAttributeClass





@dataclass
class MultiplayerScoredGameState:

    players: tuple(Player)

    @property
    def winner(self):
        pass

@dataclass
class ScoreMixin:







class Game:

    default_score = 0
    min_players = None
    max_players = None

    def __init__(self, *args, **kwargs) -> None:
        try:
            self.players = kwargs.pop("players")
        except KeyError as e:
            raise ImproperlyConfigured(f"{self.__class__.__name__} must receive a players keyword argument.")
        
        if self.max_players and len(self.players) > self.max_players:
            raise ImproperlyConfigured(f"{self.__class__.__name__} can play no more than {self.max_players} but received {len(self.players)} players")
        elif self.min_players and len(self.players) < self.min_players:
            raise ImproperlyConfigured(f"{self.__class__.__name__} must have {self.min_players} but received {len(self.players)} players")

        self.state = object

        self.scores = {
            player: self.default_score for player in self.players
        }
        self.setup()
        return
    
    def setup(self) -> None:
        pass
            
    def score(self, player, points=1):
        self.scores[player] += points

    def play(self):
        self.setup()
        return self.play_game()
    
    def play_game(self):
        pass
    
    

    @property
    def winner(self):
        return self.determine_winner()
    

class TwoPlayerGame(Game):

    min_players = 2
    max_players = 2

    def other_player(self, player):
        return self.players[0] if self.players[0] != player else self.players[1]

    @property
    def point_leader(self):
        return self.players[0] if self.scores[self.players[0]] > self.scores[self.players[1]] else self.players[1]

    @property
    def loser(self):
        return self.other_player(self.winner)
    

@dataclass
class TargetScoreGameState:

    target_score: int


@dataclass
class VariableDeckGameMixin(RequiredAttributeClass):

    deck_class = None
    required_attributes = ["deck_class"]
    
    @property
    def deck_size(self):
        return self.deck_class.get_deck_size()
