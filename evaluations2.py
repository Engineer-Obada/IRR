def read_mappings():
    f = open("corpus2/cacm/qrels.text")

    mappings = {}

    for a_line in f.readlines():
        voc = a_line.strip().split()
        key = voc[0].strip()
        current_value = voc[1].strip()
        #print("voc = ",voc) # voc is a line
        #print("key = ",key) # key is Query Id
        #print("current_value = ",current_value) #current_value is document id

        value = []
        if key in mappings.keys():
            value = mappings.get(key)
        value.append(current_value)
        mappings[key] = value

    f.close()
    print("mappings is",mappings)
    return mappings


#############################################################################################################33


def prefilter(doc_terms, query):
    docs = []
    for doc_id in doc_terms.keys():
        found = False
        i = 0
        while i<len(query.keys()) and not found:
            term = list(query.keys())[i]
            if term in doc_terms.get(doc_id).keys():
                docs.append(doc_id)
                found=True
            else:
                i+=1
    return docs

##############################################################################################################

def calculate_precision(model_output, gold_standard):
    true_pos = 0
    for item in model_output:
        if item in gold_standard:
            true_pos += 1
    return float(true_pos)/float(len(model_output))


######################################################################################################3
def prefilter(doc_terms, query):
    docs = []
    for doc_id in doc_terms.keys():
        found = False
        i = 0
        while i<len(query.keys()) and not found:
            term = list(query.keys())[i]
            if term in doc_terms.get(doc_id).keys():
                docs.append(doc_id)
                found=True
            else:
                i+=1
    return docs