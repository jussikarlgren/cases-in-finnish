import morphology
import hyperdimensionalsemanticspace
from nltk import sent_tokenize
from nltk import word_tokenize
import readrawtext


def nop(dummy):
    # do nothing
    return None


dimensionality = 2000
denseness = 10

# tokens x words context 2x2
tokencontextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "token vs wds, 2x2")
# tokens x words context sentence
tokenutterancespace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "token vs wds, utt")
# lemmas x cases context one token per entire corpus
lemmacasespace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "lemma x case")
# lemmas x cases per text
# lemmacasetextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality,denseness)

# feats x feats context one token per entire corpus
featurecollocationspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "feats vs feats")
# feats x words context sentence
featureutterancespace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "feats vs wds, utt")
# feats x words context 2x2
featurecontextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "feats vs wds, 2x2")

# lemmas x words context text (topical analysis)
# lemmatextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness)

morphology.read_dictionary('/home/jussi/data/1.case/analyses.mini.json')

clitics = ["KO", "KAAN", "KIN", "HAN", "PA"]
for cc in clitics:
    featurecontextspace.observe(cc)
    featurecollocationspace.observe(cc)

readrawtext.readstats()
window = 2
files = readrawtext.getfilelist()
i = 0
antalsatser = 0
antalord = 0
threshold = 0.1
for file in files:
    i += 1
    texts = readrawtext.doonetextfile(file)
    antalsatser += len(texts)
    flag = []
    for text in texts:
        ss = sent_tokenize(text.lower())
        for sent in ss:
            words = word_tokenize(sent)
            i = 0
            for word in words:
                i += 1
                if morphology.known(word):
                    flag.append(word)
                    featureset = morphology.lookup(word)
                    lemma = featureset["lemma"]
                    lemmacasespace.observe(lemma)
                    thesefeatures = []
                    for dd in ["case", "num", "poss"]:
                        if dd in featureset:
                            featurecontextspace.observe(featureset[dd], True, dd)
                            featurecollocationspace.observe(featureset[dd], True, dd)
                            thesefeatures.append(dd)
                    for cc in clitics:
                        if cc in featureset:
                            featurecontextspace.observe(cc, True, "clitic")
                            featurecollocationspace.observe(cc, True, "clitic")
                            thesefeatures.append(cc)
                    for fff in thesefeatures:
                        lemmacasespace.addintoitem(lemma, fff)
                        for eee in thesefeatures:
                            if fff != eee:
                                featurecollocationspace.addintoitem(fff, eee)
                    tokencontextspace.observe(word, True, lemma)
                    lhs = words[i-window:i]
                    rhs = words[i+1:i+window+1]
                    for lw in lhs:
                        tokencontextspace.addintoitem(word, lw, readrawtext.weight(word), "before")
                        for fff in thesefeatures:
                            featurecontextspace.addintoitem(fff, lw, 1, "before")
                    for rw in rhs:
                        tokencontextspace.addintoitem(word, rw, readrawtext.weight(word), "after")
                        for fff in thesefeatures:
                            featurecontextspace.addintoitem(fff, rw, 1, "after")
            if len(flag) >= 1:
                antalord += len(words)
            for knownword in flag:
                featureset = morphology.lookup(knownword)
                thesefeatures = []
                for dd in ["case", "num", "poss"]:
                    if dd in featureset:
                        featureutterancespace.observe(featureset[dd], True, dd)
                        thesefeatures.append(dd)
                for cc in clitics:
                    if cc in featureset:
                        featureutterancespace.observe(cc, True, "clitic")
                        thesefeatures.append(cc)
                tokenutterancespace.observe(knownword, True, featureset["lemma"])
                for word in words:
                    tokenutterancespace.addintoitem(knownword, word)
                    for fff in thesefeatures:
                        featureutterancespace.addintoitem(fff, word)
            flag = []
    if i > 3:
        i = 0
        print("==", antalsatser, antalord, "============", sep="\t")
        for s in [tokencontextspace, tokenutterancespace]:
            print(s.name, "----------", sep="\t")
            tokenneighbours = {}
            nabesize = {}
            for oneitem in s.contextspace:
                if s.tag[oneitem] not in tokenneighbours:
                    tokenneighbours[s.tag[oneitem]] = 0
                    nabesize[s.tag[oneitem]] = 0
                nabe = s.contextneighbours(oneitem, 0, True, True)
                for nnn in nabe:
                    tokenneighbours[s.tag[oneitem]] += nnn[1] / ((len(nabe) + 1) * len(nabe))
                    if nnn[1] > threshold:
                        nabesize[s.tag[oneitem]] += 1 / len(nabe)
            for lemma in tokenneighbours:
                print(lemma, tokenneighbours[lemma], nabesize[lemma], sep="\t")

        for s in [lemmacasespace]:
            print(s.name)
            for oneitem in s.contextspace:
                print(oneitem, s.contextneighbours(oneitem), sep="\t")

        for s in [featurecontextspace, featureutterancespace]:
            print(s.name)
            for oneitem in s.contextspace:
                print(oneitem, s.contextneighbours(oneitem, 0, True, True, 0), sep="\t")

        for s in [featurecollocationspace]:
            print(s.name)
            for oneitem in s.contextspace:
                print(oneitem, s.contextneighbours(oneitem, 0, True, False, 0), sep="\t")
