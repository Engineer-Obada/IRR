from textblob import TextBlob

import evaluations2
import get_query, processing_query, date_parsing, normalizeation, limitization, stop_word_removal, \
    stemming, read_terms, vectorMath, processing, processing_without_word, convert_to_string, evaluations

import re,math
def calculate():
    diction=processing_without_word.build_vec_mod()
    saved_terms = read_terms.read_terms()
    total_rr = 0
    avg = 0
    reciprocal_rank = 0
    for Q in range(1,6):
        q = get_query.get_current_query(Q)

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
            doc = processing.find_relevance_documents(list(diction_query.values()), diction)
            result_query = []
            print("result::", doc)

            reslist = sorted(doc.items(), key=lambda item: item[1])
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
                print("num of query", Q, "result_query", result_query)
            print("doc", doc)
            lenght_of_doc = len(doc)
            lenght_of_result_query = len(result_query)
            print("lenght_of_doc", lenght_of_doc)
            print("sort_doc", sortdoc)
            count_pre_recall = 0
            for i in sortdoc:
                array_for_precision.append(i)
            print("array_for_precision", array_for_precision)
            string = convert_to_string.convert(result_query)
            print("string::=", string)
            sortdoc.clear()
            result_query.clear()
            doc.clear()
            ###############3
            mapping = evaluations2.read_mappings()
            print("mapping value::", mapping['1'])
            count_pr10 = 0
            map_index = mapping[str(Q)]
            print("map_index", map_index)
            for i in string:
                if i in map_index:
                    count_pr10 = count_pr10 + 1
            print("count", count_pr10)
            array_for_precision_to_string = convert_to_string.convert(array_for_precision)
            for i in array_for_precision_to_string:
                if i in map_index:
                    count_pre_recall += 1
            print("count_pre_recall", count_pre_recall)
            precision = 0.0
            recall = 0.0
            precision10 = 0.0
            precision = float(count_pre_recall) / float(lenght_of_doc)
            avg += precision
            print("precision", precision)
            recall = float(count_pre_recall) / float(len(map_index))
            print("recall", recall)
            precision10 = float(count_pr10) / float(lenght_of_result_query)
            print("precision@10", precision10)
            for i, d in enumerate(string):
                if d in map_index:
                    reciprocal_rank = 1 / (i + 1)
                    print("reciprocal_rank", reciprocal_rank, "i=", i)
                    total_rr += reciprocal_rank
                    print("total_rr", total_rr)
                    break
    MAP = avg / 64
    print("MAP", MAP)
    MAA = total_rr / 64
    print("MAA=", MAA)
