import pickle as pkl
import numpy as np
from utilities.segmentation import syllable_segmentation
# import tensorflow as tf
# from tensorflow import keras
from tensorflow.python.keras.models import load_model
# from keras.models import load_model
import os


DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def load_files():
    # load vocabs(features) and classes
    vocab = pkl.load(open(os.path.join(DIRECTORY, "resource/vocab.pkl"), "rb"))
    classes = pkl.load(open(os.path.join(DIRECTORY, "resource/classes.pkl"), "rb"))
    # load model
    model = load_model(os.path.join(DIRECTORY, "resource/gender-predict-name.h5"), compile=False)
    return vocab, classes, model


def predict_gender(name):
    # break name into syllables
    name = syllable_segmentation.syllable_break(name, "orthographic")
    name = name.replace(" + ", " ")

    # load model files
    vocab, classes, model = load_files()

    # predict gender
    x = [0] * len(vocab)
    for word in name.split():
        if word in vocab:
            x[vocab.index(word)] += 1
    x = np.array(x)
    x.shape = (1, 369)
    result = model.predict(x)
    result_arg = result.argmax()
    result_prob = "{:.2f}".format(result[0][result_arg] * 100) + "%"

    # return results
    return result_prob, classes[result_arg]
