import numpy
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

############################################################
# CIS 521: Homework 1
############################################################
"""
student_name = "Ankita Patel"

# This is where your grade report will be sent.
student_email = "ankip@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = "Strongly typed means variables
do have type and the type matters when performing operations.
Interpreter keeps track of all variable types and not allow
anything that's incompatible with the type of the data involved.
For example, if variable x holds string type and variable y holds
int type, then we cannot add those two.
x = 'someString'
y = 9
result = x + y

Dynamically typed means a variable is simply a value bound to
a name; the value has a type -- like "integer" or "string" or
"list" -- but the variable itself doesn't. You could have a
variable which, right now, holds a number, and later assign a
 string to it if you need it to change.

x = 9
x = 'myString"
"

python_concepts_question_2 = "Python requires its dictionary
key value to be of immutable type. Since the given code snippet
uses list as a key which is mutable, error occurs. To fix this,
keys can be changed to tuple type and since tuple is immutable, the
code will be acceptable.
points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
"

python_concepts_question_3 = "The first method uses for loop and the
second method uses .join method which is significantly faster than the
first method for the larger input. The .join method uses iterator which counts
the number of strings to join and hence reduces the number of steps required
to join those strings compared to for loop.
"
"""
############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [x for row in seqs for x in row]


def transpose(matrix):
    for x in matrix:
        matrixSize = len(x)
    result = []
    i = 0
    while (i < matrixSize):
        rowMatrix = []
        for x in matrix:
            rowMatrix.append(x[i])
        result.append(rowMatrix)
        i += 1
    return result

############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    newSeq = seq[:]
    return newSeq


def all_but_last(seq):
    if not seq:
        return seq
    new_Seq = seq[:-1]
    return new_Seq


def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    lenSeq = len(seq)
    i = 0
    while i <= lenSeq:
        yield seq[:i]
        i += 1


def suffixes(seq):
    lenSeq = len(seq)
    i = 0
    while i <= lenSeq:
        yield seq[i:lenSeq]
        i += 1


def slices(seq):
    lenSeq = len(seq)
    i = 0
    while i <= lenSeq:
        j = i
        while j < lenSeq:
            yield seq[i:j+1]
            j += 1
        i += 1

############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    text = text.strip().lower()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def no_vowels(text):
    vowels = ('a', 'e', 'i', 'o', 'u')
    for ch in text:
        if ch.lower() in vowels:
            text = text.replace(ch, "")
    return text


def digits_to_words(text):
    digitStr = ""
    num2Words = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three',
                 '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
                 '8': 'eight', '9': 'nine'}
    for t in text:
        if t in num2Words.keys():
            digit = num2Words.get(t)
            digitStr = digitStr + " " + digit
    return digitStr.strip()


def to_mixed_case(name):
    wordLst1 = name.split("_")
    wordLst = [word for word in wordLst1 if word != ""]
    listLen = len(wordLst)
    if listLen == 0:
        return ""
    wordLst[0] = wordLst[0].lower()
    i = 1
    while i < listLen:
        wordLst[i] = wordLst[i].capitalize()
        i += 1
    newStr = "".join(wordLst)
    return newStr

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        tupleLst = list(self.get_polynomial())
        convLst = []
        for pair in tupleLst:
            intLst = list(pair)
            intLst[0] = intLst[0] * -1
            convLst.append(tuple(intLst))
        final_tuple = Polynomial(tuple(convLst))
        return final_tuple

    def __add__(self, other):
        added_tuple = self.get_polynomial() + other.get_polynomial()
        poly_tuple = Polynomial(added_tuple)
        return poly_tuple

    def __sub__(self, other):
        lst1 = list(self.get_polynomial())
        lst2 = list(other.__neg__().get_polynomial())
        list_added = lst1 + lst2
        poly_sub_tuple = Polynomial(tuple(list_added))
        return poly_sub_tuple

    def __mul__(self, other):
        lst1 = list(self.get_polynomial())
        lst2 = list(other.get_polynomial())
        lenList1 = len(lst1)
        lenList2 = len(lst2)
        Result = []
        ip = 0
        jp = 0
        iq = 0
        jq = 0
        while (ip < lenList1):
            iq = 0
            while (iq < lenList2):
                jq = 0
                jp = 0
                ResultArray = []
                ResultArray.append(lst1[ip][jp] * lst2[iq][jq])
                jp += 1
                jq += 1
                ResultArray.append(lst1[ip][jp] + lst2[iq][jq])
                Result.append(tuple(ResultArray))
                iq += 1
            ip += 1
        return Polynomial(tuple(Result))

    def __call__(self, x):
        value = 0
        for tuplepair in self.get_polynomial():
            value += tuplepair[0] * x**(tuplepair[1])
        return value

    def simplify(self):
        lenList = len(self.get_polynomial())
        selfList = list(self.get_polynomial())
        for i in range(0, lenList):
            for j in range(0, lenList-i-1):
                if (selfList[j][1] < selfList[j + 1][1]):
                    temp = selfList[j]
                    selfList[j] = selfList[j + 1]
                    selfList[j + 1] = temp
        i = 0
        while (i < len(selfList) - 1):
            if selfList[i][1] == selfList[i + 1][1]:
                firstValue = selfList[i][0] + selfList[i + 1][0]
                secondValue = selfList[i][1]
                selfList[i] = firstValue, secondValue
                selfList.pop(i + 1)
                if selfList[i][0] == 0:
                    selfList.pop(i)
                else:
                    continue
            else:
                i += 1
        if len(selfList) == 0:
            selfList.insert(0, (0, 0))
        self.polynomial = tuple(selfList)

    def __str__(self):
        simple_list = list(self.get_polynomial())
        lenList = len(simple_list)
        poly_string = ""
        for i in range(0, lenList):
            co_eff = simple_list[i][0]
            if co_eff < 0:
                sign = '-'
                co_eff = co_eff * -1
            else:
                sign = '+'
            power = simple_list[i][1]

            if power == 0:
                term = str(co_eff)
            elif power == 1 and co_eff != 1:
                term = str(co_eff) + 'x'
            elif power == 1 and co_eff == 1:
                term = 'x'
            elif power > 1 and co_eff != 1:
                term = str(co_eff)+'x^'+str(power)
            elif power > 1 and co_eff == 1:
                term = 'x^'+str(power)

            if poly_string == "":
                if sign == '-':
                    poly_string = sign + term
                elif sign == '+':
                    poly_string = term
            else:
                poly_string = poly_string + ' ' + sign + ' ' + term
        return poly_string


############################################################
# Section 7: Python Packages
############################################################


def sort_array(list_of_matrices):
    final_array = numpy.array([])
    final2_array = []
    lenList = len(list_of_matrices)
    for i in range(0, lenList):
        new_arr = list_of_matrices[i].reshape(-1)
        final_array = numpy.concatenate((final_array, new_arr))
    final_array_sorted = numpy.sort(final_array)
    final_array = final_array_sorted[::-1]
    for element in final_array:
        final2_array.append(int(element))
    return final2_array


def POS_tag(sentence):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(sentence)
    stopWords = set(stopwords.words('english'))
    filtered_tokens = [w.lower() for w in new_words
                       if not w.lower() in stopWords]
    tagged_words = nltk.pos_tag(filtered_tokens)
    return tagged_words

############################################################
# Section 8: Feedback
############################################################


feedback_question_1 = """I did work on it  over various days. My count is
not accurate,but I may have spent at least 16 hours. """

feedback_question_2 = """I did not stumble on anything but I found second last
problem in polynomial section taking 2 hours or so just for one problem."""

feedback_question_3 = """The assignment brushed off my python skills. So, think
great assignment. And I like almost all of it. I would suggest letting student
know in advance. That this assignment can take several hours."""
