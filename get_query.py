def get_current_query(q):
    with open("corpus1/queries1/{}.text".format(q), "r") as f:
         contentAQuery = f.read()
         f.close()
    return contentAQuery

