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
    ghost_info = state.getGhostStates()

    if (x, y) in capsules:
      return 50
    elif state.hasFood(x,y):
      return 10
    elif (x, y) in ghosts:
      if ghost_info[ghosts.index((x,y))].scaredTimer > 0:
        return 100
      else:
        return -10
    else:
      return 0


  def bestDirection(self, state, legalActions):
    x, y = state.getPacmanPosition()
    scores = dict()

    for action in legalActions:
      if action == Directions.NORTH:
        p1 = self.evaluateDirection(state, x+1, y+1)
        p2 = self.evaluateDirection(state, x, y+1)
        p3 = self.evaluateDirection(state, x-1, y+1)
        if p1 == -10 or p2 == -10 or p3 == -10:
          scores[action] = -10
        else:
          scores[action] = p2
      elif action == Directions.EAST:
        p1 = self.evaluateDirection(state, x+1, y+1)
        p2 = self.evaluateDirection(state, x+1, y)
        p3 = self.evaluateDirection(state, x+1, y-1)
        if p1 == -10 or p2 == -10 or p3 == -10:
          scores[action] = -10
        else:
          scores[action] = p2
      elif action == Directions.SOUTH:
        p1 = self.evaluateDirection(state, x+1, y-1)
        p2 = self.evaluateDirection(state, x, y-1)
        p3 = self.evaluateDirection(state, x-1, y-1)
        if p1 == -10 or p2 == -10 or p3 == -10:
          scores[action] = -10
        else:
          scores[action] = p2
      elif action == Directions.WEST:
        p1 = self.evaluateDirection(state, x-1, y+1)
        p2 = self.evaluateDirection(state, x-1, y)
        p3 = self.evaluateDirection(state, x-1, y-1)
        if p1 == -10 or p2 == -10 or p3 == -10:
          scores[action] = -10
        else:
          scores[action] = p2

    best_action = max(scores.items(), key=lambda x: x[1])

    best_directions = []
    for k, v in scores.items():
      if v == best_action[1]:
        best_directions.append(k)

    return random.choice(best_directions)


  def getAction(self, state):
    "Get action from moveHistory or chooses best direction based on evaluation"
    legalActions = state.getLegalPacmanActions()
    move = self.bestDirection(state, legalActions)

    if len(self.moveHistory['actions']) > 0:
      if self.moveHistory['actions'][0][-1] in legalActions:
        move = self.moveHistory['actions'].pop(0)[-1]

    return move