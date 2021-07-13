import random

from game import Agent
from pacman import Directions

class QAgent(Agent):
  def __init__(self, numGames = 1000, learningRate = 0.8, explorationRate = 0.8, discountFactor = 0.5):
    self.learning_rate = float(learningRate)
    self.exploration_rate = float(explorationRate)
    self.discount_factor = float(discountFactor)
    self.num_games = int(numGames)
    self.episodes = 0
    self.q_table = dict()
    self.prev_position = None
    self.prev_action = None
    self.prev_score = 0
    self.cumulativeReward = 0
    self.rewards = []
    self.cumulativeActions = 0
    self.num_actions = []
    self.scores = []
  
  def bellman_equation(self, state, final = False):
    position = state.getPacmanPosition()

    max_q_value = 0
    if not final:
      max_q_value = max(list(self.q_table[position].values()))

    reward = state.getScore() - self.prev_score
    self.cumulativeReward += reward
    self.q_table[self.prev_position][self.prev_action] += (self.learning_rate * (reward + self.discount_factor * max_q_value - self.q_table[self.prev_position][self.prev_action]))


  def getAction(self, state):
    legalActions = state.getLegalPacmanActions()
    pacmanPosition = state.getPacmanPosition()

    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    if pacmanPosition not in self.q_table:
      self.q_table[pacmanPosition] = dict()
      for action in legalActions:
        if action not in self.q_table[pacmanPosition]:
          self.q_table[pacmanPosition][action] = 0

    if self.prev_position:
      self.bellman_equation(state)

    self.prev_position = pacmanPosition

    if random.random() < self.exploration_rate:
      self.prev_action = random.choice(legalActions)
    else:
      max_q_action = None
      for action in legalActions:
        if max_q_action == None:
          max_q_action = action
        if self.q_table[pacmanPosition][action] > self.q_table[pacmanPosition][max_q_action]:
          max_q_action = action
      self.prev_action = max_q_action
    
    self.prev_score = state.getScore()
    self.cumulativeActions += 1
    
    return self.prev_action


  def final(self, state):
    if self.prev_position:
      self.bellman_equation(state, final = True)

    self.prev_position = None
    self.prev_action = None
    self.scores.append(state.getScore())
    self.prev_score = 0
    self.rewards.append(self.cumulativeReward)
    self.cumulativeReward = 0
    self.num_actions.append(self.cumulativeActions)
    self.cumulativeActions = 0

    self.episodes += 1
    if self.episodes == self.num_games - 10:
      # stops learning and starts exploitation
      self.learning_rate = 0.3
      self.exploration_rate = 0.3

      results = dict()
      results['rewards'] = self.rewards
      results['actions'] = self.num_actions
      results['scores'] = self.scores
      print results

      self.rewards = []
      self.num_actions = []
      self.scores = []

    # exploitation mode - last 10 games
    elif self.episodes == self.num_games:
      results = dict()
      results['rewards'] = self.rewards
      results['actions'] = self.num_actions
      results['scores'] = self.scores
      print results

    elif self.episodes % 1000 == 0:
      if self.learning_rate > 0.3:
        self.learning_rate -= 0.1
      if self.exploration_rate > 0.3:
        self.exploration_rate -= 0.1

