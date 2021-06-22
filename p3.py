import os
import cPickle
from collections import Counter

from pacman import readCommand, runGames
from layout import getLayout

class Individual:
  def __init__(self, score = float("inf"), win = False, moveHistory = [], food_count = 55, capsules_count = 2):
    self.score = score
    self.win = win
    self.moveHistory = moveHistory
    self.food_count = food_count
    self.capsules_count = capsules_count

  def fitness(self):
    return self.score + 10000 * int(self.win) - (1000 * self.capsules_count + 1000 * self.food_count)


# asexual reproduction
def duplication(individuals, gen, layout, crop = 3, factor = 2):
  new_individuals = []
  for (index, ind) in enumerate(factor * individuals):
    moves = ind.moveHistory
    if type(moves) is str:
      f = open(moves)
      moves = cPickle.load(f)['actions']
      f.close()
    
    moves = moves[:crop]

    _dir = 'gen-{gen}'.format(gen=gen)
    if not os.path.exists(_dir):
      os.mkdir(_dir)
    
    fname = '{dir}/child-{child}'.format(dir=_dir, child=index)
    f = file(fname, 'w')
    
    components = {'layout': getLayout(layout), 'actions': moves}
    cPickle.dump(components, f)
    f.close()

    new_individuals.append(Individual(moveHistory=fname))

  return new_individuals



def get_half_moves(individual):
  moves = individual.moveHistory
  if type(individual.moveHistory) is str:
    f = open(individual.moveHistory)
    moves = cPickle.load(f)['actions']
    f.close()
    
  return moves[:(len(moves) // 2)] 

# sexual reproduction
def crossover(individuals, gen, layout):
  i = 0
  j = len(individuals) - 1
  children = []

  while i < j:
    p1_first_half_moves = get_half_moves(individuals[i])
    p2_second_half_moves = get_half_moves(individuals[j])

    children_move_history = p1_first_half_moves + p2_second_half_moves

    _dir = 'gen-{gen}'.format(gen=gen)
    if not os.path.exists(_dir):
      os.mkdir(_dir)
    
    fname = '{dir}/child-{child}'.format(dir=_dir, child=i)
    f = file(fname, 'w')
    
    components = {'layout': getLayout(layout), 'actions': children_move_history}
    cPickle.dump(components, f)
    f.close()

    children.append(Individual(moveHistory=fname))

    i += 1
    j -= 1

  return children


def mutation(individual, crop = 3):
  if type(individual.moveHistory) is str:
    f = open(individual.moveHistory, 'rb')
    components = cPickle.load(f)
    f.close()

    components['actions'] = components['actions'][:crop]
    f = open(individual.moveHistory, 'wb')
    cPickle.dump(components, f)
    f.close()
  else:
    individual.moveHistory = individual.moveHistory[:crop]


def evaluateIndividual(games):
  scores = [game.state.getScore() for game in games]
  wins = [game.state.isWin() for game in games]

  best_score = max(score)
  best_index = scores.index(best_score)


  move_history = games[best_index].moveHistory
  food_count = [game.state.getNumFood() for game in games]
  capsules_count = [len(game.state.getCapsules()) for game in games]

  return Individual(scores[best_index], wins[best_index], move_history, food_count[best_index], capsules_count[best_index])


def main():
  NUMBER_OF_GENERATIONS = 5
  NUMBER_OF_INDIVIDUALS = 4
  LAYOUT = 'smallClassic'
  REPRODUCTION = 'asexual'
  FACTOR = 2
  crop = 2
  INDIVIDUALS_PERSIST = False
  MUTATION = False

  gen_performance = {}
  individuals = []
  default_args = ['-p', 'RandomAgent', '--layout', LAYOUT, '--numGames', 3]

  for gen in range(NUMBER_OF_GENERATIONS):
    print 'Generation {gen}'.format(gen=gen)
    if gen == 0:
      for _ in range(NUMBER_OF_INDIVIDUALS):
        args = readCommand(default_args)
        games = runGames(**args)

        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        move_history = games[0].moveHistory
        food_count = [game.state.getNumFood() for game in games]
        capsules_count = [len(game.state.getCapsules()) for game in games]

        individuals.append(evaluateIndividual(games))

    # generation average
    gen_performance[gen] = []
    gen_performance[gen].append(sum(ind.score for ind in individuals) / NUMBER_OF_INDIVIDUALS)
    gen_performance[gen].append(sum([ind.fitness() for ind in individuals]))
    gen_performance[gen].append(Counter([ind.win for ind in individuals]))

    # parents - best from current generation
    best_individuals = list(reversed(sorted(individuals, key=lambda x: x.fitness())))[:(NUMBER_OF_INDIVIDUALS // FACTOR)]

    crop += 1

    # reproduction
    children = []
    if REPRODUCTION == 'sexual':
      children = crossover(best_individuals, gen, LAYOUT)
    else:
      children = duplication(best_individuals, gen, LAYOUT, crop, FACTOR)

    # evaluate children
    for child in children:
      children_args = ['-p', 'EvolutiveAgent', '--agentArgs', 'moveHistory={moveHistory}'.format(moveHistory=child.moveHistory), '--layout', LAYOUT]
      args = readCommand(children_args)
      games = runGames(**args)

      scores = [game.state.getScore() for game in games]
      wins = [game.state.isWin() for game in games]
      food_count = [game.state.getNumFood() for game in games]
      capsules_count = [len(game.state.getCapsules()) for game in games]

      child.score = scores[0]
      child.win = wins[0]
      child.food_count = food_count[0]
      child.capsules_count = capsules_count[0]
    
    individuals = []
    if INDIVIDUALS_PERSIST:
      individuals = list(reversed(sorted(individuals + children, key=lambda x: x.fitness())))[:NUMBER_OF_INDIVIDUALS]
    else:
      individuals = list(reversed(sorted(children, key=lambda x: x.fitness())))[:NUMBER_OF_INDIVIDUALS]

    # mutation
    if MUTATION:
      for ind in individuals:
        mutation(ind)

  print gen_performance


main()