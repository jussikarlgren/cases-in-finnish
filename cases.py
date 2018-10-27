import morphology
import hyperdimensionalsemanticspace
from nltk import sent_tokenize
from nltk import word_tokenize
import readrawtext


def nop(dummy):
    # do nothing
    return None


tokenutterancespace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
featureutterancespace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
lemmautterancespace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
tokencontextspace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
featurecontextspace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
lemmatextspace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
featurecollocationspace = hyperdimensionalsemanticspace.SemanticSpace(2000, 10)
morphology.read_dictionary('/home/jussi/data/1.case/analyses.mini.json')

featurecontextspace.observe("KO")
featurecontextspace.observe("KAAN")
featurecontextspace.observe("HAN")
featurecontextspace.observe("PA")
featurecollocationspace.observe("KO")
featurecollocationspace.observe("KAAN")
featurecollocationspace.observe("HAN")
featurecollocationspace.observe("PA")

window = 2
texts = readrawtext.readtexts()
readrawtext.readstats()
textbag = []
flag = []
textflag = []
for text in texts:
    ss = sent_tokenize(text.lower())
    for sent in ss:
        words = word_tokenize(sent)
        i = 0
        for word in words:
            i += 1
            textbag.append(word)
            if morphology.known(word):
                flag.append(word)
                r = morphology.lookup(word)
                textflag.append(r["lemma"])
                lhs = words[i-window:i]
                rhs = words[i+1:i+window+1]
                tokencontextspace.observe(word)
                featurecontextspace.observe(r["case"])
                featurecontextspace.observe(r["num"])
                if "poss" in r:
                    featurecontextspace.observe(r["poss"])
                featurecollocationspace.observe(r["case"])
                featurecollocationspace.observe(r["num"])
                if "poss" in r:
                    featurecollocationspace.observe(r["poss"])
                for l in lhs:
                    tokencontextspace.addintoitem(word, l, readrawtext.weight(word),
                                                  "before")
                    featurecontextspace.addintoitem(r["case"], l, 1,
                                                  "before")
                    featurecontextspace.addintoitem(r["num"], l, 1,
                                                    "before")
                    if "poss" in r:
                        featurecontextspace.addintoitem(r["poss"], r, 1,
                                                    "before")
                    if "KO" in l:
                        featurecontextspace.addintoitem("KO", l, 1,
                                                        "before")
                    if "KAAN" in l:
                        featurecontextspace.addintoitem("KAAN", l, 1,
                                                        "before")
                    if "HAN" in l:
                        featurecontextspace.addintoitem("HAN", l, 1,
                                                        "before")
                    if "PA" in l:
                        featurecontextspace.addintoitem("PA", l, 1,
                                                        "before")
                for rw in rhs:
                    tokencontextspace.addintoitem(word, rw, readrawtext.weight(word),
                                                  "after")
                    featurecontextspace.addintoitem(r["case"], rw, 1,
                                                  "after")
                    featurecontextspace.addintoitem(r["num"], rw, 1,
                                                    "after")
                    if "poss" in r:
                        featurecontextspace.addintoitem(r["poss"], rw, 1,
                                                    "after")
                    if "KO" in r:
                        featurecontextspace.addintoitem("KO", rw, 1,
                                                    "after")
                    if "KAAN" in r:
                        featurecontextspace.addintoitem("KAAN", rw, 1,
                                                    "after")
                    if "HAN" in r:
                        featurecontextspace.addintoitem("HAN", rw, 1,
                                                    "after")
                    if "PA" in r:
                        featurecontextspace.addintoitem("PA", rw, 1,
                                                    "after")
                ffs = [r["case"], r["num"]]
                if "poss" in r:
                    ffs.append(r["poss"])
                if "KO" in r:
                    ffs.append("KO")
                if "KAAN" in r:
                    ffs.append("KAAN")
                if "HAN" in r:
                    ffs.append("HAN")
                if "PA" in r:
                        ffs.append("PA")
                for fff in ffs:
                    for eee in ffs:
                        if fff != eee:
                                featurecollocationspace.addintoitem(fff, eee)
        for knownword in flag:
            textflag.append(knownword)
            r = morphology.lookup(knownword)
            tokenutterancespace.observe(knownword)
            featureutterancespace.observe(r["case"])
            featureutterancespace.observe(r["num"])
            if "poss" in r:
                featureutterancespace.observe(r["poss"])
            lemmautterancespace.observe(r["lemma"])
            for word in words:
                tokenutterancespace.addintoitem(knownword, word)
                featureutterancespace.addintoitem(r["case"], word)
                featureutterancespace.addintoitem(r["num"], word)
                if "poss" in r:
                    featureutterancespace.observe(r["poss"], word)
                lemmautterancespace.addintoitem(r["lemma"], word)
        flag = []
    for knownlemma in textflag:
        for word in textbag:
            lemmatextspace.addintoitem(knownlemma, word)
    textflag = []
    textbag = []

for s in [tokencontextspace, featurecontextspace, featurecollocationspace,
          tokenutterancespace, featureutterancespace, lemmautterancespace,
          lemmatextspace]:
    for i in s.contextspace:
        print(i)
        print(s.contextneighbours(i))

