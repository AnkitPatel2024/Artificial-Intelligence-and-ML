import math
from collections import defaultdict
############################################################
# CIS 521: Homework 9
############################################################

student_name = "Ankita Patel"

############################################################
# Section 1: Perceptrons
############################################################


class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.trainingList = examples
        self.iterations = iterations
        self.feature_wt = defaultdict(float)
        wi = 0
        for i in range(0, iterations):
            for (x, y) in examples:
                y_pred = None
                x_valwi = 0
                for x_i in x.keys():
                    x_val = x.get(x_i)
                    wi = self.feature_wt[x_i]
                    x_valwi += x_val * wi
                if x_valwi > 0:
                    y_pred = True
                else:
                    y_pred = False
                if y_pred != y:
                    if y:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi += x_val
                            self.feature_wt[x_i] = wi
                    else:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi -= x_val
                            self.feature_wt[x_i] = wi

    def predict(self, x):
        keys = list(x.keys())
        wixi = 0
        for i in range(0, len(keys)):
            xi = keys[i]
            x_val = x[xi]
            x_wt = self.feature_wt[xi]
            wixi += x_val * x_wt
        if wixi > 0:
            return True
        return False


class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.classes = set()
        self.features = set()
        for data, cl in examples:
            self.classes.add(cl)
            for f in data.keys():
                self.features.add(f)
        self.ws = {}
        for y in self.classes:
            self.ws[y] = {}
            for f in self.features:
                self.ws[y][f] = 0
        for i in range(0, iterations):
            for (t1, y) in examples:
                data_t = t1
                data_keys_lst = list(data_t.keys())
                wlkxi_max = -math.inf
                lk = None
                for la in self.classes:
                    wlkxi = 0
                    for k in data_keys_lst:
                        x_val = data_t.get(k)
                        wlk = self.ws[la][k]
                        wlkxi += wlk * x_val
                    if wlkxi > wlkxi_max:
                        wlkxi_max = wlkxi
                        lk = la
                y_pred = lk
                if y_pred != y:
                    yfeature_dict = self.ws[y]
                    for f, w in yfeature_dict.items():
                        f_v = data_t.get(f)
                        if f_v is not None:
                            self.ws[y][f] = self.ws[y][f] + f_v
                    yhatfeature_dict = self.ws[y_pred]
                    for f, w in yhatfeature_dict.items():
                        f_v = data_t.get(f)
                        if f_v is not None:
                            self.ws[y_pred][f] -= f_v

    def predict(self, x):
        data_t = x  # dictionary containing xs and vals
        data_keys_lst = list(data_t.keys())
        wlkxi_max = -math.inf
        lk = None
        for la in self.classes:
            wlkxi = 0
            for k in data_keys_lst:
                x_val = data_t.get(k)
                wlk = self.ws[la][k]
                wlkxi += wlk * x_val
            if wlkxi > wlkxi_max:
                wlkxi_max = wlkxi
                lk = la
        y_pred = lk
        return y_pred


############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        self.train_data = []
        self.iterations = 20
        no_features = len(data[0][0])
        features = set()
        for i in range(1, no_features+1):
            features.add(i)
        for tup in data:
            label = tup[1]
            fe = tup[0]
            feature_dict = {}
            i = 1
            for f in fe:
                feature_dict[i] = f
                i += 1
            tup_traindata = (feature_dict, label)
            self.train_data.append(tup_traindata)
        MulticlassPerceptron.__init__(self, self.train_data, self.iterations)

    def classify(self, instance):
        f_dict = {}
        i = 1
        for para in instance:
            f_dict[i] = para
            i += 1
        return MulticlassPerceptron.predict(self, f_dict)


class DigitClassifier(object):

    def __init__(self, data):
        self.train_data = []
        self.iterations = 5
        no_features = len(data[0][0])
        features = set()
        for i in range(1, no_features + 1):
            features.add(i)
        for tup in data:
            label = tup[1]
            fe = tup[0]
            feature_dict = {}
            i = 1
            for f in fe:
                feature_dict[i] = f
                i += 1
            tup_traindata = (feature_dict, label)
            self.train_data.append(tup_traindata)
        self.classes = set()
        self.features = set()
        for data, cl in self.train_data:
            self.classes.add(cl)
            for f in data.keys():
                self.features.add(f)
        self.ws = {}
        for y in self.classes:
            self.ws[y] = {}
            for f in self.features:
                self.ws[y][f] = 0
        for i in range(0, self.iterations):
            for (t1, y) in self.train_data:
                data_t = t1
                data_keys_lst = list(data_t.keys())
                wlkxi_max = -math.inf
                lk = None
                for la in self.classes:
                    wlkxi = 0
                    for k in data_keys_lst:
                        x_val = data_t.get(k)
                        wlk = self.ws[la][k]
                        wlkxi += wlk * x_val
                    if wlkxi > wlkxi_max:
                        wlkxi_max = wlkxi
                        lk = la
                y_pred = lk
                if y_pred != y:
                    yfeature_dict = self.ws[y]
                    for f, w in yfeature_dict.items():
                        f_v = data_t.get(f)
                        if f_v is not None:
                            self.ws[y][f] = self.ws[y][f] + f_v
                    yhatfeature_dict = self.ws[y_pred]
                    for f, w in yhatfeature_dict.items():
                        f_v = data_t.get(f)
                        if f_v is not None:
                            self.ws[y_pred][f] -= f_v

    def classify(self, instance):
        data_t = {}
        i = 1
        for para in instance:
            data_t[i] = para
            i += 1
        data_keys_lst = list(data_t.keys())
        wlkxi_max = -math.inf
        lk = None
        for la in self.classes:
            wlkxi = 0
            for k in data_keys_lst:
                x_val = data_t.get(k)
                wlk = self.ws[la][k]
                wlkxi += wlk * x_val
            if wlkxi > wlkxi_max:
                wlkxi_max = wlkxi
                lk = la
        y_pred = lk
        return y_pred


class BiasClassifier(object):

    def __init__(self, data):
        self.trainingList = []
        self.iterations = 10
        self.bias = -1
        for tup in data:
            label = tup[1]
            fe = tup[0]
            fe += self.bias
            feature_dict = {}
            feature_dict['f'] = fe
            tup_traindata = (feature_dict, label)
            self.trainingList.append(tup_traindata)
        self.feature_wt = defaultdict(float)
        wi = 0
        for i in range(0, self.iterations):
            for (x, y) in self.trainingList:
                y_pred = None
                x_key = list(x.keys())[0]
                x_val = x.get(x_key)
                x_val += self.bias
                wi = self.feature_wt[x_key]
                if x_val * wi > 0:
                    y_pred = True
                else:
                    y_pred = False
                if y_pred == y:
                    self.feature_wt[x_key] = wi
                else:
                    if y:
                        wi += x_val
                        self.feature_wt[x_key] = wi
                    else:
                        wi -= x_val
                        self.feature_wt[x_key] = wi

    def classify(self, instance):
        f_dict = {}
        i = 1
        f_dict['f'] = instance
        keys = list(f_dict.keys())
        wixi = 0
        for i in range(0, len(keys)):
            xi = keys[i]
            x_val = f_dict[xi]
            x_wt = self.feature_wt[xi]
            wixi += x_val * x_wt
        if wixi + self.bias > 0:
            return True
        return False


class MysteryClassifier1(object):

    def __init__(self, data):
        self.train_data = []
        self.iterations = 100
        self.bias = -35
        no_features = len(data[0][0])
        features = set()
        for i in range(1, no_features + 1):
            features.add(i)
        for tup in data:
            label = tup[1]
            fe = tup[0]
            feature_dict = {}
            i = 1
            for f in fe:
                feature_dict[i] = f**2
                i += 1
            tup_traindata = (feature_dict, label)
            self.train_data.append(tup_traindata)
        self.feature_wt = defaultdict(float)
        wi = 0
        for i in range(0, self.iterations):
            for (x, y) in self.train_data:
                y_pred = None
                x_valwi = 0
                for x_i in x.keys():
                    x_val = x.get(x_i)
                    wi = self.feature_wt[x_i]
                    x_valwi += x_val * wi
                if x_valwi + self.bias > 0:
                    y_pred = True
                else:
                    y_pred = False
                if y_pred != y:
                    if y:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi += x_val
                            self.feature_wt[x_i] = wi
                    else:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi -= x_val
                            self.feature_wt[x_i] = wi

    def classify(self, instance):
        f_dict = {}
        i = 1
        for para in instance:
            f_dict[i] = para**2
            i += 1
        keys = list(f_dict.keys())
        wixi = 0
        for i in range(0, len(keys)):
            xi = keys[i]
            x_val = f_dict[xi]
            x_wt = self.feature_wt[xi]
            wixi += x_val * x_wt
        if wixi + self.bias > 0:
            return True
        return False


class MysteryClassifier2(object):

    def __init__(self, data):
        self.train_data = []
        self.iterations = 100
        self.bias = 0
        no_features = len(data[0][0])
        features = set()
        for i in range(1, no_features + 1):
            features.add(i)
        for tup in data:
            label = tup[1]
            fe = tup[0]
            feature_dict = {}
            i = 1
            for f in fe:
                feature_dict[i] = f * f * f
                i += 1
            tup_traindata = (feature_dict, label)
            self.train_data.append(tup_traindata)
        self.feature_wt = defaultdict(float)
        for f in features:
            self.feature_wt[f] = 1
        for i in range(0, self.iterations):
            for (x, y) in self.train_data:
                y_pred = None
                x_valwi = 1
                for x_i in x.keys():
                    x_val = x.get(x_i)
                    wi = self.feature_wt[x_i]
                    x_valwi *= x_val * wi
                if x_valwi + self.bias > 0:
                    y_pred = True
                else:
                    y_pred = False
                if y_pred != y:
                    if y:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi += x_val
                            self.feature_wt[x_i] = wi
                    else:
                        for x_i in x.keys():
                            x_val = x.get(x_i)
                            wi -= x_val
                            self.feature_wt[x_i] = wi

    def classify(self, instance):
        f_dict = {}
        i = 1
        for para in instance:
            f_dict[i] = para * para * para
            i += 1
        keys = list(f_dict.keys())
        wixi = 1
        for i in range(0, len(keys)):
            xi = keys[i]
            x_val = f_dict[xi]
            x_wt = self.feature_wt[xi]
            wixi *= x_val * x_wt
        if wixi + self.bias > 0:
            return True
        return False


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 22

feedback_question_2 = """
understanding of the multiclass perceptron logic.
"""

feedback_question_3 = """
Clearer instructions of multiclass perceptron logic.
"""
