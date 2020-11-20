import tensorflow_hub as hub
import os.path
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import pickle
from nltk.tokenize import word_tokenize


class SentenceEmbedder():

    def __init__(self):
        '''
        Constructs SentenceEmbedder object
        '''
        self.embedder = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def embed(self, string_vec):
        '''
        Embeds given vector of strings into a 512-dim space
        :param string_vec: A vector of strings(s)
        :return: A Tensor object of the string_vec embedding
        '''
        return self.embedder(string_vec)


def get_labeled_data():
    path = "../relationships_aliases_labeled_by_YW.txt"
    assert os.path.isfile(path)

    labeled = {}  # sentence --> label
    with open(path, mode="r") as file:
        sentence = ""
        for line in file:
            line = line.strip()
            if len(line) > 0:
                # print(line)
                if line[0:2] != "[{" and "-->" not in line:
                    labeled[line] = -1
                    sentence = line
                elif "-->" in line:
                    label = line[-1]
                    if label == '0' or label == '1':
                        labeled[sentence] = int(label)

    reverse_labeled = {}  # label --> sentences
    for key, value in labeled.items():
        if value not in reverse_labeled:
            reverse_labeled[value] = []
        reverse_labeled[value].append(key)

    return labeled, reverse_labeled


def get_embedding(string):
    '''
    Returns a vectorized representation of string.

    :param string: A vector of sequence(s) of tokens
    :return: Vectorized representation of string
    '''
    embedder = SentenceEmbedder()
    return embedder.embed(string)


def an_enzyme(symbol):
    '''
    Determines if symbol is an enzyme.

    :param symbol: Token to be examined
    :return: Boolean value
    '''
    if symbol in enzymes1 or symbol in enzymes2:
        print("found:", symbol, " as key")
        return True
    else:
        for key, value in enzymes1.items():
            for word in value:
                if symbol == word:
                    print("found:", symbol, " as value of", key, " in enzyme1")
                    return True

        for key, value in enzymes2.items():
            for word in value:
                if symbol == word:
                    print("found:", symbol, " as value of", key, " in enzyme2")
                    return True

    return False


def censor(string):
    '''
    Replaces an enzyme name with an alphabetical character

    :param string: A sequence of tokens to censor;
                  if the sequence contains an enzyme, that enzyme will be censored
    :return: A censored sequence of tokens
    '''
    idx = 88
    word_list = word_tokenize(string)
    for i, word in enumerate(word_list):
        if an_enzyme(word):
            replacement = chr(idx)
            idx += 1
            word_list[i] = replacement

    print(word_list, "\n")
    return "".join(word_list)


def normalize(vector):
    '''
    Normalizes vector to unit vector

    :param vector: A vector, possibly non-unit vector
    :return: A normalized vector
    '''
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


if __name__ == "__main__":
    enzymes1 = pickle.load(open("data/enzyme_symbols/enzymes_alias1.pickle", "rb"))
    enzymes2 = pickle.load(open("data/enzyme_symbols/enzymes_alias2.pickle", "rb"))

    labeled, reverse_labeled = get_labeled_data()
    # for label in reverse_labeled:
    #     print(label, len(reverse_labeled[label]))

    scores = []
    ones = [sentences for sentences in reverse_labeled[1]]
    zeros = [sentences for sentences in reverse_labeled[0]]

    test1 = get_embedding(["Fred is married to Jane"])
    test2 = get_embedding(["Jane is married to Fred"])
    print(euclidean_distances(test1, test2))


    # censor(ones[0])
    # censor(ones[1])
    # censor(zeros[0])
    # # one_emb1 = get_embedding([ones[0]])
    # # one_emb2 = get_embedding([ones[1]])
    # # normalization
    # one_emb1 = normalize(get_embedding([ones[0]]))
    # one_emb2 = normalize(get_embedding([ones[1]]))
    # score = euclidean_distances(one_emb1, one_emb2)
    # print(score)

    # ones_embs = get_embedding(ones)
    # zeros_embs = get_embedding(zeros)
    # print(ones_embs.shape)
    # # for i in range(len(ones_embs) - 1):
    # #     for j in range(i + 1, len(ones_embs)):
    # #         print("computing similarity: ", i, j)
    # #         vec_i = np.reshape(ones_embs[i], (1, -1))
    # #         vec_j = np.reshape(ones_embs[j], (1, -1))
    # #         score = euclidean_distances(vec_i, vec_j)
    # #         print(score)
    # #         scores.append(score)
    # #         print()
    # #         break
    # #     break
    # # print("avg score = ", np.mean(scores))
    #
    # vec_i = np.reshape(ones_embs[0], (1, -1))
    # vec_j = np.reshape(zeros_embs[0], (1, -1))
    # score = euclidean_distances(vec_i, vec_j)
    # print(score)


