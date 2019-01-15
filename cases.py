import morphology
import hyperdimensionalsemanticspace
from nltk import sent_tokenize
from nltk import word_tokenize
import readrawtext
import time
import sparsevectors
import json

full = False  #  set to true for full word space (very expensive)
probes = True  # set to true to get an analysis of probe term space
profiles = False  # to get a profile similarity for lemmas wrt observed cases

debug = True

def nop(dummy):
    # do nothing
    return None

outputfile = "/home/jussi/aktuellt/1.case/tammikuu/finnish-cases-output.txt"

dimensionality = 2000
denseness = 10

# tokens x words context 2x2
tokencontextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "token vs wds, 2x2")
# tokens x words context sentence
tokenutterancespace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "token vs wds, utt")
# tokens x words context 2x2
fullcontextspace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "all token vs wds, 2x2")
# tokens x words context sentence
fullutterancespace = hyperdimensionalsemanticspace.SemanticSpace(dimensionality, denseness, "all token vs wds, utt")
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
j = 0
k = 0
antalsatser = 0
antalord = 0
threshold = 0.1
seen = set()
for file in files:
    with open(outputfile, "a") as f:
        f.write(f'{i}\t{j}\t{k}\t{file}\t{full}\t{probes}\t{profiles}\n')
    i += 1
    j += 1
    k += 1
    texts = readrawtext.doonetextfile(file)
    antalsatser += len(texts)
    flag = []
    for text in texts:
        ss = sent_tokenize(text.lower())
        for sent in ss:
            words = word_tokenize(sent)
            ii = 0
            for word in words:
                ii += 1
                lhs = words[ii - window:ii]
                rhs = words[ii + 1:ii + window + 1]
                if full:
                    fullcontextspace.observe(word)
                    fullutterancespace.observe(word)
                    for lw in lhs:
                        fullcontextspace.addintoitem(word, lw, readrawtext.weight(word), "before")
                    for rw in rhs:
                        fullcontextspace.addintoitem(word, rw, readrawtext.weight(word), "after")
                    for otherword in words:
                        fullutterancespace.addintoitem(word, otherword, readrawtext.weight(otherword))
                if morphology.known(word):
                    flag.append(word)
                    seen.add(word)
                    featureset = morphology.lookup(word)
                    thesefeatures = []
                    lemma = featureset["lemma"]
                    for dd in ["case", "num", "poss"]:
                        if dd in featureset:
                            featurecontextspace.observe(featureset[dd], True, dd)
                            featurecollocationspace.observe(featureset[dd], True, dd)
                            thesefeatures.append(featureset[dd])
                    for cc in clitics:
                        if cc in featureset:
                            featurecontextspace.observe(cc, True, "clitic")
                            featurecollocationspace.observe(cc, True, "clitic")
                            thesefeatures.append(cc)
                    if profiles:
                        lemmacasespace.observe(lemma)
                        for fff in thesefeatures:
                            lemmacasespace.addintoitem(lemma, fff)
                            for eee in thesefeatures:
                                if fff != eee:
                                    featurecollocationspace.addintoitem(fff, eee)
                    if probes:
                        tokencontextspace.observe(word, True, lemma)
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
            if probes:
                for knownword in flag:
                    featureset = morphology.lookup(knownword)
                    thesefeatures = []
                    for dd in ["case", "num", "poss"]:
                        if dd in featureset:
                            featureutterancespace.observe(featureset[dd], True, dd)
                            thesefeatures.append(featureset[dd])
                    for cc in clitics:
                        if cc in featureset:
                            featureutterancespace.observe(cc, True, "clitic")
                            thesefeatures.append(cc)
                    tokenutterancespace.observe(knownword, True, featureset["lemma"])
                    for word in words:
                        tokenutterancespace.addintoitem(knownword, word, readrawtext.weight(word))
                        for fff in thesefeatures:
                            featureutterancespace.addintoitem(fff, word)
            flag = []

#        for s in [tokencontextspace, tokenutterancespace]:
            # number of items in nabe (observed morphset)
            # number of other items with nabe radius
            # average distance ============from items to each other
            # average distance from centroid to all items
            # some good examples of neighbours outside morphset
            # potentially see if morphset can be separated into subsets based on geometry
    if i > 3 and probes:
        i = 0
        with open(outputfile, "a") as f:
            f.write(
                f'==\t{time.ctime()}\t==\t{antalsatser}\t==\t{antalord}\t============\t{full}\t{probes}\t{profiles}\n')
            for s in [tokencontextspace, tokenutterancespace]:
                f.write(s.name + "\t" + "----------\n")
                morphsetaveragedistance = {}
                morphsetaveragethresholdeddistance = {}
                morphsetaveragethresholdedsize = {}
                morphsetcentroiddistance = {}
                morphsetvectors = {}
                morphsetsize = {}
                morphset = {}
                morphsetcache = {}
                lemmafrequency = {}
                seenlemmas = []
                for oneitem in s.contextspace:
                    lemma = s.tag[oneitem]
                    if lemma not in seenlemmas:
                        seenlemmas.append(lemma)
                        morphsetaveragedistance[lemma] = 0
                        morphsetaveragethresholdedsize[lemma] = 0
                        morphsetaveragethresholdeddistance[lemma] = 0
                        morphsetcentroiddistance[lemma] = 0
                        morphsetvectors[lemma] = []
                        morphsetsize[lemma] = 0
                        morphset[lemma] = []
                        morphsetcache[lemma] = {}
                        lemmafrequency[lemma] = 0
                    lemmafrequency[lemma] += s.observedfrequency[oneitem]
                    morphset[lemma] = s.contextneighbours(oneitem, 0, True, True)  # get items with same lemma
                    morphsetsize[lemma] = len(morphset[lemma])
                    morphsetcache[lemma][oneitem] = morphset[lemma]
                    for nnn in morphset[lemma]:
                        morphsetvectors[lemma].append(s.contextspace[nnn[0]])
                        morphsetaveragedistance[lemma] += nnn[1]
                        if nnn[1] > threshold:
                            morphsetaveragethresholdedsize[lemma] += 1
                            morphsetaveragethresholdeddistance[lemma] += nnn[1]
                for observedlemma in seenlemmas:
                    a = 0
                    if morphsetsize[observedlemma] > 0:
                        a = morphsetaveragedistance[observedlemma] / (morphsetsize[observedlemma] *
                                                                      (morphsetsize[observedlemma] + 1))
                    c = sparsevectors.centroid(morphsetvectors[observedlemma])
                    m = sparsevectors.averagedistance(c, morphsetvectors[observedlemma], debug)
                    d = 0
                    if observedlemma in morphsetaveragethresholdedsize and \
                            morphsetaveragethresholdedsize[observedlemma] > 1:
                        d = morphsetaveragethresholdeddistance[observedlemma] / \
                            morphsetaveragethresholdedsize[observedlemma]
                    f.write(f"{observedlemma}\t{lemmafrequency[observedlemma]}\t{a}\t{m}\t{morphsetsize[observedlemma]}\t{d}\n")
                    f.write(f"\t\t\t{morphsetcache[observedlemma]}\n")
    if j > 3 and full:
        print("..", time.ctime(), "..", antalsatser, "..", antalord, "..........", full, probes, profiles, sep="\t")
        j = 0
        for s in [fullcontextspace, fullutterancespace]:
            print(s.name)
            for item in seen:
                nabe = s.contextneighbours(item, 10, True)
                print(item, nabe)
    if k > 3 and profiles:
        print("##", time.ctime(), "##", antalsatser, "##", antalord, "###", full, probes, profiles, sep="\t")
        k = 0
        for s in [lemmacasespace]:
            print(s.name)
            for oneitem in s.contextspace:
                print(oneitem, s.observedfrequency[oneitem], s.contextneighbours(oneitem, 10, True), sep="\t")
#        for s in [featurecollocationspace]:
#            json.dump(s.name)
#            for oneitem in s.contextspace:
#                json.dump(oneitem, s.contextneighbours(oneitem, 0, True, False, 0), sep="\t")
#
#        for s in [featurecontextspace, featureutterancespace]:
#            json.dump(s.name)
#            for oneitem in s.contextspace:
#                json.dump(oneitem, s.contextneighbours(oneitem, 0, True, True, 0), sep="\t")
#
