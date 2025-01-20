from utilities.summarization import Syllabification, PhraseSegmentation, SentenceSegmentation
import pandas as pd
import numpy as np
import os.path
import nltk
import re
import logging

# path for loading txt file in the current directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)

logger = logging.getLogger(__name__)  # get an instance of logging

def set_data_structures():
    found_words = set()
    not_found_words = set()
    max_syllable = 6
    return found_words, not_found_words, max_syllable


def load_dictionary():
    # load dictionary
    #dict_words = open(os.path.join(BASE, "original_dictionary.txt"), "r", encoding="utf8").read().splitlines()
    dictionary = pd.read_csv(os.path.join(BASE, "summarization/resource/dictionary.csv"), sep=",", skiprows=1, header=None, encoding="utf-8")
    dct_tag = dict(dictionary.get([0,1]).values.tolist())
    dct_count = dict(dictionary.get([0,2]).values.tolist())
    stop_words = open(os.path.join(BASE, "summarization/resource/stopwords.txt"), "r", encoding="utf8").read().splitlines()
    return dct_tag, dct_count, stop_words


# Search the created N-syllable words in dictionary
def _is_in_dictionary(word, found_words, not_found_words, stop_words, dict_tag, dict_count, phraseboundary):
    found = True
    if word in found_words:
        found = True
    elif word in not_found_words:
        found = False
    elif not (word in dict_tag.keys() or word in stop_words or word in phraseboundary):
        #not_found_words.add(word)
        found = False
    else:
        found_words.add(word)
        found = True
    # logger.info(found_words)
    return found


# Greedy Left to Right Matching with maximum syllable, 6
def left_to_right_matching(_input, found_words, not_found_words, stop_words, dict_tag, dict_count, phraseboundary, _max_syllable):
    length = len(_input)
    position = 0
    result = []
    while length > 0:
        for i in range(min(_max_syllable, length), 0, -1):
            size = position + i
            # Proposed Segmented Words
            word = "".join(_input[position:size])
            #logger.error(word)
            if _is_in_dictionary(word, found_words, not_found_words, stop_words, dict_tag, dict_count, phraseboundary) or i == 1:
                result.append(word)
                position += i
                length -= i
                break
    return result


def do_word_break(data):
    found_words, not_found_words, max_syllable = set_data_structures()
    dict_tag, dict_count, stop_words = load_dictionary()
    phrase_boundary = PhraseSegmentation.load_phrase_boundary()
    max_syllable = 6  # default
    sentences, _ = SentenceSegmentation.sentence_segmentation(data)
    output = list()
    for sent in sentences:
        #formatted_data = re.sub('[?၊\\(\\)]', ' ', sent)  # clean text, remove unwanted symbols
        formatted_data = re.sub(r'\s+', ' ', sent) # replace multiple whitespaces into one
        syllables = Syllabification.do_syllable_break(formatted_data)  # syllable break
        syllable_tokens = nltk.word_tokenize(syllables)  # restore syllables into list
        segmented_text = left_to_right_matching(syllable_tokens, found_words, not_found_words, stop_words,
                                                dict_tag, dict_count, phrase_boundary, max_syllable)  # word break
        temp = "_".join(segmented_text)
        output.append(temp)
        # logger.info(output)
    return output, "\n\n".join(output)


def get_existing_new_words(data):
    dict_words, dict_tags, stop_words = load_dictionary()
    number = "[၀-၉]"
    punctuation = "[?၊။\\(\\)]"
    burmese = "[က-အ၎ဣဤဥဦဧဩဪဿ၌၍၏၊။]"
    existing_words = list()
    new_words = list()
    for sentence in data:
        sentence = sentence.replace('\r', '')
        sentence = sentence.split("_")
        for item in sentence:
            ## ignore the numbers, non-burmese words and EoS marker
            if not re.findall(punctuation, item) and not re.findall(number, item[0]) and re.findall(burmese, item[0]):
                if item in dict_words.keys() or item in stop_words:
                    existing_words.append(item)
                else:
                    if item not in new_words:
                        new_words.append(item)

    return existing_words, new_words


def do_save_new_words(data):
    ## check whether the words already exist in dictionary.
    dict_words, dict_tags, stop_words = load_dictionary()
    proposed_words = data['chk']
    proposed_pos = data['slt']
    words_pos = np.vstack((proposed_words, proposed_pos)).T
    confirmed_words = list()
    for item in words_pos:
        if item[0] not in dict_words and item[0] not in stop_words:
            syllables = Syllabification.do_syllable_break(item[0])
            sylLength = len(syllables.split(" "))
            temp = [item[0], item[1], sylLength]
            confirmed_words.append(temp)

    with open(os.path.join(BASE, "summarization/resource/dictionary.csv"), 'a', newline='', encoding="utf-8") as f:
        #df = pd.DataFrame(data)
        df = pd.DataFrame(confirmed_words, columns=["chk", "tag", "slt"])
        df.to_csv(f, sep=',', header=False, index=False)