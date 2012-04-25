#! /usr/bin/env python

"""
A smart script to iterate all files in a directory, then show every file 
which has a specific string in it with the line numbers.

2012 Galuh Utama <galuh.utama@gwutama.de>
Licensed under GPLV3
"""

import os, fnmatch, sys, re, argparse

class Colors:
    """
    Pretty colors for output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Textfinder:
    wildcard = None
    regex = None
    interactive = False
    replacement = None

    num_files = 0
    num_dirs = 0
    num_matches_strings = 0
    num_matches_files = 0
    num_replaces = 0


    def __init__(self, wildcard, regex, interactive=False, replacement=None):
        self.wildcard = wildcard
        self.regex = regex
        self.interactive = interactive
        self.replacement = replacement


    def textfinder(self, directory):
        """
        Finds a string inside files in a directory and pretty print them.
        """
        # iterate every file in this directory
        for file in os.listdir(directory):
            # call textfinder again if this is a directory, 
            # otherwise,find matches if it matches the wildcard.
            file = directory + '/' + file

            if os.path.isdir(file):
                self.textfinder(file)
                self.num_dirs += 1
            elif fnmatch.fnmatch(file, self.wildcard) and os.path.isfile(file):
                matches = self.search_string(file)
                if matches:
                    self.num_matches_strings += len(matches)
                    self.num_matches_files += 1
                    self.num_files += 1
                    print Colors.OKGREEN + '%s' % (file, )                

                if matches and self.replacement == None:
                    for match in matches:
                        print match
                    print Colors.ENDC
                    if self.interactive:
                        raw_input()
                elif matches and self.replacement:
                    self.replace_string(file)
                    print Colors.OKGREEN + 'End of file'               
            else:
                self.num_files += 1


    def search_string(self, filename):
        """
        Search something in a file based on regex. Prints out the occurence 
        with the line numbers.
        """
        f = open(filename, 'r')
        matches = []

        # compile regex first
        regex = '(.*)(%s)(.*)' % (self.regex,)
        prog = re.compile(regex)    

        # iterate every line in the file and print matches
        i = 0
        for line in f:
            i += 1
            if prog.match(line):
                stripped = line.strip()
                match = self._format_line(i, stripped, regex)
                matches.append(match)
        f.close()
        return matches


    def replace_string(self, filename):
        """
        Replaces string occurences in a file. Always in interactive mode.
        """
        data = []
        f = open(filename, 'r')
        rplregex = self.regex
        rplregex2 = '(.*)(%s)(.*)' % (self.replacement,)
        regex = '(.*)(%s)(.*)' % (self.regex,)
        prog = re.compile(regex)    

        # iterate every line in the file and print matches replaced line preview
        i = 0
        for line in f:
            i += 1
            if prog.match(line):
                stripped = line.strip()

                # formatted match
                print self._format_line(i, stripped, regex)

                # formatted replacement preview
                text = re.sub(rplregex, self.replacement, stripped)            
                print self._format_line(i, text, rplregex2)

                answer = raw_input('Replace string? [y/n]\n')
                # ignore 'n' only consider for 'y' answer
                if answer == 'y':
                    change = re.sub(rplregex, self.replacement, line)
                    data.append(change)
                    self.num_replaces += 1
                else:
                    data.append(line) 
            else:
                data.append(line)
        f.close()

        # write data to file
        f = open(filename, 'w')
        f.writelines(data)    
        f.close()


    def _format_line(self, head, content, regex):
        """
        Formats a line with color. Head is for example for the line number,
        while content is the text to print itself.
        Regex is used to higlight some portion of the resulting text.
        """
        text = re.sub(regex, '\\1' + Colors.WARNING + '\\2' + 
                Colors.ENDC + '\\3', content)
        fmt = '%s%03d  %s%s' % (Colors.OKBLUE, head, Colors.ENDC, text,)
        return fmt


    def summary(self):
        """
        Prints the summary
        """
        print Colors.ENDC
        print 'Summary'
        print '-------'
        print 'Directories iterated:\t%d' % (self.num_dirs)
        print 'Files iterated:\t\t%d' % (self.num_files)
        print 'Matched files:\t\t%d' % (self.num_matches_files)
        print 'Matched strings:\t%d' % (self.num_matches_strings)
        print 'Replaced strings:\t%d' % (self.num_replaces)
        print


def main():
    """
    The main function to run the whole script.
    """
    parser = argparse.ArgumentParser(description="""A smart script to iterate 
                all files recursively  in a directory, then show every file
                which has a specific string in it.""",
                epilog='example: textfinder /home/foo/ *.cpp something')

    parser.add_argument('directory', nargs=1, help='Base directory')
    parser.add_argument('wildcard', nargs=1, help='Unix style file name match')
    parser.add_argument('regex', nargs=1, help='Regular expression')    
    parser.add_argument('--interactive', '-i', help="""Stop on every match, does
        not have effect when --replacement flag is set""", 
        action='store_true')
    parser.add_argument('--replacement', '-r', help="""Replacement string. 
        Regular expression captures can be used. If set, textfinder will attempt
        to replace occurences in files. Will be run in interactive mode.""")

    args = parser.parse_args()

    # valid directory?
    if os.path.isdir(args.directory[0]) == False:
        print 'Error: Not a directory: %s' % (directory,)
        help()        
        sys.exit(2)

    # Run the finder function now.
    try:
        finder = Textfinder(wildcard=args.wildcard[0], regex=args.regex[0],
                    interactive=args.interactive, replacement=args.replacement)
        finder.textfinder(args.directory[0])
        finder.summary()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main();

