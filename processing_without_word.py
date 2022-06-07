

import re, math
import spacy
# read stop words
from scipy import spatial

import date_parsing
import get_query, processing_query, evaluations, convert_to_string
import limitization
import normalizeation
import stemming
import stop_word_removal
import vectorMath
def find_relevance_documents(queryVector, diction):
    result = {}
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector = list(value_dic.values())
        result.update({key_dic: vectorMath.angle_between_two_vector(queryVector, vector)})
    return result


def build_vec_mod():
    # read stop words
    f = open("common_words", "r")

    content = f.read() #content contain stopwords
    #print("content is :",content)
    f.close()
    stop_words = re.findall("\S+", content)

    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    for x in range(1, 500):
        f = open("corpus1/dataSet1/{}.text".format(x), "r")
        contentAFile = f.read()
        # print("content in A file",x,"is",contentAFile)
        f.close()

        dates = date_parsing.ourDate(contentAFile)
        #print(dates)
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(0[1-9]|1[012])"
                              "[/.-](\d{4})", "", contentAFile)
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                              "[/.-](\d{4})", "", contentAFile)
        contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                              "(January|February|March|April|May|June|July|August|September|October|November|December)"
                              "[/.-](\d{4})", "", contentAFile)
        dates = date_parsing.convert_to_regular_date(dates)

        # processing year
        years = re.findall("\d{4}", contentAFile)
        contentAFile = re.sub("\d{4}", "", contentAFile)

        contentAFile = contentAFile.lower()
        contentAFile = normalizeation.do_normalize(contentAFile)

        verbs_nounes = limitization.filter_verbs_nouns(contentAFile)
        verbs = stop_word_removal.remove_stop_words(verbs_nounes[0], stop_words)
        nounes = stop_word_removal.remove_stop_words(verbs_nounes[1], stop_words)

        verbs = limitization.do_limitize(verbs)
        nounes = stemming.do_stemming(nounes)

        # new step

        termsInAfile.extend(verbs)
        termsInAfile.extend(nounes)
        termsInAfile.extend(dates)
        termsInAfile.extend(years)
        for w in termsInAfile:
            if w not in tokines:
                tokines.append(w)

        temp_dic = {}  # dictionary for each term
        for y in termsInAfile:  # the key y is the name of term
            temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})
        diction.update({x: temp_dic})

        termsInAfile.clear()
    for a in range(1,500):
        temp_dic2 = diction.get(a).copy()
        diction.get(a).clear()

        for y in tokines:
            if y not in temp_dic2.keys():
                diction.get(a).update({y: 0.0})
            else:
                diction.get(a).update({y: temp_dic2[y]})

    f1 = open("vector model.txt", "w")
    f1.write(str(diction))
    f1.close()

    f2 = open("terms.txt", "w")
    f2.write(str(tokines))
    f2.close()
    return diction