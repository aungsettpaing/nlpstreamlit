import os.path
import re
import nltk
from utilities.summarization import WordSegmentation, SentenceSegmentation, Syllabification
import logging

# Get the base project path.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)

logger = logging.getLogger(__name__)

#
# @author: asp
# @date: 14th Nov, 2019
# @function: It loads the phrase boundary data.
# @return: phrase boundary data list
#
def load_phrase_boundary():
    phrase_boundary = open(os.path.join(BASE, "summarization/resource/phraseboundary.txt"), "r",
                           encoding="utf-8-sig").read().splitlines()
    return phrase_boundary

#
# @author: asp
# @date: 14th Nov, 2019
# @function: It breaks into phrases
# @input: paragraph data
# @return: phrases
#
def do_phrase_break(data):
    found_words, not_found_words, max_syllable = WordSegmentation.set_data_structures()  # set data structures
    dict_tag, dict_count, stop_words = WordSegmentation.load_dictionary()  # load dictionary
    phrase_boundary = load_phrase_boundary()  # load phrase boundary
    #logger.error(phrase_boundary)
    max_syllable = 6
    sentences,_ = SentenceSegmentation.sentence_segmentation(data)  # sentence segmentation
    output = list()
    for sent in sentences:
        # logger.error(sent)
        #formatted_data = re.sub('[?၊\\(\\)]', ' ', sent)  # clean text, remove unwanted symbols
        formatted_data = re.sub(r'\s+', ' ', sent)  # replace multiple whitespaces into single one
        syllables = Syllabification.do_syllable_break(formatted_data)  # syllable break
        syllable_tokens = nltk.word_tokenize(syllables)  # restore it into list
        segmented_text = WordSegmentation.left_to_right_matching(syllable_tokens, found_words, not_found_words,
                                                stop_words, dict_tag, dict_count, phrase_boundary, max_syllable)  # word break
        temp = do_make_phrase_segmented_sentences(segmented_text, phrase_boundary)
        output.append(temp)
    return "\n\n".join(output)


def do_make_phrase_segmented_sentences(segmented_text, phrase_boundary):
    temp = ""
    for s in segmented_text:
        if s in phrase_boundary:
            temp += s
            temp += '/ '
        else:
            if s == "။":
                temp += s
                temp += "/"
            elif s == "၊":
                temp += s
                temp += "/ "
            else:
                temp += s+ " "  # add space between words
    return temp