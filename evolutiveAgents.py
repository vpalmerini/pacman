import cPickle
import random
from game import Agent

class EvolutiveAgent(Agent):
  def __init__(self, moveHistory):
    f = open(moveHistory)
    self.moveHistory = cPickle.load(f)
    f.close()
  
  def getAction(self, state):
    "Get action from moveHistory or moves randomly"
    move = random.choice(state.getLegalPacmanActions())

    if len(self.moveHistory['actions']) > 0:
      nextMove = self.moveHistory['actions'].pop(0)[-1]
      if nextMove in state.getLegalPacmanActions():
        move = nextMove
    return move