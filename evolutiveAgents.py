import cPickle
import random
from game import Agent, Directions

class EvolutiveAgent(Agent):
  def __init__(self, moveHistory):
    f = open(moveHistory)
    self.moveHistory = cPickle.load(f)
    f.close()

  def goToFood(self, state):
    x,y = state.getPacmanPosition()
    legalActions = state.getLegalPacmanActions()

    if Directions.EAST in legalActions and state.data.food[x+1][y]:
      return Directions.EAST
    elif Directions.NORTH in legalActions and state.data.food[x][y+1]:
      return Directions.NORTH
    elif Directions.WEST in legalActions and state.data.food[x-1][y]:
      return Directions.WEST
    elif Directions.SOUTH in legalActions and state.data.food[x][y-1]:
      return Directions.SOUTH
    else:
      return None
  
  def getAction(self, state):
    "Get action from moveHistory or moves randomly"
    # prioritizes path with food
    move = self.goToFood(state)
    if move: return move

    # moves randomly if there is no food in the neighborhood and no more stored actions available
    move = random.choice(state.getLegalPacmanActions())

    if len(self.moveHistory['actions']) > 0:
      nextMove = self.moveHistory['actions'].pop(0)[-1]
      if nextMove in state.getLegalPacmanActions():
        move = nextMove
    return move