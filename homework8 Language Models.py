import math
import random
import string
import re
import random
from collections import defaultdict

student_name = "Ankita Patel"

############################################################
# Section 1: Markov Models
############################################################


def tokenize(text):
    lst = []
    word = ""
    i = 0
    while i < len(text):
        if text[i] in string.punctuation:
            lst.append(text[i])
            i += 1
        elif text[i].isspace():
            i += 1
            continue
        else:
            while i < len(text) and text[i] not in string.punctuation and \
                    not text[i].isspace():
                word += text[i]
                i += 1
            lst.append(word)
            word = ""
    return lst


def ngrams(n, tokens):
    tokens_copy = tokens[:]
    n_list = []
    if n == 1:
        context = ()
        for token in tokens:
            n_list.append((tuple(context), token))
        n_list.append((context, '<END>'))
        return n_list
    no_starts = n - 1
    for i in range(0, no_starts):
        tokens_copy.insert(0, '<START>')
    for index in range(no_starts, len(tokens_copy)):
        tuple_list = []
        j = index - 1
        for i in range(0, no_starts):
            tuple_list.insert(0, tokens_copy[j])
            j -= 1
        tuple_first = tuple(tuple_list)
        n_list.append((tuple_first, tokens_copy[index]))
    tuple_list = []
    j = len(tokens_copy) - 1
    for i in range(0, no_starts):
        tuple_list.insert(0, tokens_copy[j])
        j -= 1
    n_list.append((tuple(tuple_list), '<END>'))
    return n_list


class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.context_count = defaultdict(float)
        self.contword_count = defaultdict(float)

    def update(self, sentence):
        ord = self.order
        tokens_list = tokenize(sentence)
        n_list = ngrams(ord, tokens_list)
        for (c, w) in n_list:
            self.context_count[c] += 1
            self.contword_count[(c, w)] += 1

    def prob(self, context, token):
        cont_c = self.context_count[context]
        contword_c = self.contword_count[(context, token)]
        return contword_c/cont_c

    def random_token(self, context):
        r = random.random()
        tokens_set = set()
        for (c, w) in self.contword_count.keys():
            if c == context:
                tokens_set.add(w)
        tokens_lst = list(tokens_set)
        tokens_lst.sort()
        prob_t = 0
        if len(tokens_lst) < 1:
            return
        f_token = tokens_lst[0]
        prob_t += self.prob(context, f_token)
        if r < prob_t:
            return f_token
        i = 1
        for i in range(1, len(tokens_lst)):
            prob_t += self.prob(context, tokens_lst[i])
            if r < prob_t:
                return tokens_lst[i]
        return tokens_lst[i]

    def random_text(self, token_count):
        n = self.order
        starting_context = ()
        random_text_list = []
        if n == 1:
            while len(random_text_list) < token_count:
                rand_tok = self.random_token(tuple(starting_context))
                if rand_tok is not None:
                    random_text_list.append(rand_tok)
                if len(random_text_list) == token_count:
                    return ' '.join(random_text_list)
        if n > 1:
            for c in self.context_count.keys():
                if c[-1] == '<START>':
                    starting_context = c
                    break
        context_lst = list(starting_context)
        rand_tok = self.random_token(tuple(context_lst))
        if rand_tok is not None:
            random_text_list.append(rand_tok)
            context_lst.append(rand_tok)
            context_lst.pop(0)
        if len(random_text_list) == token_count:
            return ' '.join(random_text_list)
        if rand_tok == '<END>' or rand_tok is None:
            rand_tok = starting_context
        while len(random_text_list) < token_count:
            rand_tok = self.random_token(tuple(context_lst))
            if rand_tok is not None:
                random_text_list.append(rand_tok)
                context_lst.append(rand_tok)
                context_lst.pop(0)
            if rand_tok == '<END>' or rand_tok is None:
                rand_tok = starting_context
                context_lst = list(starting_context)
        return ' '.join(random_text_list)

    def perplexity(self, sentence):
        n = self.order
        tokens_lst = tokenize(sentence)
        m = len(tokens_lst)
        pr = 1 / (m + 1)
        n_gramlst = ngrams(n, tokens_lst)
        sum = 0
        for (cont, wi) in n_gramlst:
            prob_wi = self.prob(cont, wi)
            inv_prob = 1 / prob_wi
            sum += math.log(inv_prob)
        product = math.exp(sum * pr)
        return product


def create_ngram_model(n, path):
    f = open(path, "r")
    lines = f.readlines()
    ng_model = NgramModel(n)
    for li in lines:
        ng_model.update(li)
    return ng_model


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 12

feedback_question_2 = """
perplexity function.
"""

feedback_question_3 = """
Provide more guidance on perplexity function.
"""
