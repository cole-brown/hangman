#!/usr/bin/env python3

import time
import os

#-------------------------------------------------------------------------------
# Prints stuff
#-------------------------------------------------------------------------------
def DBG(printable, printFlag=True, prefix=None):
   """No one likes bugs..."""
   if printFlag:
      if prefix:
         print(prefix, printable)
      else:
         print(printable)


#===============================================================================
# http://preshing.com/20110924/timing-your-code-using-pythons-with-statement
#===============================================================================
class Timer:
   """Times code with the with statement. E.g.
   
   with Timer() as t:
      conn = httplib.HTTPConnection('google.com')
      conn.request('GET', '/')
   print('Request took %.03f sec.' % t.interval)

   Add in try/finally for timing even with exceptions."""
   def __enter__(self):
      self.start = self.getTime()
      return self

   def __exit__(self, *args):
       self.end = self.getTime()
       self.interval = self.end - self.start

   def getTime(self):
      """Uses most accurate clock, based on platform. See:
      http://docs.python.org/library/timeit.html#timeit.default_timer"""
      if os.name == 'nt':
         # clock() has best accuracy on Windows
         return time.clock()
      else:
         # time() has best accuracy on Unix
         return time.time()
      

#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == "__main__":
   with Timer() as t:
      DBG("util.py - nothing to do here.", True)
      DBG("util.py - nothing to do here.", True, " > ")
      time.sleep(1)

   print("That took %.09f sec." % t.interval)

