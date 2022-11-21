from utilities.summarization import WordSegmentation
import math
from collections import Counter
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)


# compute all features
def compute_features(title, data):
    # sentence break, word break
    segmented_data, _ = WordSegmentation.do_word_break(data)
    try:
        segmented_title, _ = WordSegmentation.do_word_break(title)
    except:
        segmented_title = []
    # Feature 1 (Length)
    sentence_length_normalized = compute_sentence_length_normalized(segmented_data)
    # Feature 2 (Position)
    sentence_position = compute_sentence_position(segmented_data)
    # Feature 3 (NER)
    ner = compute_ner(segmented_data)
    # Feature 4 (Number)
    number = compute_number(segmented_data)
    # Feature 5 (Title)
    title_similarity = compute_title_similarity(segmented_title, segmented_data)
    # Feature 6 (Title)
    topic_words = compute_topic_words(segmented_data)
    # Feature 7 (TFISF)
    tfisf_list = compute_feature_TFISF(segmented_data)
    return sentence_length_normalized, sentence_position, ner, number, title_similarity, topic_words, tfisf_list


# compute tf
def computeTF(wordDict, BoW):
    tfDict = {}
    BoWCount = len(BoW)
    for word, count in wordDict.items():
        tfDict[word] = round(count / float(BoWCount), 3)
    return tfDict


# compute isf
def computeIDF(documents):
    N = len(documents)
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = round(math.log(N / float(val)), 2)
    return idfDict


# compute ifisf
def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


# compute tfisf_feature
def compute_feature_TFISF(segmented_data):
    sentencelist = list()
    tfisf_list = list()
    for sent in segmented_data:
        sentencelist.append(sent)
    # bag of words
    bowlist = list()
    for sentence in sentencelist:
        temp = sentence.split("_")
        bowlist.append(temp)
    bagofwords = []
    for lst in bowlist:
        bagofwords += lst

    # unique words
    uniqueWords = set(bagofwords)

    # dictionary
    dictionarylist = list()
    for lst in bowlist:
        tempDict = dict.fromkeys(uniqueWords, 0)
        for word in lst:
            tempDict[word] += 1
        dictionarylist.append(tempDict)

    # compute TF
    tflist = list()
    for dlst, blst in zip(dictionarylist, bowlist):
        temp = computeTF(dlst, blst)
        tflist.append(temp)

    # compute IDF
    idflist = computeIDF(dictionarylist)

    # compute TFIDF
    tfidflist = list()
    for tf in tflist:
        temp = computeTFIDF(tf, idflist)
        tfidflist.append(temp)

    for tfidf in tfidflist:
        tfisf_list.append(round(sum(tfidf.values()), 3))
    #print(tfisf_list)
    return tfisf_list


# compute topic_words_feature
def compute_topic_words(segmented_data):
    _, _, stop_words = WordSegmentation.load_dictionary()
    vocabulary_list = list()
    topic_words_count = list()
    # collect all words
    for sent in segmented_data:
        temp = sent.split("_")
        vocabulary_list += temp
    # remove stop words
    bow = list()
    for item in vocabulary_list:
        if item not in stop_words and item != "။":
            bow.append(item)
    # explore most common
    result = Counter(bow)
    # topic words
    topic_words = result.most_common(20)
    topic_words = [item[0] for item in topic_words] # it makes (word, count) => (word)
    # count topic words
    for sent in segmented_data:
        count = 0
        if sent:
            temp = sent.split("_")
            for item in temp:
                if item in topic_words:
                    count += 1
            sentencelength = len(temp) - 1
            topic_words_count.append(round(count/sentencelength, 4))
        else:
            #print("0")
            topic_words_count.append(0)
    #print(topic_words_count)
    return topic_words_count


# compute title_similarity_feature
def compute_title_similarity(segmented_title, segmented_data):
    try:
        title_words = segmented_title[0].split("_")
    except:
        title_words = []
    title_similarity = list()
    for sent in segmented_data:
        count = 0
        if sent:
            temp = set(sent.split("_"))
            for word in temp:
                if word in title_words and word != "။":
                    count += 1
        title_similarity.append(count)
    maximum = max(title_similarity)
    #print(title_similarity)
    if len(title_words) != 0:
        title_similarity = [round(count/maximum, 4) for count in title_similarity]
    else:
        title_similarity = [0 for count in title_similarity]
    #print(title_similarity)
    return title_similarity


# compute number_feature
def compute_number(segmented_data):
    number_count = list()
    for sent in segmented_data:
        count = 0
        if sent:
            temp = sent.split("_")
            length = len(temp) - 1
            for word in temp:
                if re.match("[၀-၉]+", word):
                    count += 1
        else:
            length = 1
        number = round(count/length, 4)
        number_count.append(number)
    #print(number_count)
    return number_count


# compute ner_feature
def compute_ner(segmented_data):
    file = open(os.path.join(BASE, "summarization/resource/ners.txt"), "r", encoding="utf-8")
    ners = file.readlines()
    ners = [ner.replace("\n", "") for ner in ners]
    ners_count = list()
    for sent in segmented_data:
        count = 0
        temp = sent.split("_")
        for word in temp:
            if word in ners:
                count += 1
        ners_count.append(count)
    #print(ners_count)
    return ners_count


# compute sentence_position_feature
def compute_sentence_position(segmented_data):
    sentence_position = list()
    total_sentence = len(segmented_data)
    #print(total_sentence)
    for index, sent in enumerate(segmented_data):
        if index <= 4:
            sentence_position.append(1)
        elif index > total_sentence-6:
            # -6 because enumerate starts at 0
            sentence_position.append(1)
        else:
            position = round((total_sentence-index-1)/total_sentence, 4)
            sentence_position.append(position)
    #print(sentence_position)
    return sentence_position


# compute sentence_length_feature
def compute_sentence_length_normalized(segmented_data):
    sentence_length = list()
    for sent in segmented_data:
        sentence_length.append(len(sent.split("_"))-1)

    #print(sentence_length)
    largest = max(sentence_length)
    sentence_length = [round(length/largest, 4) for length in sentence_length]
    #print("Sentence length", sentence_length)
    return sentence_length
