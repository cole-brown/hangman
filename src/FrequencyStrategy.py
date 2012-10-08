#!/usr/bin/env python3
#

# Python imports
import os
import re
import collections

# local imports
if __name__ == '__main__':
   # this way so I can run this as main to test stuff,
   from GuessLetter import GuessLetter
   from GuessWord import GuessWord
   from HangmanGame import HangmanGame
   import util
else:
   from src.GuessLetter import GuessLetter
   from src.GuessWord import GuessWord
   from src.HangmanGame import HangmanGame
   from src import util

# CONSTANTS
DEBUG = False # TODO True for now
TIMING = True

#===============================================================================
# CLASS
#===============================================================================
class FrequencyStrategy:
   """Guesses frequent-in-English letters first, then switches to
   popular-amongst-possible-words letters, then guesses the words"""
   # CLASS CONSTANTS

   # Based on:
   # http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
   # TODO - remove?
   POPULAR_LETTERS = list("ETAOINSRHDLUCMFYWGPBVKXQJZ")

   #-----------------------------------------------------------------------------
   # ctor
   #-----------------------------------------------------------------------------
   def __init__(self, filepath):
      """Initialize FrequencyStrategy"""
        
      # all the possible words, divided out based on length
      self.allWords = collections.defaultdict(set)

      # fill in allWords set
      self.parseWordsFile(filepath)

      self.newGame()


   #-----------------------------------------------------------------------------
   # pick a strategy
   #-----------------------------------------------------------------------------
   def nextGuess(self, game):
      """better description""" #TODO

      with util.Timer() as upTime:
         if self.firstRun:
            self.firstUpdatePossibleWords(game)
         else:
            self.updatePossibleWords(game)
      util.DBG("    Update took %.09f sec." % upTime.interval, TIMING)

      # pick a strategy
      # TODO - better decision?
      # if we can guess all the possible words and not lose, go for it.
      if len(self.possibleWords) <= game.numWrongGuessesRemaining():
         return GuessWord(self.wordStrategy(game))
      else:
         # Pick a letter.
         # Any letter.
         # Not that letter.
         return GuessLetter(self.letterStrategy(game))


   #-----------------------------------------------------------------------------
   # pick-a-word strategy
   #-----------------------------------------------------------------------------
   def wordStrategy(self, game):
      """guess a word, based on possible words
      return - the word to be guessed (string)"""

      for word in self.possibleWords:
         if word not in game.getIncorrectlyGuessedWords():
            util.DBG("GUESS: " + word, DEBUG)
            return word


   #-----------------------------------------------------------------------------
   # pick-a-letter strategy
   #-----------------------------------------------------------------------------
   def letterStrategy(self, game):
      """guess a letter, based on letter frequency in possible words
      return - the letter to be guessed (string)"""

      # bulid a letter frequency list
      letterCount = collections.Counter()
      for word in self.possibleWords:
         # update counter with word's letters (repeated letters removed)
         letterCount.update(set(word))
         # TODO test set(word) vs just word (uniq vs non-uniq'd)

      # pick the first letter that hasn't been guessed
      for letter, _ in letterCount.most_common():
         if letter not in game.getAllGuessedLetters():
            util.DBG("GUESS: " + letter, DEBUG)
            return letter

      # TODO: raise error if entire alphabet has been guessed already?


   #-----------------------------------------------------------------------------
   # find possibilities
   #-----------------------------------------------------------------------------
   def firstUpdatePossibleWords(self, game):
      """Narrow down the possible words based on length"""

      self.firstRun = False
      
      # First time. Get a shallow copy of the proper length wordset
      self.possibleWords = self.allWords[game.getSecretWordLength()].copy()
            
      util.DBG("Possibles: " + str(len(self.possibleWords)) + " (Guesses Left: " + str(game.numWrongGuessesRemaining()) + ")", DEBUG)


   #-----------------------------------------------------------------------------
   # find possibilities
   #-----------------------------------------------------------------------------
   def updatePossibleWords(self, game):
      """Uses the dictionary and current guess to narrow down the possible words"""

      # turn current guess into a regex
      current = list(game.getGuessedSoFar())
      # match() only matches at start of string so add a final "$" to make sure
      # it's a whole match and we're not saying "c-t" matches "catapult"
      current.append("$") 
#      util.DBG("".join(current), DEBUG)
      for i in range(len(current)):
         if current[i] == HangmanGame.MYSTERY_LETTER:
            # convert to any-letter regex
            current[i] = '[A-Z]{1}'
#      util.DBG("".join(current), DEBUG)
      guessRegex = re.compile("".join(current))

      # turn incorrectly guessed letters into a regex
      wrongLetters = game.getIncorrectlyGuessedLetters()
      wrongRegex = None
      if wrongLetters:
         wrongRegex = re.compile("[" + "".join(wrongLetters) + "]+")

      # TODO something for un-possible words

      # need a (different) set to iterate over whist I remove words
      # from the possibleWords set
      tempPossibles = self.possibleWords.copy()

      # test each word in the possibilites set
#      util.DBG("Possibles pre: " + str(len(self.possibleWords)), DEBUG)
      for word in tempPossibles:
         # purge words that can't match current guess
         if guessRegex.match(word) == None:
            self.possibleWords.remove(word)

         # purge words containing incorrectly guessed letters
         elif wrongRegex != None and wrongRegex.search(word) != None:
            self.possibleWords.remove(word)

      util.DBG("Possibles: " + str(len(self.possibleWords)) + " (Guesses Left: " + str(game.numWrongGuessesRemaining()) + ")", DEBUG)


   #-----------------------------------------------------------------------------
   # reset for new game
   #-----------------------------------------------------------------------------
   def newGame(self):
      """Resets class variables to be ready for another game."""

      self.firstRun = True

   #-----------------------------------------------------------------------------
   # Read words file
   #-----------------------------------------------------------------------------
   def parseWordsFile(self, filepath):
      """Reads the dictionary and places each word into the allWords set.
      Dictionary file must be one word per line.
      exception - IOError if file can't be found/opened/read"""

      with open(filepath, 'r') as dictionary: 
         util.DBG(pretty_size(os.path.getsize(filepath)), DEBUG)

         # read words file into set
         for line in dictionary:
            word = line.strip()
            if word != "": # avoid empty lines
               self.allWords[len(word)].add(word.upper())


#===============================================================================
# Functions that are cool enough not to need a class
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
