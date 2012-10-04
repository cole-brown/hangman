#!/usr/bin/env python3
#

# Python imports
###import java.util.Collections;
###import java.util.HashSet;
###import java.util.Set;

# local imports

#===============================================================================
# CLASS
#===============================================================================
class HangmanGame:
   """Contains all state for the game of Hangman."""
   #-----------------------------------------------------------------------------
   # CLASS CONSTANTS
   #-----------------------------------------------------------------------------

   # 'enum' for the current state of the game
   GAME_WON      = 0
   GAME_LOST     = 1
   KEEP_GUESSING = 2

   # A marker for the letters in the secret words that have not been guessed yet.
   MYSTERY_LETTER = '-'

   #-----------------------------------------------------------------------------
   # ctor
   #-----------------------------------------------------------------------------
   def __init__(self, secretWord, maxWrongGuesses):
      """Initializer.
      secretWord - The word that needs to be guessed
      maxWrongGuesses - The maximum number of incorrect word/letter guesses that 
      are allowed"""

      # The word that needs to be guessed (e.g. 'FACTUAL')
      self.secretWord = secretWord.upper()

      # The letters guessed so far (unknown letters will be marked by the
      # MYSTERY_LETTER constant). For example, 'F-CTU-L'
      self.guessedSoFar = list(self.MYSTERY_LETTER * len(self.secretWord))

      # The maximum number of wrong letter/word guesses that are allowed
      # (e.g. 6, and if you exceed 6 then you lose)
      self.maxWrongGuesses = maxWrongGuesses

      # Set of all correct letter guesses so far (e.g. 'C', 'F', 'L', 'T', 'U')
      self.correctlyGuessedLetters = set()

      # Set of all incorrect letter guesses so far (e.g. 'R', 'S')
      self.incorrectlyGuessedLetters = set()

      # Set of all incorrect word guesses so far (e.g. 'FACTORS')
      self.incorrectlyGuessedWords = set()


   #-----------------------------------------------------------------------------
   # Guess the letter
   #-----------------------------------------------------------------------------
   def guessLetter(self, ch):
      """Guess the specified letter and update the game state accordingly
      return - The string representation of the current game state
      (which will contain MYSTERY_LETTER in place of unknown letters)"""
      self.assertCanKeepGuessing()
      ch = ch.upper()

      # ch == 1 char?
      assert type(ch) is str, "%r is not a string" % ch
      assert len(ch) == 1, "%r is not a single character" % ch

      # update the guessedSoFar buffer with the new character
      goodGuess = False
      for i in range(len(self.secretWord)):
         if self.secretWord[i] == ch:
            self.guessedSoFar[i] = ch
            goodGuess = True

      # update the proper set of guessed letters
      if goodGuess:
          self.correctlyGuessedLetters.add(ch)
      else:
          self.incorrectlyGuessedLetters.add(ch)

      return self.getGuessedSoFar()


   #-----------------------------------------------------------------------------
   # Guess the word
   #-----------------------------------------------------------------------------
   def guessWord(self, guess):
      """Guess the specified word and update the game state accordingly
      return - The string representation of the current game state
      (which will contain MYSTERY_LETTER in place of unknown letters)"""
      self.assertCanKeepGuessing()
      guess = guess.upper()

      if guess == self.secretWord:
         # if the guess is correct, then set guessedSoFar to the secret word
         self.guessedSoFar = list(self.secretWord)
      else:
         self.incorrectlyGuessedWords.add(guess)

      return self.getGuessedSoFar()


   #-----------------------------------------------------------------------------
   # current game score
   #-----------------------------------------------------------------------------
   def currentScore(self):
      """return - The score for the current game state"""
      if (self.gameStatus() == self.GAME_LOST):
         return 25
      else:
         return self.numWrongGuessesMade() + len(self.correctlyGuessedLetters)


   #-----------------------------------------------------------------------------
   # Exceptions!
   #-----------------------------------------------------------------------------
   def assertCanKeepGuessing(self):
      """Throws AssertionError if not allowed to keep guessing"""
      assert self.gameStatus() == self.KEEP_GUESSING, "More guesses not allowed!"


   #-----------------------------------------------------------------------------
   # Game's current state
   #-----------------------------------------------------------------------------
   def gameStatus(self):
      """return - The current game status"""
      if self.secretWord == self.getGuessedSoFar():
         return self.GAME_WON
      elif self.numWrongGuessesMade() > self.maxWrongGuesses:
         return self.GAME_LOST
      else:
         return self.KEEP_GUESSING


   #-----------------------------------------------------------------------------
   # Wrong Guesses
   #-----------------------------------------------------------------------------
   def numWrongGuessesMade(self):
      """return - Number of wrong guesses made so far"""
      return len(self.incorrectlyGuessedLetters) + len(self.incorrectlyGuessedWords)


   #-----------------------------------------------------------------------------
   # Wrong Guesses Left
   #-----------------------------------------------------------------------------
   def numWrongGuessesRemaining(self):
      """return - Number of wrong guesses still allowed"""
      return self.getMaxWrongGuesses() - self.numWrongGuessesMade()


   #-----------------------------------------------------------------------------
   # Max Wrong Guesses
   #-----------------------------------------------------------------------------
   def getMaxWrongGuesses(self):
      """return - Number of total wrong guesses allowed"""
      return self.maxWrongGuesses


   #-----------------------------------------------------------------------------
   # Gesses So Far
   #-----------------------------------------------------------------------------
   def getGuessedSoFar(self):
      """return - The string representation of the current game state
      (which will contain MYSTERY_LETTER in place of unknown letters)"""
      return "".join(self.guessedSoFar)


   #-----------------------------------------------------------------------------
   # Correct Letter Guesses
   #-----------------------------------------------------------------------------
   def getCorrectlyGuessedLetters(self):
      """return - Set of all correctly guessed letters so far"""
      return set(self.correctlyGuessedLetters)


   #-----------------------------------------------------------------------------
   # Incorrect Letter Guesses
   #-----------------------------------------------------------------------------
   def getIncorrectlyGuessedLetters(self):
      """return - Set of all incorrectly guessed letters so far"""
      return set(self.incorrectlyGuessedLetters)

   #-----------------------------------------------------------------------------
   # All Letter Guesses
   #-----------------------------------------------------------------------------
   def getAllGuessedLetters(self):
      """return - Set of all guessed letters so far"""
      return self.correctlyGuessedLetters | self.incorrectlyGuessedLetters


   #-----------------------------------------------------------------------------
   # All Incorrect Word Guesses
   #-----------------------------------------------------------------------------
   def getIncorrectlyGuessedWords(self):
      """return - Set of all incorrectly guessed words so far"""
      return set(self.incorrectlyGuessedWords)


   #-----------------------------------------------------------------------------
   # Secret Word's Length
   #-----------------------------------------------------------------------------
   def getSecretWordLength(self):
      """return - The length of the secret word"""
      return len(self.secretWord)


   #-----------------------------------------------------------------------------
   # print out function
   #-----------------------------------------------------------------------------
   def __str__(self):
      """HangmanGame's representation as a string"""

      status = "KEEP_GUESSING"
      if self.gameStatus() == self.GAME_LOST:
          status = "GAME_LOST"
      elif self.gameStatus() == self.GAME_WON:
          status = "GAME_WON"

      return self.getGuessedSoFar() + "; score=" + str(self.currentScore()) + "; status=" + status



#===============================================================================
# Functions that are cool enough not to need a class
#===============================================================================

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
   from GuessLetter import GuessLetter
   from GuessWord import GuessWord

   # secret word is factual, 4 wrong guesses are allowed
   game = HangmanGame("factual", 4)
   print(game)

   GuessLetter('a').makeGuess(game)
   print(game)

   GuessWord("natural").makeGuess(game)
   print(game)

   GuessLetter('x').makeGuess(game)
   print(game)

   GuessLetter('u').makeGuess(game)
   print(game)

   GuessLetter('l').makeGuess(game)
   print(game)

   GuessWord("factual").makeGuess(game)
   print(game)

# Fin
