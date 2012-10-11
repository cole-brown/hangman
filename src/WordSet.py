#!/usr/bin/env python3
#

# Python imports
import collections

#===============================================================================
# CLASS
#===============================================================================
class WordSet:
   """Simple class to encapsulate a set of possible words and the letter
   frequency assoicated with it."""

   #-----------------------------------------------------------------------------
   # ctor
   #-----------------------------------------------------------------------------
   def __init__(self, words=None):
      """Initialize WordSet with provided set. If none provided, initialize with 
      empty set."""

      if words == None:
         self.words = set()
         self.letterFreq = collections.Counter()
      else:
          self.words = words.copy()
          self.updated()


   #-----------------------------------------------------------------------------
   # shallow copy 
   #-----------------------------------------------------------------------------
   def copy(self):
      """shallow copy of members into returned WordSet"""
      retVal = WordSet()
      retVal.words = self.words.copy()
      retVal.letterFreq = self.letterFreq.copy()
      return retVal


   #-----------------------------------------------------------------------------
   # words have been updated
   #-----------------------------------------------------------------------------
   def updated(self):
      """Object's words have been updated, so redo the letter frequency count."""

      # This list comprehension version is much faster than the below loop,
      # at the cost of the memory used by the transient list it creates.
      self.letterFreq = collections.Counter([letter for sublist in map(set,self.words) for letter in sublist])

      #letterFreq = collections.Counter()
      #for word in self.possibleWords:
      #   # update counter with word's letters (repeated letters removed)
      #   letterFreq.update(set(word))


   #-----------------------------------------------------------------------------
   # len(WordSet)
   #-----------------------------------------------------------------------------
   def __len__(self):
      """WordSet's length is the length of its words set. Which this returns"""

      return len(self.words)


   #-----------------------------------------------------------------------------
   # print out function
   #-----------------------------------------------------------------------------
   def __str__(self):
      """WordSet's representation as a string"""

      return str(self.words) + " " + str(self.letterFreq)



#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == '__main__':
   foo = WordSet()
   bar = WordSet(set(["CAT", "HAT"]))
   print("Empty:", foo)
   print("Not:  ", bar)

   baz = bar.copy()
   baz.words.add("FAT")
   baz.updated()
   print("2:", bar)
   print("3:", baz)
