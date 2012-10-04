#!/usr/bin/env python3

"""top level doc string"""

# Python imports
import sys
from optparse import OptionParser

# local imports

# CONSTANTS

#-----------------------------------------------------------------------------
# function
#-----------------------------------------------------------------------------
def main(argv=None):
  """this is run when the file is evaluated"""
  if argv is None:
    argv = sys.argv
  try:
    parser = OptionParser()
#     parser.add_option("-f", "--file", dest="filename",
#                       help="write report to FILE", metavar="FILE")
#     parser.add_option("-q", "--quiet",
#                       action="store_false", dest="verbose", default=True,
#                       help="don't print status messages to stdout")

    (options, args) = parser.parse_args()


    # your code here
  except:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

#===============================================================================
#-------------------------------------------------------------------------------
#                                The Main Event
#-------------------------------------------------------------------------------
#===============================================================================
if __name__ == "__main__":
  sys.exit(main())

