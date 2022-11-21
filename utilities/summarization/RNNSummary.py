import os
import tensorflow as tf
from tensorflow import keras
from utilities.summarization import FeatureComputation, SentenceSegmentation
import pandas as pd
import numpy as np


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)


def summarize(title, body):
    sentences, testingdata, ids = compute_features(title, body)
    summary = predict(sentences, testingdata, ids)
    return summary


def compute_features(title, body):
    sentences, _ = SentenceSegmentation.sentence_segmentation(body)
    sentence_length_normalized, sentence_position, ner, number, title_similarity, topic_words, tfisf_list = FeatureComputation.compute_features(title, body)
    ids = np.array([[1,i] for i in range(1, len(sentence_position)+1)])
    df = pd.DataFrame(list(zip(sentence_length_normalized, sentence_position, ner, number, title_similarity, topic_words, tfisf_list)), columns=["sentencelength","sentenceposition","ner","number","titlesimilarity","topicwords","tfisf"])
    df = df.values
    data = df[:, :]
    testingdata = data.reshape(len(data), 1, 7)
    return sentences, testingdata, ids


def predict(sentences, testingdata, ids):
    model = keras.models.load_model(os.path.join(BASE, "summarization/resource/rnn_model.h5"))
    predictions = model.predict(testingdata)
    result = np.concatenate((predictions, ids), axis=1)
    summarylist = list()
    for res in result:
        if np.argmax(res[:2]) == 1:
            sen_id = res[3:4]
            sen_id = int(sen_id)
            # sentence score
            score = testingdata[sen_id-1: sen_id]
            value = score.sum()
            summarylist.append([sen_id, float(value), sentences[sen_id-1]])

    sort_desc(summarylist)
    top4summary = summarylist[:4]
    sorted_summary = sort_desc_by_position(top4summary)
    result = list()
    for sent in sorted_summary:
        # format  (sentence no, score, sentence)
        # temp = str(sent[0]) + ", " + str(sent[1]) + ", "+ str(sent[2])
        temp = str(sent[2].lstrip(" "))
        result.append(temp)
    return "\n\n".join(result)


# sort descending by sentence score
def sort_desc(lst):
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst


# sort descending by sentence position
def sort_desc_by_position(lst):
    lst.sort(key=lambda x: x[0], reverse=False)
    return lst
