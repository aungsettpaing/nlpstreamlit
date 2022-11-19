def syllable_break(sentence, option):
    print(sentence, option)
    import re
    # myanmar character list
    special = "[ဣဤဧဩဿဪ၌၍၏ဥဦ၎ဿ]"
    consonants = "[က-အ]"

    # remove all spaces
    sentence = re.sub("\s+", "", sentence)

    # change typing order
    sentence = re.sub("့်", "့်", sentence)
    sentence = re.sub("ဥ်", "ဉ်", sentence)

    # check segmentation option
    if option == "Phonetically":
        sentence = re.sub("်္", "်", sentence)
        sentence = re.sub("(?<!်)္", "်", sentence)

    counter = 0
    previous = 0

    result = []

    while counter < len(sentence):
        if re.search(consonants, sentence[counter]):
            if re.search("[္]", sentence[max(0, counter - 1)]) or re.search("[္်]", sentence[min(len(sentence) - 1, counter + 1)]):
                pass
            else:
                if previous != counter:
                    result.append(sentence[previous: counter])
                    previous = counter
        elif re.search(special, sentence[counter]):
            if previous != counter:
                result.append(sentence[previous: counter])
            previous = counter
        counter += 1

    result.append(sentence[previous: counter])
    return " + ".join(result)
