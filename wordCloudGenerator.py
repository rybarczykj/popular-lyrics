from wordcloud import WordCloud, STOPWORDS
import numpy as numpy
from PIL import Image

class wordCloudGenerator:

    def __init__(self, wordFrequencies):
        self.freqTuples = wordFrequencies

    def generateWordCloudPNG(self):
        freqDict = dict(self.freqTuples)
        wc = WordCloud()
        wc.generate_from_frequencies(freqDict)
        return wc.to_file("wordCloud.png")
