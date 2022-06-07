import nltk
from nltk import PunktSentenceTokenizer, WordNetLemmatizer
from nltk.corpus import state_union


def filter_verbs_nouns(s):
    train = state_union.raw("2005-GWBush.txt")
    # sample_text = open("corpus/1.txt", "r").read()
    # print(s)
    cust = PunktSentenceTokenizer(train)
    tok = cust.tokenize(s)

    # tokenized_word = word_tokenize(sample_text)
    # print(len(tokenized_word))
    # print(tokenized_word)
    verbs = []
    nouns = []
    for i in tok:
        words = nltk.word_tokenize(i)
        tag = nltk.pos_tag(words)
        for c in tag:
            # print(c[0])
            if c[1] == "VBD" or c[1] == "VBG" or c[1] == "VBN" or c[1] == "VBN" or c[1] == "VBP" or c[1] == "VBZ" or \
                    c[1] == "VP":
                verbs.append(c[0])
            else:
                nouns.append(c[0])

            # print(c[0])
            # print(c)

    return [verbs, nouns]

def do_limitize(verbs):
    lmtzr = WordNetLemmatizer()
    lemmatizedVerbs = []
    for v in verbs:
        lemmatizedVerbs.append(WordNetLemmatizer().lemmatize(v, 'v'))

    verbs = lemmatizedVerbs
    return verbs
