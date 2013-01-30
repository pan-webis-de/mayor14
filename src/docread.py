import re

def txt(filename):
    with open(filename) as fh:
        wds = fh.read('\W+', fh.read())
    return wds
        
