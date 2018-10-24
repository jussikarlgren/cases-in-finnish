dictionary = {}
clitics = {}
possessives = {}
numerus = {}
casus = {}

def known(word):
    if word in dictionary:
        return True
    else:
        return False

# read Tommi's files
def read_dictionary():
    global dictionary
    dictionary = {}

def lookup(word):
    if known(word):
        r = {}
        r["lemma"] = dictionary[word]
        r["luku"] = numerus[word]
        r["sija"] = casus[word]
        r["omistus"] = possessives[word]
        r["liite"] = clitics[word]
        return r
    else:
        return None
