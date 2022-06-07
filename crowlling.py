import math
import re

import spacy

import date_parsing
import get_query
import limitization
import normalizeation
import processing_query
import stemming
import stop_word_removal
from scipy import spatial

nlp = spacy.load(r'C:\Python310\Lib\site-packages\en_core_web_lg\en_core_web_lg-3.3.0')

def doc_process():
    # read stop words
    f = open("common_words", "r")

    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)

    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction2 = {}  # dictionary for all tokens
    for x in range(1,400):
        f = open("corpus2/dataSet2/{}.text".format(x), "r")
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
    return  temp_dic



def query_doc():
    # read stop words
    f = open("common_words", "r")

    content = f.read() #content contain stopwords
    #print("content is :",content)
    f.close()
    stop_words = re.findall("\S+", content)

    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    reslist = {}
    sortdoc = {}
    doc = {}
    document_embadding = []
    query_embadding = []
    result_query = []
    reciprocal_rank = 0
    total_rr =  0
    avg = 0
    for q in range(1,2):
        query = get_query.get_current_query(q)
        query_after_process = processing_query.process_query(query)
        for x in range(1, 500):
            f = open("corpus1/dataSet1/{}.text".format(x), "r")
            contentAFile = f.read()
            # print("content in A file",x,"is",contentAFile)
            f.close()

            dates = date_parsing.ourDate(contentAFile)
            print(dates)
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

            doc_to_string = ' '.join(termsInAfile)
            query_to_string = ' '.join(query_after_process)
            document_embadding = list(nlp(doc_to_string).vector)
            query_embadding = list(nlp(query_to_string).vector)
            similarity = 1-spatial.distance.cosine(document_embadding,query_embadding)
            if similarity >0.3:
                doc.update({x: similarity})



            for w in termsInAfile:
                if w not in tokines:
                    tokines.append(w)

            temp_dic = {}  # dictionary for each term
            for y in termsInAfile:  # the key y is the name of term
                temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})
            diction.update({x: temp_dic})
            # print("document number : {} Done".format(x))
            termsInAfile.clear()

        reslist = sorted(doc.items(), key=lambda item: -item[1])
        # print("reslost", reslist)
        sortdoc = dict(reslist)
        # print("sorted",sortdoc)

    return diction