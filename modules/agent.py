from modules import file_io as io
from modules import detectors
import datetime
import warnings
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)



attributes_train = []
attributes_test = []
labels_train = []
labels_test = []

def setdata():
    whitelist = io.parse_domains()
    blacklist = io.parse_blacklist()
    labels_white = []
    labels_black = []
    for i in whitelist:
        labels_white.append(0)
    labels_black = []
    for i in blacklist:
        labels_black.append(1)

    blacklist = blacklist[:len(whitelist)]
    dataset = whitelist + blacklist
    labels = labels_white + labels_black

    dataset, labels = shuffle(dataset,labels)    

    dataset_analyzed = []
    i = 0
    for data in dataset:
        print(str(i) + ". " + str(data))
        i += 1
        result = detectors.domain_analysis(data)
        dataset_analyzed.append(result)
    io.write(dataset_analyzed, "dataset_analyzed")
    io.write(labels, "labels_analyzed")

    return 0

def shuffle(dataset,labels):
    combined = list(zip(dataset,labels))
    random.shuffle(combined)
    dataset[:], labels [:] = zip(*combined)

    z = 0
    g = 0
    print(len(labels))
    for i in labels:
        if (int(i) == 0):
            g += 1
        elif(int(i) == 1):
            z +=1
    print("Zararlı:" + str(z) + ", Güvenli:" + str(g))
    return dataset, labels

def normalize(dataset):
    max = 0
    min = 0
    min = float(dataset[0][0])
    for data in dataset:
        data[0] = float(data[0])
        if (data[0] > max):
            max = data[0]
        elif (data[0] < min):
            min = data[0]

    for data in dataset:
        data[0] = (data[0]-min) / (max-min)
        
    return dataset

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
def train():
    global attributes_train, attributes_test, labels_train, labels_test
    dataset = io.read("dataset_analyzed")
    data = []
    for d in dataset:
        d = d.split(',')
        for x in d:
            x = float(x)
        data.append(d)

    data = normalize(data)

    labels = io.read("labels_analyzed")

    dataset, labels = shuffle(dataset,labels)
    attributes_train, attributes_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2, random_state=0)
    for d in attributes_train:
        del d[1]
    #model = svm.SVC(kernel="poly",gamma="scale")
    #model = KNeighborsClassifier(n_neighbors=1)
    model = DecisionTreeClassifier(random_state=0)

    model.fit(attributes_train,labels_train)
    print("Accuracy: " + str(model.score(attributes_train,labels_train)))
    return model
def save_model(model,name):
    joblib.dump(model, name + ".pkl") 

def load_model(name):
    try:
        return joblib.load(name + ".pkl")
    except Exception as e:
        return None

def predict(model, sample):
    print(sample)
    prediction = model.predict(sample)
    return prediction


