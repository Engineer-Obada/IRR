import ast


def read_terms():
    ## read terms that extract from curpus
    f3 = open("terms.txt", "r")
    saved_terms = f3.read()
    f3.close()
    saved_terms = list(ast.literal_eval(saved_terms))
    return saved_terms

