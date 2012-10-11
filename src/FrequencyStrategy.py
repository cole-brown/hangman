#!/usr/bin/env python3
#

# Python imports
import os
import re
import collections

# local imports
if __name__ == '__main__':
   # This way so it can be run as main for quick testing.
   # If we had a setup.py and installed this, it wouldn't be needed.
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
   """Guesses letters based on which occurs in most of the popular"""

   #---
   # CLASS CONSTANTS
   #---

   # don't pre-seed cache for word sets smaller than this
   SEED_MIN = 10


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


   #-----------------------------------------------------------------------------
   # pick a strategy
   #-----------------------------------------------------------------------------
   def nextGuess(self, game):
      """Updates possible words based on previous guess, then decides whether
      to guess a word or a letter, and returns the GuessWord/GuessLetter."""

      with util.Timer() as upTime:
         self.updatePossibleWords(game)
      util.DBG("Update took %.09f sec." % upTime.interval, TIMING)

      # pick a strategy
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
      """Guess a word, based on possible words
      return - the word to be guessed (string)"""

      # sorted the word set for stable word scores
      for word in sorted(self.possible.words):
         if word not in game.getIncorrectlyGuessedWords():
            util.DBG("GUESS: " + word, DEBUG)
            return word


   #-----------------------------------------------------------------------------
   # pick-a-letter strategy
   #-----------------------------------------------------------------------------
   def letterStrategy(self, wordSet, letterSet, guessesLeft):
      """Guess a letter, based on letter frequency in possible words
      return - the letter to be guessed (string)"""

      # speed test
      # TODO remove
#      for letter in self.list("ETAOINSRHDLUCMFYWGPBVKXQJZ"):
#         if letter not in game.getAllGuessedLetters():
#            return letter

      # Pick the first letter that hasn't been guessed.
      # Sort letterFreq for stable word scores by ensuring that 11 a's always
      # get guessed after 11 b's. Turns out a-z gets worse scores than z-a
      # in the test dictionary.
      for letter, _ in sorted(wordSet.letterFreq.most_common(),
                              key=lambda lc: (lc[1], lc[0]), reverse=True): # z-a
                              #key=lambda lc: (-lc[1], lc[0])): # a-z
         if letter not in letterSet:
            util.DBG("GUESS: " + letter, DEBUG)
            util.DBG(" num: " + str(len(wordSet)), DEBUG)
            util.DBG(" letters: " + str(wordSet.letterFreq.most_common()), DEBUG)
            return letter


   #-----------------------------------------------------------------------------
   # find possibilities
   #-----------------------------------------------------------------------------
   def updatePossibleWords(self, game):
      """Uses the dictionary and current guess to narrow down the possible words.
      return - Nothing. Updates self vars."""

      # check the cache before doing any work
      if self.key(game) in self.wordCache:
         # It's there. Use it.
         self.possible = self.wordCache[self.key(game)].copy()
         return
      # try set intersection if possible
      elif False: # TODO
         # key with latest bad guess
         # check for key in cache
         # set intersection!
         pass

      # Set to use in the regex. Either any caps letter, 
      # or not the incorrect letters.
      wrongLetters = game.getIncorrectlyGuessedLetters()
      if wrongLetters:
         notWrongLetters = "[^" + "".join(wrongLetters) + "]{"
      else:
         notWrongLetters = "[A-Z]{"

      # turn guessedSoFar into a regex using notWrongLetters
      current = re.compile("(" + HangmanGame.MYSTERY_LETTER + 
                           "+|[A-Z]+)").findall(game.getGuessedSoFar())
      for i in range(len(current)):
         if current[i][0] == HangmanGame.MYSTERY_LETTER:
            current[i] = notWrongLetters + str(len(current[i])) + "}"

      # match() only matches at start of string so add a final "$" to make sure
      # it's a whole match and we're not saying "c-t" matches "catapult"
      current.append("$") 
      guessRegex = re.compile("".join(current))

      # need a (different) set to iterate over whist I remove words
      # from the possible set
      tempPossibles = self.possible.words.copy()

      # test each word in the possibilites set
      for word in tempPossibles:
         # purge words that can't match current guess
         if guessRegex.match(word) == None:
            self.possible.words.remove(word)

      # inform the WordSet that it's been updated
      self.possible.updated()

      # cache results
      self.cache(game)


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
      Does not verify the words (i.e. does not check that they've only got 
      letters in them).
      exception - IOError if file can't be found/opened/read"""

      with open(filepath, 'r') as dictionary: 
         util.DBG(util.pretty_size(os.path.getsize(filepath)), DEBUG)

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
      # TODO - does this speed things up much?
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
#            # determine second guess letter
#            letter = self.letterStrategy(self.wordCache[k], set(letter), 1000)
#
#            # weed down to just failures
#            noLetter = self.wordCache[k].copy()
#            for word in self.wordCache[k].words:
#               if letter in word:
#                  noLetter.words.remove(word)
#            noLetter.updated()
#
#            # save to cache with new key
#            key = HangmanGame.MYSTERY_LETTER * len(word) + "!" + letter
#            self.wordCache[key] = noLetter
#            util.DBG("pre-cached: " + key, DEBUG)




#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == '__main__':
   strat = FrequencyStrategy("words.txt")
   print("aa" in strat.wordCache)

# Fin
