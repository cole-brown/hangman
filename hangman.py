#!/usr/bin/env python3

# TODO
"""top level doc string"""

# Python imports
import sys
from optparse import OptionParser

# local imports
from src.HangmanGame import HangmanGame
from src.GuessLetter import GuessLetter
from src.GuessWord import GuessWord
from src.FrequencyStrategy import FrequencyStrategy

# CONSTANTS
DEBUG = True # TODO - true for now

#-----------------------------------------------------------------------------
# run the game
#-----------------------------------------------------------------------------
def run(game, strategy):
   """Runs one game of Hangman with the supplied strategy"""

   while game.gameStatus() == HangmanGame.KEEP_GUESSING:
      # ask strategy for a guess
      guess = strategy.nextGuess(game)

      # apply guess to game
      guess.makeGuess(game)
      
      DBG(game)

   return game.currentScore()

#-----------------------------------------------------------------------------
# primary function
#-----------------------------------------------------------------------------
def main(argv=None):
   """this is run when the file is evaluated"""
   if argv is None:
      argv = sys.argv
   try:
      parser = OptionParser()
#      parser.add_option("-f", "--file", dest="filename",
#                        help="write report to FILE", metavar="FILE")
#      parser.add_option("-q", "--quiet",
#                        action="store_false", dest="verbose", default=True,
#                        help="don't print status messages to stdout")

      (options, args) = parser.parse_args()

      # make stuff
      word = "factual".upper()
      maxWrong = 5
      game = HangmanGame(word, maxWrong)
      strategy = FrequencyStrategy("words.txt")

      # run a game!
      run(game, strategy)

      print(word + " = " + str(game.currentScore()))
      return 0
   except Exception as err:
      raise err # TODO - for now, I want the stack trace
      print(err, file=sys.stderr)
      print("for help use --help", file=sys.stderr)
      return 2


#-------------------------------------------------------------------------------
# Sometimes you just want to make the voices go away...
#-------------------------------------------------------------------------------
def DBG(printable):
   """No one likes bugs..."""
   if DEBUG:
      print(printable)

#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == "__main__":
  sys.exit(main())

