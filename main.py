import cutting_dataSet1
import cutting_queries1
import cutting_queries2
import date_parsing
import limitization
import normalizeation
import processing
import processing2
import processing2_without_word
import evaluation2_befor_word
import query_correction
import read_terms
import math
from tkinter import *
import re
import stemming
import stop_word_removal,processing_without_word
import vectorMath
from textblob import TextBlob
from cutting_queries1 import read_queries
import evaluation_befor_word
import cutting_dataSet2
#________________________________________________________________________________________________


cutting_dataSet1

cutting_dataSet2

queries =cutting_queries1.read_queries()

queries2 = cutting_queries2.read_queries()

diction=processing_without_word.build_vec_mod()

diction2=processing2_without_word.build_vec_mod()

#calculate_evaluation.clculate_pre_recall()
print("/////////////////////////////////////////////////////////////////////////")

evaluation_befor_word.calculate()

evaluation2_befor_word.calculate()

word_embadding = processing.build_vec_mod()

word_embadding2 = processing2.build_vec_mod()

saved_terms=read_terms.read_terms()








def search():
    q = input1.get("1.0", "end-1c")
    print("cccccccccccccccccccccccccccc",type(q))

    corrected_query = ""
    for i in re.findall("\S+", q.lower()):
        print("iii",i)
        print("original text: " + str(i))
        b = TextBlob(i)
        print("corrected text: " + str(b.correct()))
        corrected_query += str(b.correct()) + " "
    if q != correctQuery:
        correctQuery.delete(0, END)  # reset the output field
        correctQuery.insert(0, corrected_query)  # write in output field

    ## processing the query
    # read stop words
    f = open("common_words", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)

    termsInQuery = []  # this contain all terms in query without stop words
    terms = []  #
    dates = date_parsing.ourDate(q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(0[1-9]|1[012])"
                          "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                          "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(January|February|March|April|May|June|July|August|September|October|November|December)"
                          "[/.-](\d{4})", "", q)
    dates = date_parsing.convert_to_regular_date(dates)

    # processing year
    years = re.findall("\d{4}", q)
    q = re.sub("\d{4}", "", q)

    q = q.lower()
    q = normalizeation.do_normalize(q)

    verbs_nounes = limitization.filter_verbs_nouns(q)
    verbs = stop_word_removal.remove_stop_words(verbs_nounes[0], stop_words)
    nounes = stop_word_removal.remove_stop_words(verbs_nounes[1], stop_words)

    verbs = limitization.do_limitize(verbs)
    nounes = stemming.do_stemming(nounes)
    termsInQuery.extend(verbs)
    termsInQuery.extend(nounes)
    termsInQuery.extend(years)
    termsInQuery.extend(dates)

    diction_query = {}  # dictionary for  terms and its frequencies
    for y in termsInQuery:
        diction_query.update({y: (1 + math.log(termsInQuery.count(y), 10)).__round__(5)})

    # remove duplication from termsInQuery
    tempTerms = []
    for w in termsInQuery:
        if w not in tempTerms:
            tempTerms.append(w)

    termsInQuery = tempTerms

    # # Extension of the previous diction in order to contain all terms
    # # and show their repetition within the query
    temp_dic2 = diction_query.copy()
    diction_query.clear()

    for term in saved_terms:
        if term not in temp_dic2.keys():
            diction_query.update({term: 0.0})
        else:
            diction_query.update({term: temp_dic2[term]})
            # diction_query.update({y: 505})

    # for x, y in diction_query.items():
    #     print(x," ====> ", y)

    # # check if vector of the query is zero or not , if was zero that mean the query
    # # will not return any results
    len_vec_query = vectorMath.length_vector(list(diction_query.values()))
    if len_vec_query != 0.0:
        result = processing.find_relevance_documents(list(diction_query.values()), diction)
        result_query = ""
        print("result::", result)

        reslist = sorted(result.items(), key=lambda x: x[1])
        sortdict = dict(reslist)

        c = 0
        for r in sortdict:
            c += 1
            result_query += "d({}) -".format(r)
            if c == 11:
                break

        #######################################################################


        output1.delete(0, END)  # reset the output field
        output1.insert(0, result_query)  # write in output field
    else:
        output1.delete(0, END)  # reset the output field
        output1.insert(0, "Sorry No Results")  # write in output field


#____________________________________________________________________________________________________________

def search2():
    q = input1.get("1.0", "end-1c")
    print("cccccccccccccccccccccccccccc",type(q))

    corrected_query = ""
    for i in re.findall("\S+", q.lower()):
        print("original text: " + str(i))
        b = TextBlob(i)
        print("corrected text: " + str(b.correct()))
        corrected_query += str(b.correct()) + " "
    if q != correctQuery:
        correctQuery.delete(0, END)  # reset the output field
        correctQuery.insert(0, corrected_query)  # write in output field

    ## processing the query
    # read stop words
    f = open("common_words", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)

    termsInQuery = []  # this contain all terms in query without stop words
    terms = []  #
    dates = date_parsing.ourDate(q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(0[1-9]|1[012])"
                          "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                          "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(January|February|March|April|May|June|July|August|September|October|November|December)"
                          "[/.-](\d{4})", "", q)
    dates = date_parsing.convert_to_regular_date(dates)

    # processing year
    years = re.findall("\d{4}", q)
    q = re.sub("\d{4}", "", q)

    q = q.lower()
    q = normalizeation.do_normalize(q)

    verbs_nounes = limitization.filter_verbs_nouns(q)
    verbs = stop_word_removal.remove_stop_words(verbs_nounes[0], stop_words)
    nounes = stop_word_removal.remove_stop_words(verbs_nounes[1], stop_words)

    verbs = limitization.do_limitize(verbs)
    nounes = stemming.do_stemming(nounes)
    termsInQuery.extend(verbs)
    termsInQuery.extend(nounes)
    termsInQuery.extend(years)
    termsInQuery.extend(dates)

    diction_query = {}  # dictionary for  terms and its frequencies
    for y in termsInQuery:
        diction_query.update({y: (1 + math.log(termsInQuery.count(y), 10)).__round__(5)})

    # remove duplication from termsInQuery
    tempTerms = []
    for w in termsInQuery:
        if w not in tempTerms:
            tempTerms.append(w)

    termsInQuery = tempTerms

    # # Extension of the previous diction in order to contain all terms
    # # and show their repetition within the query
    temp_dic2 = diction_query.copy()
    diction_query.clear()

    for term in saved_terms:
        if term not in temp_dic2.keys():
            diction_query.update({term: 0.0})
        else:
            diction_query.update({term: temp_dic2[term]})
            # diction_query.update({y: 505})

    # for x, y in diction_query.items():
    #     print(x," ====> ", y)

    # # check if vector of the query is zero or not , if was zero that mean the query
    # # will not return any results
    len_vec_query = vectorMath.length_vector(list(diction_query.values()))
    if len_vec_query != 0.0:
        result = processing2.find_relevance_documents(list(diction_query.values()), diction2)
        result_query = ""
        print("result::", result)

        reslist = sorted(result.items(), key=lambda x: x[1])
        sortdict = dict(reslist)

        c = 0
        for r in sortdict:
            c += 1
            result_query += "d({}) -".format(r)
            if c == 11:
                break

        #######################################################################

        output1.delete(0, END)  # reset the output field
        output1.insert(0, result_query)  # write in output field
    else:
        output1.delete(0, END)  # reset the output field
        output1.insert(0, "Sorry No Results")  # write in output field


root = Tk()
root.title("IR")
root.minsize(600, 300)
lable1 = Label(root, text="Enter Your Query ...!?", font=("Arial Bold", 20))
lable1.pack()

# input1 = Entry(root, width=90)
input1 = Text(root, width=50, height=4)
input1.pack()

B = Button(root, text="search", font=("Arial Bold", 10), command=search)
B.pack()

lable1 = Label(root, text="correct query", font=("Arial Bold", 10))
lable1.pack()

correctQuery = Entry(root, width=80)
correctQuery.pack()

lable1 = Label(root, text="result", font=("Arial Bold", 10))
lable1.pack()

output1 = Entry(root, width=80)
output1.pack()

root.mainloop()
