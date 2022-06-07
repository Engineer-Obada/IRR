def remove_stop_words(t, st):
    clean_data = []
    for w in t:
        if w not in st:
            clean_data.append(w)

    return clean_data
