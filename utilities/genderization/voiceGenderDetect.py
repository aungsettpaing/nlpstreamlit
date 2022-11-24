import pickle as pkl
import numpy as np
# import tensorflow
# from tensorflow import keras
from tensorflow.python.keras.models import load_model
import os
import librosa
from random import randrange
import os
import soundfile as sf
import numpy as np
import pyaudio 
from pydub import AudioSegment, effects


FILE_ROOT = os.path.dirname(os.path.abspath(__file__))
UTILS_ROOT = os.path.dirname(FILE_ROOT)
PROJECT_ROOT = os.path.dirname(UTILS_ROOT)

def record(self):
    # start Recording
    self.audio = pyaudio.PyAudio()
    stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024,
                    input_device_index=0)
    self.frames = []
    for i in range(0, int(44100 / 1024 * 8)):
        data = stream.read(self.chunk)
        self.frames.append(data)
    # stop Recording
    # stream.stop_stream()
    # stream.close()
    # self.audio.terminate()
    # self.save()

    
def save_audio_block(blob):
    # random numbers
    rand1 = randrange(100000)
    rand2 = randrange(100000)

    file_path = "file_" + str(rand1) + "_" + str(rand2) + ".wav"
    # write file
    with open(os.path.join(UTILS_ROOT, "media/audio/"+file_path), 'wb') as f: #bx
        f.write(blob)

    # setWavFormat(file_path)
    return file_path


def setWavFormat(file_path):
    # read audio, manipulate and write with soundfile
    new_audio = AudioSegment.from_file(os.path.join(PROJECT_ROOT, file_path)).set_frame_rate(8000)
    new_audio_signal = np.array(new_audio.get_array_of_samples(),
                                dtype=np.float32) / 32768.0  # scale to between [-1.0, 1.0]

    # the output from down here using the scaled numpy array sounds about half the speed as the first.
    sf.write(os.path.join(PROJECT_ROOT, file_path),
             data=new_audio_signal, samplerate=new_audio.frame_rate, format='wav')


def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    # X, sample_rate = scipy.io.wavfile.read(file_name)
    file_path = os.path.join(PROJECT_ROOT, "nlpapps/media/audio/"+file_name)
    X, sample_rate = librosa.load(file_path, duration=2.0)
    if chroma or contrast:
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
        result = np.hstack((result, mel))
    if contrast:
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
        result = np.hstack((result, contrast))
    if tonnetz:
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
        result = np.hstack((result, tonnetz))
    return result


def predict(features):
    model = load_model(os.path.join(FILE_ROOT, "models/gender-voice/model.h5"), compile=False)
    result = model.predict(features)[0][0]
    return result
