import re


#
# @author: asp
# @date: 14th Nov, 2019
# @function: It splits the input data into multiple sentences.
# @input: paragraph data
# @return: (1) list
#          (2) String (concatenate list)
#
def sentence_segmentation(data):
    #print(data)
    trimmed_data = re.sub("\s+", " ", data)  # replace multiple spaces into single one
    sentences = trimmed_data.split("။")  # split data into sentences
    sentences = [sent for sent in sentences if sent != '' or len(sent) != 0]  # remove extra null-sentence
    #print("sent", sentences)
    sentences = [sent for sent in sentences if sent != " "]
    sentences = [sent + "။" for sent in sentences]  # append each sentence with the sentence end marker
    return sentences, "\n\n".join(sentences)
