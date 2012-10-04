#!/usr/bin/env python3
#

# Python imports
import os

# local imports

# CONSTANTS

#===============================================================================
# CLASS
#===============================================================================
class FrequencyStrategy:
   """Guesses frequent-in-English letters first, then switches to
   popular-amongst-possible-words letters, then guesses the words"""
   # CLASS CONSTANTS

   # Based on:
   # http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
   POPULAR_LETTERS = list("ETAOINSRHDLUCMFYWGPBVKXQJZ")
   # TODO: build this based on what letters appear in the most words?

   #-----------------------------------------------------------------------------
   # ctor
   #-----------------------------------------------------------------------------
   def __init__(self, filepath):
      """Initialize FrequencyStrategy"""
      #DBG("__init__") # DEBUG
        
      # all the possible words
      self.allWords = set()

      # fill in allWords set
      self.parseWordsFile(filepath)


   #-----------------------------------------------------------------------------
   # pick a strategy
   #-----------------------------------------------------------------------------
   def nextGuess(self, game):
      """better description"""

      # pick a strategy

      # pick word/letter

      # return that GuessWord/GuessLetter

      # but for now,
      return GuessLetter(letterStrategy(game))


   #-----------------------------------------------------------------------------
   # pick-a-letter strategy
   #-----------------------------------------------------------------------------
   def letterStrategy(self, game):
      """guess a letter, based on letter frequency in English
      return - the letter to be guessed (string)"""

      guessed = game.getAllGuessedLetters()

      # pick the first letter that hasn't been guessed
      for letter in POPULAR_LETTERS:
         if letter not in guessed:
            return letter

      # TODO: raise error if entire alphabet has been guessed already?


   #-----------------------------------------------------------------------------
   # Read words file
   #-----------------------------------------------------------------------------
   def parseWordsFile(self, filepath):
      """better description"""

      # TODO catch IOError here or let bubble up?
      #   except IOError as err:
      #     print >>sys.stderr, "Trouble reading or opening file.\n"
      #     print >>sys.stderr, err
      with open(filepath, 'r') as wordsFile: 
         DBG(pretty_size(os.path.getsize(filepath)))

         # read words file into set
         for line in wordsFile:
            if line.strip() != "": # avoid empty lines
               self.allWords.add(line.strip()) # get rid of newline char

# TODO NOTES!
# read file into set
# keep set for subsequent games
# shallow copy (set.copy()) for each game, so can remove words as needed?

#===============================================================================
# Functions that are Cool enough not to need a class
#===============================================================================
  
#-------------------------------------------------------------------------------
# pretty_size: I'm so pretty~ Oh so pretty~
#-------------------------------------------------------------------------------
def pretty_size(num):
   """Returns a string of the input bytes, prettily formatted for human reading. E.g. 2048 -> '2 KiB'"""
   for x in ['bytes','KiB','MiB','GiB','TiB', 'PiB', 'EiB', 'ZiB', 'YiB']:
      if num < 1024.0:
         return "%3.1f %s" % (num, x)
      num /= 1024.0

#-------------------------------------------------------------------------------
# Sometimes you just want to make the voices go away...
#-------------------------------------------------------------------------------
DEBUG = True
def DBG(printable):
   """No one likes bugs..."""
   if DEBUG:
      print(printable)




#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == '__main__':
   strat = FrequencyStrategy("words.txt")
   print("aa" in strat.allWords)
   print(strat.POPULAR_LETTERS)

# Fin
