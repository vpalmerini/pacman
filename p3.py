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
    return self.score + 100 * int(self.win) - (10 * self.capsules_count + self.food_count)


def get_half_moves(individual, half = 'first'):
  moves = individual.moveHistory
  if type(individual.moveHistory) is str:
    f = open(individual.moveHistory)
    moves = cPickle.load(f)['actions']
    f.close()
    
  moves_length = len(moves)
  if half == 'second':
    return moves[moves_length:] 
  return moves[:moves_length]


def generate_children(individuals, gen, layout):
  i = 0
  j = len(individuals) - 1
  children = []

  while i < j:
    p1_first_half_moves = get_half_moves(individuals[i], 'first')
    p2_second_half_moves = get_half_moves(individuals[j], 'second')

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


def main():
  NUMBER_OF_GENERATIONS = 100
  NUMBER_OF_INDIVIDUALS = 6
  LAYOUT = 'smallClassic'

  gen_performance = {}
  individuals = []
  default_args = ['-p', 'RandomAgent', '-q', '--layout', LAYOUT]

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

        individuals.append(Individual(scores[0], wins[0], move_history, food_count[0], capsules_count[0]))

    # generation average
    gen_performance[gen] = []
    gen_performance[gen].append(sum(ind.score for ind in individuals) / NUMBER_OF_INDIVIDUALS)
    gen_performance[gen].append(sum([ind.fitness() for ind in individuals]))
    gen_performance[gen].append(Counter([ind.win for ind in individuals]))

    # parents - best 6 from current generation
    best_individuals = list(reversed(sorted(individuals, key=lambda x: x.fitness())))[:10]

    # reproduction
    children = generate_children(best_individuals, gen, LAYOUT)


    for child in children:
      children_args = ['-p', 'EvolutiveAgent', '--agentArgs', 'moveHistory={moveHistory}'.format(moveHistory=child.moveHistory), '-q', '--layout', LAYOUT]
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
    
    individuals = list(reversed(sorted(individuals + children, key=lambda x: x.fitness())))[:NUMBER_OF_INDIVIDUALS]

  print gen_performance


main()