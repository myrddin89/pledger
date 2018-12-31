from pandas import read_csv as pdcsv

def read_csv(name, **kwargs):
    csv_file = pdcsv(name, **kwargs)
    
    return csv_file
