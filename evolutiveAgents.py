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
    legalActions = state.getLegalPacmanActions()
    move = random.choice(legalActions)

    if len(self.moveHistory['actions']) > 0:
      if self.moveHistory['actions'][0][-1] in legalActions:
        move = self.moveHistory['actions'].pop(0)[-1]
    return move