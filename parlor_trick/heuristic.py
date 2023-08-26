import random
from parlor_trick.core import Heuristic


class UserInput(Heuristic):

    def decision(self, game, player, choices):
        print("-----------------------------------------")
        return self.solicit_choice(choices)
    
    def solicit_choice(self, choices):
        print("Plays:")
        for i, choice in enumerate(choices):
            print(f"({i}): {choice}")

        choice = None
        message = "Please select a play: \n"
        while choice is None or not 0 <= choice < len(choices):
            try:
                choice = int(input(message))
            except ValueError as e:
                pass
            message = "Please select a valid play: \n"
        
        return choice
    

class ShowHandUserInput(UserInput):
    
    def decision(self, game, player, choices):
        if len(choices) < player.hand.size:
            print("Hand:")
            player.hand.fan()
        return self.solicit_choice(choices)
    

class RandomDecision(Heuristic):

    def decision(self, game, player, choices):
        return random.randrange(len(choices))