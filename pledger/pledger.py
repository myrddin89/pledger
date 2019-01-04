"""
Pledger CLI helper tool

Usage:
    pledger import [options] <input>

Commands:
    import              Import CSV file into ledger format.
    
Arguments:
    <input>             CSV file to import.
    
Options:
    -h --help           Display this help message and exit.
    -V --version        Print version and exit.
    -l FILE             An existing ledger file to learn accounts from.
    -s SEPARATOR        Separator for parsing the CSV file. [default: ,]
    -H                  Specifies if the CSV file has header line.
    --names NAMES       List of column names.
    -L LENGTH           Number of tokens to consider for training.
"""

import docopt

from . import csvimporter as cim
from . import tokenizer as tkn
import pandas as pd
import numpy as np

class Settings(object):
    def __init__(self, argv):
        self.argv = argv
        
        self.input = argv["<input>"]
        self.sep = argv["-s"]
        self.header = 0 if argv["-H"] else None
        self.names = self.get_names(argv["--names"])
        self.length = int(argv["-L"])
    
    def get_names(self, names):
        if names is None:
            return None
        
        return [nm.strip() for nm in names.split(",")]
            
            
            
def main():
    argv = None
    
    try:
        argv = docopt.docopt(__doc__, version="pledger 0.1.0")
    except docopt.DocoptExit as e:
        print(e)
    else:
        stng = Settings(argv)
        input_data = cim.read_csv(stng.input,
                                  sep=stng.sep,
                                  header=stng.header,
                                  names=stng.names,
                                  usecols=[2,3])
        
        input_data.columns = ["tokens", "accounts"]
        input_data.tokens = input_data.tokens.str.upper().str.replace("[.,-/()*0-9]", "").str.split()
        input_data.tokens = input_data.tokens.apply(lambda x: list(set(x)))
        
        tkn_data = input_data.tokens.apply(pd.Series).stack().reset_index(level=1, drop=True)
        tkn_data.name = 'tokens'
        data = input_data.drop('tokens', axis=1).join(tkn_data).reset_index(drop=True)
        data = data.groupby(['tokens', 'accounts']).size()
        data = data / data.sum()
        
        with open("test.dat", "w") as f:
            f.write(data.to_csv())
