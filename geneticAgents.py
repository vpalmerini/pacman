import cPickle
import random
from game import Agent, Directions

class GeneticAgent(Agent):
  def __init__(self, moveHistory):
    f = open(moveHistory)
    self.moveHistory = cPickle.load(f)
    f.close()


  def evaluateDirection(self, state, x, y):
    capsules = state.getCapsules()
    food = state.getFood()
    ghosts = state.getGhostPositions()

    if (x, y) in capsules:
      return 50
    elif state.hasFood(x,y):
      return 10
    elif (x, y) in ghosts:
      return -10
    else:
      return 0


  def bestDirection(self, state, legalActions):
    x, y = state.getPacmanPosition()
    scores = dict()

    for action in legalActions:
      if action == Directions.NORTH:
        scores[action] = self.evaluateDirection(state, x, y+1)
      elif action == Directions.EAST:
        scores[action] = self.evaluateDirection(state, x+1, y)
      elif action == Directions.SOUTH:
        scores[action] = self.evaluateDirection(state, x, y-1)
      elif action == Directions.WEST:
        scores[action] = self.evaluateDirection(state, x-1, y)

    return max(scores, key=lambda key: scores[key])


  def getAction(self, state):
    "Get action from moveHistory or chooses best direction based on evaluation"
    legalActions = state.getLegalPacmanActions()
    move = self.bestDirection(state, legalActions)

    if len(self.moveHistory['actions']) > 0:
      if self.moveHistory['actions'][0][-1] in legalActions:
        move = self.moveHistory['actions'].pop(0)[-1]

    return move