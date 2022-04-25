from nltk.tokenize import word_tokenize
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.probability import FreqDist
import pandas as pd

slangs = {}


def tokenizing(text):
    text_tokens = word_tokenize(text)
    return text_tokens


def remove_slang_in_sentence(sentence: string):
    tokenized = tokenizing(sentence)
    for i, t in enumerate(tokenized):
        if t in slangs.keys():
            sentence = sentence.replace(t, slangs[t])
    return sentence


def case_folding(text):
    # Lowercasing all characters
    text = text.lower()

    # text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text)
    text = re.sub("(\d+)|(/.+/)|(@\w+)|(\S*http\S+)", "", text)

    # Remove punctuations
    text = text.translate(str.maketrans(
        string.punctuation, ' '*len(string.punctuation)))

    # Remove whitespaces
    text = text.rstrip().lstrip()

    # Remove slangs before tokenized (there are some slangs that will be replaced with more than 1 word)
    text = remove_slang_in_sentence(text)
    return tokenizing(text)


def remove_stopwords(tokenized_sentence):
    stopwords_engine = StopWordRemoverFactory()
    stopwords = stopwords_engine.get_stop_words()
    result = []
    for word in tokenized_sentence:
        if word not in stopwords:
            result.append(word)
    return result


def stemming(word_list):
    engine = StemmerFactory()
    stemmer = engine.create_stemmer()
    stemmed_words = [stemmer.stem(word) for word in word_list]
    return stemmed_words


def stemming_sentence(sentence):
    engine = StemmerFactory()
    stemmer = engine.create_stemmer()
    stemmed_sentence = stemmer.stem(sentence)
    return stemmed_sentence


def char_frequency(data, column):
    bin_range = np.arange(0, 260, 10)
    char_freq = data[column].str.len()
    char_freq.hist(bins=bin_range)
    descriptive_analysis(char_freq)
    plt.show()


def word_length(data, column):
    bin_range = np.arange(0, 50)
    word_freq = data[column].str.split().map(lambda x: len(x))
    word_freq.hist(bins=bin_range)
    descriptive_analysis(word_freq)
    plt.show()


def mean_word_length(data, column):
    mean_length = data[column].str.split().apply(lambda x: [len(i) for i in x])
    mean_length = mean_length.map(lambda x: np.mean(x))
    mean_length.hist()
    descriptive_analysis(mean_length)
    plt.show()


def word_frequency(data, column):
    tweet_data = data[column].apply(lambda x: tokenizing(str(x)))
    tweets = [word for tweet in tweet_data for word in tweet]
    fqdist = FreqDist(tweets)
    fqdist.plot(20, cumulative=False)
    plt.show()


def bi_diagram(data, column, count):
    tweet_data = data[column].apply(lambda x: tokenizing(str(x)))
    tweets = [word for tweet in tweet_data for word in tweet]
    result = pd.Series(nltk.ngrams(tweets, 2)).value_counts()[:count]
    print(result)


def descriptive_analysis(series):
    df_series = pd.DataFrame(series)
    print(f"Describe : {df_series.describe()}")
    print(f"Skewness : {df_series.skew()}")
