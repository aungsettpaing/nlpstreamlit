import pandas as pd
from sklearn.cluster import KMeans
from utilities.summarization import WordSegmentation, FeatureComputation, SentenceSegmentation
import os
import re
from collections import Counter
import math

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)

#
# @author: asp
# @date: 5th February, 2020
# @function: Feature computation
# @input:
#

def summarize(title, body):
    sentence_length_normalized, sentence_position, ner, number, title_similarity, topic_words, tfisf_list = FeatureComputation.compute_features(title, body)
    sid = [i for i in range(1, len(ner)+1)]
    df = pd.DataFrame(list(zip(sid, sentence_length_normalized, sentence_position, ner, number, title_similarity, topic_words, tfisf_list)), columns=["sid", "sentencelength","sentenceposition","ner","number","titlesimilarity","topicwords","tfisf"])
    #df['score'] = df.sum(axis=1, skipna=True)
    n_cluster = min(4, len(df))
    kmeanModel = KMeans(n_clusters=n_cluster)
    dataframe = df[:][["sentencelength","sentenceposition","ner","number","titlesimilarity","topicwords","tfisf"]]
    kmeanModel.fit(dataframe)
    clusterlabels = kmeanModel.labels_
    sid = list(df["sid"])
    dataframe['score'] = dataframe.sum(axis=1, skipna=True)
    score = list(dataframe["score"])
    setence_and_cluster_label = zip(sid, clusterlabels, score)
    # retrieve sentences
    sentence_and_id = list()
    original_sentences,_ = SentenceSegmentation.sentence_segmentation(body)
    segmented_data,_ = WordSegmentation.do_word_break(body)
    #print(len(segmented_data), len(original_sentences))
    for index, text in enumerate(original_sentences): # previous one is segmented_data
        temp = [index+1, text]
        sentence_and_id.append(temp)

    cluster_list = list()
    cluster_1 = list()
    cluster_2 = list()
    cluster_3 = list()
    cluster_4 = list()
    for sentid, cluster, score in setence_and_cluster_label:
        temp = list()
        if cluster == 0:
            temp.append(sentid)
            temp.append(sentence_and_id[sentid - 1][1])
            temp.append(score)
            cluster_1.append(temp)
        elif cluster == 1:
            temp.append(sentid)
            temp.append(sentence_and_id[sentid - 1][1])
            temp.append(score)
            cluster_2.append(temp)
        elif cluster == 2:
            temp.append(sentid)
            temp.append(sentence_and_id[sentid - 1][1])
            temp.append(score)
            cluster_3.append(temp)
        elif cluster == 3:
            temp.append(sentid)
            temp.append(sentence_and_id[sentid - 1][1])
            temp.append(score)
            cluster_4.append(temp)

    summarylist = list()
    if len(cluster_1) > 0:
        SortDesc(cluster_1)
        cluster_list.append(cluster_1)
        summarylist.append(cluster_1[0])
    if len(cluster_2) > 0:
        SortDesc(cluster_2)
        cluster_list.append(cluster_2)
        summarylist.append(cluster_2[0])
    if len(cluster_3) > 0:
        SortDesc(cluster_3)
        cluster_list.append(cluster_3)
        summarylist.append(cluster_3[0])
    if len(cluster_4) > 0:
        SortDesc(cluster_4)
        cluster_list.append(cluster_4)
        summarylist.append(cluster_4[0])

    # make summary sorted, list[sent pos, text, score] into string(pos, text, score)
    sortedsummary = Sort(summarylist)
    #sortedsummary = [str(sent[0])+", "+str(sent[1])+", "+str(sent[2]) for sent in sortedsummary]
    sortedsummary = [str(sent[1].lstrip((" "))) for sent in sortedsummary]
    returnsummary = "\n\n".join(sortedsummary)
    # make clusterlist
    return_cluster_list = list()
    for cluster in cluster_list:
        templist = list()
        for sentence in cluster:
            #tempstring = str(sentence[0]) + ", " + str(sentence[1]) + ", " + str(sentence[2])
            tempstring = str(sentence[1].lstrip(" "))
            templist.append(tempstring)
        return_cluster_list.append("\n\n".join(templist))
    return returnsummary, return_cluster_list


def make_line_by_line(cluster_list):
    result = list()
    for cluster in cluster_list:
        temp = list()
        for sentence in cluster:
            string = str(sentence[0]) + "," + str(sentence[1]) + "," + str(sentence[2])
            temp.append(string)
        result.append(temp)
    return result


# sort descending by sentence score
def SortDesc(lst):
    lst.sort(key=lambda x: x[2], reverse=True)
    return lst


# sort ascending by sentence position
def Sort(lst):
    lst.sort(key=lambda x: x[0])
    return lst