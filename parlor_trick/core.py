from dataclasses import asdict, dataclass, field
import random
from typing import Any
from uuid import UUID, uuid4


class Heuristic:

    def decision(self, game, player, choices: list[Any]) -> Any:
        raise NotImplemented


@dataclass
class Player:
    
    name: str
    heuristic: Heuristic
    uuid: UUID = field(default_factory=uuid4)


class PlayerManager:

    def __init__(self, players: list[Player]) -> None:
        self._players = players

    @property
    def count(self) -> int:
        return len(self._players)
    
    def all(self) -> list[Player]:
        return self._players
    
    def random(self) -> Player:
        return random.choice(self._players)
    
    def random_order(self) -> list[Player]:
        return random.sample(self._players, len(self._players))
    
    def asdict(self) -> list[dict]:
        return [asdict(player) for player in self._players]


class Game:
    
    player_class = None

    def add_players(self, players: list[Player]) -> None:
        self.players = PlayerManager(
            [self.player_class(**asdict(player)) for player in players]
        )

    def setup(self) -> None:
        return

    @property
    def game_over(self) -> bool:
        raise NotImplemented

    def play(self) -> None:
        self.setup()
        while not self.game_over:
            self.turn()
        return

    def turn(self):
        raise NotImplemented
