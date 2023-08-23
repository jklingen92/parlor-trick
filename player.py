from dataclasses import dataclass
import random


@dataclass
class Player:
    
    name: str
    
    def play(self, *args, **kwargs):
        play = self.choose_play(*args, **kwargs)
        self.hand = [card for card in self.hand if card.rank != play.rank or card.suit != play.suit]
        return play

    def decision(self, plays) -> int:
        pass


class HumanPlayer(Player):
    
    def choose_play(self, plays):
        print("Select a play:")
        plays.fan()

        choice = None
        message = "Please select a play: \n"
        while choice is None or not 0 <= choice < plays.size:
            try:
                choice = int(input(message))
            except ValueError as e:
                pass
            message = "Please select a valid play: \n"
        
        return choice
    
  
class RandomPlayer(Player):

    def choose_play(self, plays):
        return random.randint(0, plays.size - 1)