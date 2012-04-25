#! /usr/bin/env python

"""
A very smart script to iterate all files in a directory,
then show every file which has a specific string in it with the line numbers.

2012 Galuh Utama <galuh.utama@gwutama.de>
Licensed under GPLV3
"""

import os
import fnmatch
import sys
import re
import glob
import argparse


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
            match = '%s%03d  %s%s' % (Colors.OKBLUE, i, Colors.ENDC, text,)
            matches.append(match)
    return matches


def textfinder(directory, wildcard, regex, interactive):
    """
    Finds a string inside files in a directory
    and pretty print them.
    """
    # iterate every file in this directory
    for file in os.listdir(directory):
        # call textfinder again if this is a directory, 
        # otherwise,find matches if it matches the wildcard.
        file = directory + '/' + file
        if os.path.isdir(file):
            subdir = file
            textfinder(subdir, wildcard, regex, interactive)
        elif fnmatch.fnmatch(file, wildcard):
            matches = search_string(file, regex)
            if matches:
                print Colors.OKGREEN + '%s' % (file, )
                
                for match in matches:
                    print match

                print Colors.ENDC

                if interactive:
                    raw_input()


def main():
    """
    The main function to run the whole script.
    """
    parser = argparse.ArgumentParser(description="""A smart script to iterate
                all files recursively in a directory, then show every file
                which has a specific string in it.""")

    parser.add_argument('directory', nargs=1, help='Base directory')
    parser.add_argument('wildcard', nargs=1, help='Unix style file name match')
    parser.add_argument('regex', nargs=1, help='Regular expression')    
    parser.add_argument('--interactive', '-i', help='Stop on every match', action='store_true')

    args = parser.parse_args()

    # valid directory?
    if os.path.isdir(args.directory[0]) == False:
        print 'Error: Not a directory: %s' % (directory,)
        help()        
        sys.exit(2)

    # At this point we will assume that regex and wildcard are always right anyway
    # Run the finder function now.
    try:
        textfinder(args.directory[0], args.wildcard[0], args.regex[0], args.interactive)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main();

