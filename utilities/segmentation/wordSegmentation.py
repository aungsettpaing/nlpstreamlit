from utilities.segmentation import syllable_segmentation
import os.path
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
    file = open(os.path.join(BASE, "segmentation/resource/burmese-words.txt"), "r", encoding="utf-8")
    dict_words = file.read().split()
    return dict_words


# Search the created N-syllable words in dictionary
def _is_in_dictionary(word, found_words, not_found_words, phraseboundary):
    found = True
    if word in found_words:
        found = True
    elif word in not_found_words:
        found = False
    else:
        found_words.add(word)
        found = True
    logger.info(found_words)
    return found


# Greedy Left to Right Matching with maximum syllable, 6
def left_to_right_matching(_input, dict_words, _max_syllable):
    length = len(_input)
    position = 0
    result = []
    while length > 0:
        for i in range(min(_max_syllable, length), 0, -1):
            size = position + i
            # Proposed Segmented Words
            word = "".join(_input[position:size])
            if word in dict_words or i == 1:
                result.append(word)
                position += i
                length -= i
                break
    return result


def work_break(data):
    found_words, not_found_words, max_syllable = set_data_structures()
    dict_words = load_dictionary()
    max_syllable = 6
    output = list()

    formatted_data = re.sub(r'\s+', ' ', data)

    syllables = syllable_segmentation.syllable_break(formatted_data, "orthographic")
    syllables_list = syllables.split(" + ")

    segmented_text = left_to_right_matching(syllables_list, dict_words, max_syllable)  # word break
    temp = " + ".join(segmented_text)
    output.append(temp)

    return " ".join(output)
