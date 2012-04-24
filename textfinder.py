#! /usr/bin/env python

"""
A very smart script to iterate all files in a directory,
then show every file which has a specific string in it with the line numbers.

2012 Galuh Utama <galuh.utama@gwutama.de>
Licensed under GPLV3
"""

import os
import sys
import re
import glob


class Colors:
    """
    Pretty color for output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def search_string(filename, regex):
    """
    Search something in a file based on regex.
    Prints out the occurence with the line numbers.
    """
    f = open(filename, 'r')
    matches = []

    # compile regex first
    regex = '(.*)(%s)(.*)' % (regex,)
    prog = re.compile(regex)    

    # iterate every line in the file and print matches
    i = 0
    for line in f:
        i = i+1
        if prog.match(line):
            text = line.rstrip()
            text = re.sub(regex, '\\1' + Colors.WARNING + '\\2' + Colors.ENDC + '\\3', text)
            match = ' %s%03d  %s%s' % (Colors.HEADER, i, Colors.ENDC, text,)
            matches.append(match)
    return matches


def textfinder(directory, wildcard, regex):
    """
    Finds a string inside files in a directory
    and pretty print them.
    """
    # iterate every file in this directory
    path = directory + '/'
    for filename in glob.glob(path + wildcard):
        matches = search_string(filename, regex)
        # print if matches found
        if matches:
            # pretty print filename first
            print Colors.OKBLUE  + '---------------------------------------------------------------------'
            print Colors.OKGREEN + ' %s' % (filename, )
            print Colors.OKBLUE  + '---------------------------------------------------------------------'
            
            # now print every match
            for match in matches:
                print match

            print Colors.OKBLUE  + '---------------------------------------------------------------------'
            print Colors.ENDC


def help():
    """
    Displays the help section.
    """
    print "---------------------------------------------------------"
    print "Text Finder"
    print "---------------------------------------------------------"
    print "A smart script to iterate all files in a directory,"
    print "then show every file which has a specific string in it"
    print "with the line numbers."
    print
    print "2012 Galuh Utama <galuh.utama@gwutama.de>"
    print "Licensed under GPLV3"
    print
    print "Usage: ./textfinder DIRECTORY FILE_WILDCARD REGEX"
    print


def main():
    """
    The main function to run the whole script.
    """
    # only consider the second and the third arguments
    # and if argc equals to 4
    if len(sys.argv) != 4:
        help()
        print 'Error: Wrong number of arguments'
        sys.exit(2)

    # good number of arguments, now check whether they are valid
    directory = sys.argv[1]
    wildcard = sys.argv[2]
    regex = sys.argv[3]

    # valid directory?
    if os.path.isdir(directory) == False:
        print 'Error: Not a directory: %s' % (directory,)
        help()        
        sys.exit(2)

    # At this point we will assume that regex and wildcard are always right anyway
    # Run the finder function now.
    textfinder(directory, wildcard, regex)
    

if __name__ == '__main__':
    main();

