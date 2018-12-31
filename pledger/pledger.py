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
"""

import docopt

from . import csvimporter as cim
from . import tokenizer as tkn
import pandas as pd

class Settings(object):
    def __init__(self, argv):
        self.argv = argv
        
        self.input = argv["<input>"]
        self.sep = argv["-s"]
        self.header = 0 if argv["-H"] else None
        self.names = self.get_names(argv["--names"])
    
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
        data = cim.read_csv(stng.input,
                            sep=stng.sep,
                            header=stng.header,
                            names=stng.names,
                            usecols=[2,3])
        
        data[2] = data[2].str.upper().str.replace("[.,-/()*0-9]", "").str.split()
        data[2] = data[2].apply(lambda x: list(set(x)))
        
        with open("test.dat", "w") as f:
            f.write(data[2].to_csv())
        
        tokens = []
                
        for t in data[2]:
            tokens += t
        
        tokens = pd.Series(sorted(tokens))
        
        accounts = []
        
        for a in data[3]:
            accounts.append(a)
        
        accounts = pd.Series(sorted(accounts))
        
        print(tokens.value_counts(normalize=True))
        print(accounts.value_counts(normalize=True))
        
        pairs = []
        
        for _, row in data.iterrows():
            a = row[3]
            pairs += [(tkn,a) for tkn in row[2]]
        
        pairs = pd.Series(pairs)
        
        print(pairs.value_counts(normalize=True))
