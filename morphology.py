import json
from pprint import pprint


dictionary = {}


def known(word):
    if word in dictionary:
        return True
    else:
        return False


def read_dictionary(dictfile:str='/home/jussi/data/1.case/analyses.json') -> dict:
    '''Read the OMORFI dictionary which is in json form on disc.'''
    global dictionary
    with open(dictfile) as f:
        dictionary = json.load(f)
    return dictionary


def lookup(word:str) -> dict:
    '''Look up a word to see if it is in the loaded OMORFI dictionary. '''
    if known(word):
        return dictionary[word]
    else:
        return None
