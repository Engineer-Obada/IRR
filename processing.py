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
nlp = spacy.load(r'C:\Python310\Lib\site-packages\en_core_web_lg\en_core_web_lg-3.3.0')


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
        array_for_precision = []
        c = 0
        for r in sortdoc:
            c += 1
            result_query.append(r)
            if c == 11:
                break
            print("num of query", q, "result_query", result_query)
        print("doc", doc)
        lenght_of_doc=len(doc)
        lenght_of_result_query =len(result_query)
        print("lenght_of_doc",lenght_of_doc)
        print("sort_doc", sortdoc)
        count_pre_recall = 0
        for i in sortdoc:
            array_for_precision.append(i)
        print("array_for_precision",array_for_precision)
        string = convert_to_string.convert(result_query)
        print("string::=",string)
        sortdoc.clear()
        result_query.clear()
        doc.clear()
        ###############3
        mapping = evaluations.read_mappings()
        print("mapping value::",mapping['1'])
        count_pr10 =0
        map_index=mapping[str(q)]
        print("map_index",map_index)
        for i in string:
            if i in map_index:
                count_pr10=count_pr10+1
        print("count",count_pr10)
        array_for_precision_to_string = convert_to_string.convert(array_for_precision)
        for i in array_for_precision_to_string:
            if i in map_index:
                count_pre_recall += 1
        print("count_pre_recall",count_pre_recall)
        precision =0.0
        recall =0.0
        precision10=0.0
        precision=float(count_pre_recall)/float(lenght_of_doc)
        print("precision",precision)
        avg +=precision
        recall= float(count_pre_recall)/float(len(map_index))
        print("recall",recall)
        precision10 =float(count_pr10)/float(lenght_of_result_query)
        print("precision@10",precision10)
        for i ,d in enumerate(string):
            if d in map_index:
                reciprocal_rank =1/(i+1)
                print("reciprocal_rank", reciprocal_rank, "i=", i)
                total_rr += reciprocal_rank
                print("total_rr", total_rr)
                break
    MAP = avg/112
    print("MAP",MAP)
    MAA=total_rr/112
    print("MAA=",MAA)

    for a in range(1,500):
        temp_dic2 = diction.get(a).copy()
        #print("rrrrrrrrrrrr",temp_dic2)
        diction.get(a).clear()
        # print(temp_dic2)
        # for y in list(dict.fromkeys(tokines)):
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



