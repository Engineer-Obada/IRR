import re


from main import correctQuery


import re, vectorMath
from tkinter import *
import ast
from textblob import TextBlob

from textblob.en import Spelling
from textblob import TextBlob

from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer




def queryCorrection(q):
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

