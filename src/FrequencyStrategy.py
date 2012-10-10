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
   from WordSet import WordSet
   import util
else:
   from src.GuessLetter import GuessLetter
   from src.GuessWord import GuessWord
   from src.HangmanGame import HangmanGame
   from src.WordSet import WordSet
   from src import util

# CONSTANTS
DEBUG = False # TODO True for now
TIMING = False # TODO True for now

#===============================================================================
# CLASS
#===============================================================================
class FrequencyStrategy:
   """Guesses frequent-in-English letters first, then switches to
   popular-amongst-possible-words letters, then guesses the words"""
   # CLASS CONSTANTS

   # don't pre-seed cache for word sets smaller than this
   SEED_MIN = 10 # TODO - play around to find good number

   # Based on:
   # http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
   # TODO - remove?
   POPULAR_LETTERS = list("ETAOINSRHDLUCMFYWGPBVKXQJZ")

   #-----------------------------------------------------------------------------
   # ctor
   #-----------------------------------------------------------------------------
   def __init__(self, filepath):
      """Initialize FrequencyStrategy"""

      # Cache of possible words given current game state.
      # Initially just all the possible words, divided out based on length.
      # As games progress, more WordSets-possible-given-game-state-X are added.
      self.wordCache = collections.defaultdict(WordSet)

      # process dictionary file
      self.parseWordsFile(filepath)

      self.seedCache()

      self.newGame()

      util.DBG("INIT DONE!!!!!!", True)


   #-----------------------------------------------------------------------------
   # pick a strategy
   #-----------------------------------------------------------------------------
   def nextGuess(self, game):
      """better description""" #TODO

      with util.Timer() as upTime:
         self.updatePossibleWords(game)
# TODO - delete
#         if self.firstRun:
#            self.firstUpdatePossibleWords(game)
#         else:
#            self.updatePossibleWords(game)
      util.DBG("    Update took %.09f sec." % upTime.interval, TIMING)

      # pick a strategy
      # TODO - better decision?
      # if we can guess all the possible words and not lose, go for it.
      if len(self.possible) <= game.numWrongGuessesRemaining():
         return GuessWord(self.wordStrategy(game))
      else:
         # Pick a letter.
         # Any letter.
         # Not that letter.
         return GuessLetter(self.letterStrategy(self.possible,
                                                game.getAllGuessedLetters(),
                                                game.numWrongGuessesRemaining()))


   #-----------------------------------------------------------------------------
   # pick-a-word strategy
   #-----------------------------------------------------------------------------
   def wordStrategy(self, game):
      """guess a word, based on possible words
      return - the word to be guessed (string)"""

      for word in sorted(self.possible.words):
         if word not in game.getIncorrectlyGuessedWords():
            util.DBG("GUESS: " + word, DEBUG)
            return word


   #-----------------------------------------------------------------------------
   # pick-a-letter strategy
   #-----------------------------------------------------------------------------
   def letterStrategy(self, wordSet, letterSet, guessesLeft):
      """guess a letter, based on letter frequency in possible words
      return - the letter to be guessed (string)"""

      # speed test
#      for letter in self.POPULAR_LETTERS:
#         if letter not in game.getAllGuessedLetters():
#            return letter

      # Pick the first letter that hasn't been guessed.
      # Sort letterFreq for stable word scores by ensuring that 11 a's always
      # get guessed before 11 b's.
#      for letter, _ in wordSet.letterFreq.most_common(): # normal
#      for letter, _ in sorted(wordSet.letterFreq.most_common(),
#                              key=lambda lc: (-lc[1], lc[0])): # a-z
      for letter, _ in sorted(wordSet.letterFreq.most_common(),
                              key=lambda lc: (lc[1], lc[0]), reverse=True): # z-a
         if letter not in letterSet:
            util.DBG("GUESS: " + letter, DEBUG)
            util.DBG(" num: " + str(len(wordSet)), DEBUG)
            util.DBG(" letters: " + str(wordSet.letterFreq.most_common()), DEBUG)
            return letter

      # TODO: raise error if entire alphabet has been guessed already?


   #-----------------------------------------------------------------------------
   # find possibilities
   #-----------------------------------------------------------------------------
   def firstUpdatePossibleWords(self, game):
      """Narrow down the possible words based on length"""

      # TODO - don't need?

      self.firstRun = False
      
      # First time. Get a shallow copy of the proper length words.
      self.possible = self.wordCache[self.key(game)].copy()
            
      util.DBG("Possibles: " + str(len(self.possible)) + " (Guesses Left: " + str(game.numWrongGuessesRemaining()) + ")", DEBUG)


   #-----------------------------------------------------------------------------
   # find possibilities
   #-----------------------------------------------------------------------------
   def updatePossibleWords(self, game):
      """Uses the dictionary and current guess to narrow down the possible words"""

      # check the cache before doing any work
      if self.key(game) in self.wordCache:
         # It's there. Use it.
         self.possible = self.wordCache[self.key(game)].copy()
         if len(self.possible) > game.numWrongGuessesRemaining(): # TODO DEBUG
            util.DBG("non-word-guess cache hit: " + self.key(game), DEBUG)
         return

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
      # from the possible set
      tempPossibles = self.possible.words.copy()

      # test each word in the possibilites set
#      util.DBG("Possibles pre: " + str(len(self.possible)), DEBUG)
      for word in tempPossibles:
         # purge words that can't match current guess
         if guessRegex.match(word) == None:
            self.possible.words.remove(word)

         # purge words containing incorrectly guessed letters
         elif wrongRegex != None and wrongRegex.search(word) != None:
            self.possible.words.remove(word)

      # inform the WordSet that it's been updated
      self.possible.updated()

      # cache results
      self.cache(game)

      util.DBG("Possibles: " + str(len(self.possible)) + " (Guesses Left: " + str(game.numWrongGuessesRemaining()) + ")", DEBUG)


   #-----------------------------------------------------------------------------
   # The cache is locked, apparently.
   #-----------------------------------------------------------------------------
   def key(self, game):
      """Returns the key to be used for the words cache."""

      # make dict key
      return "".join(list(game.getGuessedSoFar()) + ['!'] + 
                     sorted(game.getIncorrectlyGuessedLetters()))


   #-----------------------------------------------------------------------------
   # Caching!
   #-----------------------------------------------------------------------------
   def cache(self, game):
      """Saves current self.possible to cache."""

      # save to dict
      util.DBG(self.key(game) + ": " + str(len(self.possible)), DEBUG)
      self.wordCache[self.key(game)] = self.possible.copy()

   #-----------------------------------------------------------------------------
   # reset for new game
   #-----------------------------------------------------------------------------
   def newGame(self):
      """Resets class variables to be ready for another game."""
      # TODO - needed?

      self.firstRun = True


   #-----------------------------------------------------------------------------
   # Read words file
   #-----------------------------------------------------------------------------
   def parseWordsFile(self, filepath):
      """Reads the dictionary and places each word into the words cache.
      Dictionary file must be one word per line.
      exception - IOError if file can't be found/opened/read"""

      with open(filepath, 'r') as dictionary: 
         util.DBG(pretty_size(os.path.getsize(filepath)), DEBUG)

         # read words file into set
         for line in dictionary:
            word = line.strip()
            if word != "": # avoid empty lines
               key = HangmanGame.MYSTERY_LETTER * len(word) + "!"
               self.wordCache[key].words.add(word.upper())

      # Everything read in. Generate the WordSets' letter freqs.
      for k in self.wordCache:
         self.wordCache[k].updated()


   #-----------------------------------------------------------------------------
   # seed cache
   #-----------------------------------------------------------------------------
   def seedCache(self):
      """Pre-compute misses for common letters."""

      emptySet = set() # used to get letterStrategy's first guess
      temp = self.wordCache.copy() # can't add to what we're iterating over, so temp
      for k in temp:
         # don't bother for the sets that are tiny
         if len(self.wordCache[k]) > self.SEED_MIN:
            # determine first guess letter
            letter = self.letterStrategy(self.wordCache[k], emptySet, 1000)

            # weed down to just failures
            noLetter = self.wordCache[k].copy()
            for word in self.wordCache[k].words:
               if letter in word:
                  noLetter.words.remove(word)
            noLetter.updated()

            # save to cache with new key
            key = HangmanGame.MYSTERY_LETTER * len(word) + "!" + letter
            self.wordCache[key] = noLetter
            util.DBG("pre-cached: " + key, DEBUG)

      # TODO - pre-seed two misses as well?




#===============================================================================
# Functions that are cool enough not to need a class
#===============================================================================
  
#-------------------------------------------------------------------------------
# pretty_size: I'm so pretty~ Oh so pretty~
#-------------------------------------------------------------------------------
def pretty_size(num):
   """Returns a string of the input bytes, prettily formatted for human reading. 
   E.g. 2048 -> '2 KiB'"""
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
   print("aa" in strat.wordCache)
   print(strat.POPULAR_LETTERS)

# Fin
