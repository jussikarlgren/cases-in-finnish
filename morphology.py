dictionary = {}

def known(word):
    if word in dictionary:
        return True
    else:
        return False

# read Tommi's files
def read_dictionary():
    global dictionary
    dictionary = {}

