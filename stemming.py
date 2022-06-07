from nltk import PorterStemmer


def do_stemming(nounes):
    porter = PorterStemmer()
    porteredNouns = []
    for n in nounes:
        porteredNouns.append(porter.stem(n))

    nounes = porteredNouns
    return nounes