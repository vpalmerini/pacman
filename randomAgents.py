from game import Agent
import random

class RandomAgent(Agent):
  "A crazy agent that moves randomly"

  def getAction(self, state):
    "The agent receives a GameState (defined in pacman.py)."
    return random.choice(state.getLegalPacmanActions())

