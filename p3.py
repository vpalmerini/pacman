import sys, os, cPickle, itertools
from optparse import OptionParser
from pacman import readCommand, runGames
from layout import getLayout


class Individual:
  _id = itertools.count().next

  def __init__(self, score = float("inf"), win_percentage = 0, actions = [], food_count = 55, capsules_count = 2, actions_count = 0, fitness = 0):
    self.id = Individual._id()
    self.score = score
    self.win_percentage = win_percentage
    self.move_history = None
    self.actions = actions
    self.food_count = food_count
    self.capsules_count = capsules_count
    self.actions_count = actions_count
    self.fitness = fitness

class Generation:
  def __init__(self, _id = 0, individuals = []):
    self.id = _id
    self.individuals = list(reversed(sorted(individuals, key=lambda x: x.fitness)))

  def best_fitness(self):
    return self.individuals[0]

  def worst_fitness(self):
    return self.individuals[-1]

  def best_score(self):
    _max = max(self.individuals, key=lambda x: x.score)
    index = self.individuals.index(_max)
    return self.individuals[index]

  def worst_score(self):
    _min = min(self.individuals, key=lambda x: x.score)
    index = self.individuals.index(_min)
    return self.individuals[index]

  def win_percentage(self):
    wins_average = sum([x.win_percentage for x in self.individuals])
    return wins_average / len(self.individuals)

  def performance(self):
    print 'GENERATION {gen}'.format(gen=self.id)
    print 'Best Score: {best_score:.2f}'.format(best_score=self.best_score().score)
    print 'Worst Score: {worst_score:.2f}'.format(worst_score=self.worst_score().score)
    print 'Avg Score: {avg_score:.2f}'.format(avg_score=sum(ind.score for ind in self.individuals) / len(self.individuals))
    print 'Wins Percentage: {wins_percentage:.2f}'.format(wins_percentage=self.win_percentage())
    print 'Best Fitness: {best_fitness:.2f}'.format(best_fitness=self.best_fitness().fitness)
    print 'Worst Fitness: {worst_fitness:.2f}'.format(worst_fitness=self.worst_fitness().fitness)
    print 'Avg Fitness: {avg_fitness:.2f}'.format(avg_fitness=sum(ind.fitness for ind in self.individuals) / len(self.individuals))


def fitness(method, scores = [], wins = [], movements = []):
  methods = {
    'average_score': sum(scores) / len(scores),
    'number_of_wins': len([w for w in wins if w == True]),
    'average_score_by_movements_length': (sum(scores) / len(scores)) / len(movements)
  }

  return methods[method]


def play(args):
  _args = readCommand(args)
  games = runGames(**_args)
  return games

def evaluateGames(games, _fitness):
  """Get winner (or loser if none of them won) with the best score"""
  scores = [game.state.getScore() for game in games]
  wins = [game.state.isWin() for game in games]

  wins_index = [i for i, v in enumerate(wins) if v == True]
  best_index = 0
  if len(wins_index) > 0:
    best_score = wins_index[best_index]
    for i in range(1, len(wins_index)):
      if scores[i] > scores[best_index]:
        best_index = i
  else:
    best_score = max(scores)
    best_index = scores.index(best_score)

  # performance
  perf = dict()
  perf['score'] = scores[best_index]
  perf['win_percentage'] = float(wins.count(True)) / len(wins)
  perf['actions'] = games[best_index].moveHistory
  perf['food_count'] = [game.state.getNumFood() for game in games][best_index]
  perf['capsules_count'] = [len(game.state.getCapsules()) for game in games][best_index]
  perf['actions_count'] = len(games[best_index].moveHistory)
  perf['fitness'] = fitness(_fitness, scores, wins, games[best_index].moveHistory)

  return perf

def storeIndividual(individual, gen, layout):
  _dir = 'gen-{gen}'.format(gen=gen)
  if not os.path.exists(_dir):
    os.mkdir(_dir)

  file_name = '{dir}/ind-{id}'.format(dir=_dir, id=individual.id)
  f = file(file_name, 'w')
  
  individual.move_history = file_name
  components = {'layout': getLayout(layout), 'actions': individual.actions}
  cPickle.dump(components, f)
  f.close()

  return individual

def mutation(individual, threshold = 10):
  f = open(individual.move_history)
  components = cPickle.load(f)
  f.close()

  return Individual(actions=components['actions'][:-threshold])

def main(argv):
  usageStr = """"""
  parser = OptionParser(usageStr)

  parser.add_option('--numGen', type='int', default=100)
  parser.add_option('--numPop', type='int', default=50)
  parser.add_option('--layout', type='str', default='smallClassic')
  parser.add_option('--numGames', type='int', default=3)
  parser.add_option('--numSelection', type='int', default=50)
  parser.add_option('--fitness', type='str', default='average_score')

  options, junk = parser.parse_args(argv)

  args = dict()
  args['numGen'] = options.numGen
  args['numPop'] = options.numPop
  args['layout'] = options.layout
  args['numGames'] = options.numGames
  args['numSelection'] = options.numSelection
  args['fitness'] = options.fitness
  
  individuals = []
  for gen in range(args['numGen']):
    print 'Generation {gen}'.format(gen=gen)

    # first generation uses RandomAgent
    default_args = ['-p', 'RandomAgent', '-q', '--layout', args['layout'], '--numGames', str(args['numGames'])]
    if gen == 0:
      for _ in range(args['numPop']):
        games = play(default_args)
        performance = evaluateGames(games, args['fitness'])
        individual = Individual(
          performance['score'],
          performance['win_percentage'],
          performance['actions'],
          performance['food_count'],
          performance['capsules_count'],
          performance['actions_count'],
          performance['fitness']
        )
        storeIndividual(individual, gen, args['layout'])
        individuals.append(individual)
    else:
      # next generation
      offsprings = []
      for ind in individuals:
        offsprings.append(storeIndividual(mutation(ind), gen, args['layout']))

      # play generation
      for offspring in offsprings:
        offspring_args = ['-p', 'GeneticAgent', '-q', '--agentArgs', 'moveHistory={move_history}'.format(move_history=offspring.move_history), '--layout', args['layout'], '--numGames', str(args['numGames'])]
        games = play(offspring_args)
        performance = evaluateGames(games, args['fitness'])
        offspring.score = performance['score']
        offspring.win_percentage = performance['win_percentage']
        offspring.food_count = performance['food_count']
        offspring.capsules_count = performance['capsules_count']
        offspring.actions_count = performance['actions_count']
        offspring.fitness = performance['fitness']

      individuals = offsprings[:]


    # generation performance
    generation = Generation(gen, individuals)
    generation.performance()


main(sys.argv[1:])