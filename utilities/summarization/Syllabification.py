import re
import os.path
import logging
from utilities.summarization import SentenceSegmentation

# path for loading txt file in the current directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # get D://....//extras//src
BASE = os.path.dirname(PROJECT_ROOT)  # get D://....//extras

logger = logging.getLogger(__name__)

def do_syllable_break(text):
    myConsonant = "က-အ၎"
    enChar = "a-zA-Z0-9"
    otherChar = "ဣဤဥဦဧဩဪဿ၌၍၏၊။!-/:-@[-`{-~\s"
    ssSymbol = '္'
    ngaThat = 'င်'
    aThat = '်'

    BreakPattern = re.compile(
        r"((?<!" + ssSymbol + r")[" + myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|[" + otherChar + r"]|[၀-၉]+|([a-zA-Z0-9\.]+))",
        re.UNICODE)  # it fixes the english word including (www.website.com, Word<Space>Word)
    #line = re.sub(r"\s+", "", str(text))

    sentences, _ = SentenceSegmentation.sentence_segmentation(text)
    result = list()
    for sent in sentences:
        line = sent
        line = BreakPattern.sub(r" " + r"\1", str(line))
        lst = line.split()
        lst = do_render_syllable_break(lst)
        result.append(" ".join(lst))

    #print(result)
    return "\n\n".join(result)


def do_render_syllable_break(syllables):
    rendered = list()
    for i in range(len(syllables) - 1):
        if syllables[i] != "" and syllables[i] != "င့်" and syllables[i] != "ည့်":
            if syllables[i + 1] == "င့်" or syllables[i + 1] == "ည့်":
                word = syllables[i] + syllables[i + 1]
                rendered.append(word)
            else:
                rendered.append(syllables[i])
    rendered.append(syllables[-1])  # append the last syllable
    return rendered
