import file_io as io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import random

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

def train():
    global attributes_train, attributes_test, labels_train, labels_test
    dataset = io.read("dataset_analyzed")
    data = []
    for d in dataset:
        d = d.strip('[')
        d = d.strip(']')
        d = d.split(',')
        d.pop(0)
        data.append(d)

    labels = io.read("labels_analyzed")

    dataset, labels = shuffle(dataset,labels)
    attributes_train, attributes_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2, random_state=0)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(attributes_train,labels_train)
    return model

def predict(model, sample):
    prediction = model.predict([sample])
    return prediction

import detectors
model = train()
sample = detectors.domain_analysis("facebook.com")
del sample[0]
result = predict(model, sample)
print(result)