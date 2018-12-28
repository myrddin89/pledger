"""
Pledger CLI helper tool

Usage:
    pledger [OPTIONS]

Arguments:

Options:
    -h --help       Display this help message and exit.
    -V --version    Print version and exit.
"""

import docopt

def main():
    argv = None
    
    try:
        argv = docopt.docopt(__doc__, version="pledger 0.1.0")
    except docopt.DocoptExit as e:
        print(e)
    else:
        print(argv)
