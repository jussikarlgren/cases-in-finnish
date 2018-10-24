import morphology
import hyperdimensionalsemanticspace

space = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
for item in morphology.lexicon:
    space.additem(item, False)
for item in morphology.casus:
    space.additem(item, False)
for item in morphology.clitics:
    space.additem(item, False)
for item in morphology.possessives:
    space.additem(item, False)
for item in morphology.numerus:
    space.additem(item, False)

# take a set of texts
# for each text, inspect to see if a word we know about appears
text = "a b c"
for word in text:
    if morphology.known(word):
        r = morphology.lookup(word)




# adjust items in space by cooccurrence
# for each item in space, output closest neighbours, separated by type (lexeme, number, case, possessive clitic)

