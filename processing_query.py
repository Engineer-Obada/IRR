import re,math

import date_parsing, normalizeation, limitization, stop_word_removal, stemming


def process_query(q):
    f = open("common_words", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)
    termsInQuery = []
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


    return tempTerms