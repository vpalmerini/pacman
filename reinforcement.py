import sys

from optparse import OptionParser
from pacman import readCommand, runGames

def play(args):
  _args = readCommand(args)
  games = runGames(**_args)
  return games

def evaluateGames(games):
  scores = [game.state.getScore() for game in games]
  wins = [game.state.isWin() for game in games]

  # performance
  perf = dict()
  perf['score'] = sum(scores) / len(games)
  perf['win_percentage'] = float(wins.count(True)) / len(games)
  perf['food_count'] = sum([game.state.getNumFood() for game in games]) / len(games)
  perf['capsules_count'] = sum([len(game.state.getCapsules()) for game in games]) / len(games)
  perf['actions_count'] = sum([len([move for move in game.moveHistory if move[0] == 0]) for game in games]) / len(games)

  return perf


def main(argv):
  usageStr = """"""
  parser = OptionParser(usageStr)

  parser.add_option('--layout', type='str', default='smallClassic')
  parser.add_option('--numGames', type='int', default=1000)
  parser.add_option('--learningRate', type='float', default=0.8)
  parser.add_option('--explorationRate', type='float', default=0.8)
  parser.add_option('--discountFactor', type='float', default=0.2)

  options, junk = parser.parse_args(argv)

  args = dict()
  args['layout'] = options.layout
  args['numGames'] = options.numGames
  args['learningRate'] = options.learningRate
  args['explorationRate'] = options.explorationRate
  args['discountFactor'] = options.discountFactor

  args = ['-p', 'QAgent', '-q', '-a', 'numGames={num_games},learningRate={learning_rate},explorationRate={exploration_rate},discountFactor={discount_factor}'.format(num_games=args['numGames'], learning_rate=args['learningRate'], exploration_rate=args['explorationRate'], discount_factor=args['discountFactor']), '--layout', args['layout'], '--numGames', str(args['numGames'])]
  games = play(args)
  generalPerformance = evaluateGames(games[-10:])

  print generalPerformance

main(sys.argv[1:])