import xml.etree.ElementTree as et
import os.path
from utilities.summarization import SentenceSegmentation
import re
import logging

# path for loading txt file in the current directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)

logger = logging.getLogger(__name__)


def read_xml_tree(path):
    tree = et.parse(os.path.join(BASE, path), et.XMLParser(encoding='utf-8'))
    return tree


#
# @author: asp
# @date: 15th Nov, 2019
# @function: It updates the sentences' class as summary/non-summary for specific document.
# @input: document_id, updated_sentence_list
#
def do_update_document_by_id(document_id, update_sentence_list):
    tree = read_xml_tree("resource/myanmar_news_xml.xml")  # read xml
    root = tree.getroot()  # get xml root
    # logger.error("Update Sentence" , update_sentence_list)
    for document in root.iter("document"):
        if document.attrib['documentid'] == str(document_id):
            for sentence in document.iter("sentence"):
                if sentence.attrib["sentenceid"] in update_sentence_list:
                    sentence.attrib['class'] = str(1)
                    # logger.error(sentence.attrib['class'])
                else:
                    if sentence.attrib['class'] == "1":
                        sentence.attrib['class'] = str(0)
    tree.write(os.path.join(BASE, "resource/myanmar_news_xml.xml")
               ,encoding="UTF-8",xml_declaration=True)  # encoding is vitally important


def read_document_by_id(documentid):
    tree = read_xml_tree("resource/myanmar_news_xml.xml")  # read xml
    root = tree.getroot()  # get xml root

    document_list = list()
    for document in root:
        if document.attrib['documentid'] == str(documentid):
            sentence_list = list()

            for sentence in document:
                temp_list = list()
                temp_list.append(sentence.attrib['class'])
                temp_list.append(sentence.text)
                sentence_list.append(temp_list)

            dct = {"docid":document.attrib['documentid'], "filename":document.attrib['filename'],
                   "title":document.attrib['title'], "length":document.attrib['length'], "sentencelist":sentence_list}
            document_list.append(dct)
            break

    return document_list


def read_document_title_id():
    tree = read_xml_tree("resource/myanmar_news_xml.xml")
    root = tree.getroot()
    document_list = list()
    for document in root:
        dicttemp = {"title": document.attrib["title"],
                    "id": document.attrib["documentid"]}
        document_list.append(dicttemp)
    return document_list


def do_remove_eos(sentence_list):
    output_list = list()
    for sentence in sentence_list:
        sent = re.sub("။", "", sentence) # remove sentence-end-marker
        sent = sent.strip() # remove spaces
        output_list.append(sent)
    return output_list


def prepare_document(docid, filename, title, sentences):
    sentences = do_remove_eos(sentences) # remove EOS sign
    sentences_dct = {"docid":docid, "filename":filename, "title":title, "sentencelist":sentences}
    return sentences_dct


def check_existence(filename):
    tree = read_xml_tree("myanmar_news_xml.xml")
    root = tree.getroot()
    doc = root.findall("./document/[@filename='"+ filename +"']")
    if doc:
        return True
    return False


def get_latest_documentid():
    tree = read_xml_tree("myanmar_news_xml.xml")
    root = tree.getroot()
    doc = root.findall("document")
    return doc[-1].attrib['documentid']


def write_xml(sentencedct):
    tree = read_xml_tree("myanmar_news_xml.xml")  # read xml
    root = tree.getroot()  # get xml root

    documenttag = et.SubElement(root, "document") # create document node
    documenttag.set("documentid", str(sentencedct['docid']))
    documenttag.set("filename", str(sentencedct['filename']))
    documenttag.set("length", str(len(sentencedct['sentencelist'])))
    documenttag.set("title", str(sentencedct['title']))

    for i, sentence in enumerate(sentencedct['sentencelist']):  # create sentence nodes inside document node
        sentencetag = et.SubElement(documenttag, "sentence")
        sentencetag.set("sentenceid", str(i + 1))
        sentencetag.set("class", "0")
        sentencetag.text = sentence
    tree.write(os.path.join(BASE, "resource/myanmar_news_xml.xml"), encoding="UTF-8", xml_declaration=True)


def clean_text(data):
    cleaned = re.sub("[?၊\\(\\)\\'\\\“\”\‘\’\"\']", " ", data)
    cleaned = re.sub("။", " ။ ", cleaned)
    cleaned = re.sub("\s+", " ", cleaned)
    return cleaned


# save documents into xml directly.
def save_documents(filename, title, sentences):
    if not check_existence(filename):
        title = clean_text(title)
        sentences = clean_text(sentences)
        sentences = SentenceSegmentation.sentence_segmentation(sentences)  # sentence segmentation
        documentid = int(get_latest_documentid()) + 1  # create new document id after getting latest created id
        sentencedct = prepare_document(documentid, filename, title, sentences)  # create document to be saved
        write_xml(sentencedct)  # write xml
