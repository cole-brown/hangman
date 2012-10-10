#!/usr/bin/env python3

# TODO
"""top level doc string"""

# Python imports
import sys
from argparse import ArgumentParser

# local imports
from src.HangmanGame import HangmanGame
from src.GuessLetter import GuessLetter
from src.GuessWord import GuessWord
from src.FrequencyStrategy import FrequencyStrategy
from src import util

# CONSTANTS
DEBUG = False # TODO - true for now
TIMING = False # TODO - true for now

#-----------------------------------------------------------------------------
# run the game
#-----------------------------------------------------------------------------
def run(game, strategy, printGameState=True):
   """Runs one game of Hangman with the supplied strategy"""

   while game.gameStatus() == HangmanGame.KEEP_GUESSING:
      # ask strategy for a guess
      with util.Timer() as sTime:
         guess = strategy.nextGuess(game)
      util.DBG("Strategery took %.09f sec." % sTime.interval, TIMING)

      # apply guess to game
      guess.makeGuess(game)
      
      util.DBG(game, printGameState)

   return game.currentScore()

#-----------------------------------------------------------------------------
# primary function
#-----------------------------------------------------------------------------
def main(argv=None):
   """this is run when the file is evaluated"""
   if argv is None:
      argv = sys.argv
   try:
      parser = ArgumentParser()
      parser.add_argument("dictionary",
                          help="read dictionary in from file")
      parser.add_argument("words",
                          help="read game words in from file")
#      parser.add_argument("word", nargs="+", 
#                          help="list of words to play hangman on")
      parser.add_argument("-g", "--guesses", type=int, default=5,
                          help="max number of wrong guesses")
      parser.add_argument("-v", "--verbose", 
                          #action="store_true", default=False,
                          action="count", default=0,
                          help="increase output verbosity (-vv for extra verbose)")

      args = parser.parse_args()
      util.DBG(args, DEBUG)

      # read in words to run games on
      words = []
      with open(args.words, 'r') as gameWords:
         # read words file into set
         words = [word.strip().upper() for word in gameWords if word.strip() != ""]

      with util.Timer() as sInit:
         # stuff that can be reused between games
         strategy = FrequencyStrategy(args.dictionary)
         avg = 0.0
         avgTime = 0.0
      util.DBG("Init took %.09f sec." % sInit.interval, TIMING)

      with util.Timer() as totalTime:
         for word in words:
            # make per-game stuff
            word = word.upper()
            game = HangmanGame(word, args.guesses)
           
            # run a game!
            with util.Timer() as gTime:
               run(game, strategy, args.verbose > 1)
            util.DBG("Game took %.09f sec." % gTime.interval, TIMING)
            avgTime += gTime.interval / float(len(words))

            # average score update
            avg += game.currentScore() / float(len(words))

            if args.verbose:
               print(word + " = " + str(game.currentScore()))
           
            # reset strategy for next go
            strategy.newGame()

      print("average: " + str(avg))

      util.DBG("Average game time: %.09f sec." % avgTime, True)
      util.DBG("Total: %.09f sec." % totalTime.interval, TIMING)
      return 0
   except Exception as err:
      raise err # TODO - for now, I want the stack trace
      print(err, file=sys.stderr)
      print("for help use --help", file=sys.stderr)
      return 2


#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == "__main__":
  sys.exit(main())

