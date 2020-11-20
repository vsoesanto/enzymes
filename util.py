import os
import csv
import gzip
import pickle

import pandas as pd

import spacy
from spacy import displacy
from pysbd.utils import PySBDFactory


def unzip(path):
    '''
    Unzips a given file whose path is given. The file is assumed to be a GNU zip file (.gz)

    :param path: absolute path to a .gz file to be unzipped
    :return: None
    '''
    extension = ".gz"
    file_name = os.path.abspath(path)  # get full path of files
    if file_name.endswith(extension):
        with gzip.open(file_name, mode="rb") as gz_file:
            output = open(file_name[:-3], "wb")
            gz_file_content = gz_file.read()
            output.write(gz_file_content)
            output.close()
            os.remove(file_name)
            print("Unzipped file: " + file_name[:-3])


def get_enzymes(path=None):
    '''
    Reads a file containing enzymes to be searched in abstracts. The path must be a .tsv file
    with a column "symbol" specified.

    :return: a list of enzymes
    '''
    if path is None:
        return pd.read_csv("data/enzyme_symbols/enzymes.tsv", sep="\t")["symbol"].tolist()
    else:
        return pd.read_csv(path, sep="\t")["Approved.symbol"].tolist()


def get_abstracts(path=None, segmented=False):
    '''
    Returns a list containing abstracts from NCBI's database.

    :param path: Optional - path to file containing abstracts. If not provided, data/abstracts is used.
    :param segmented: Boolean value to determine whether the segmented or unsegmented file is desired.
    Default value is False.
    :return: a list of abstracts
    '''
    print("Getting abstracts...")
    abstracts = pd.read_csv("data/abstracts/abstracts.tsv", sep="\t")["abstracts"].tolist()
    if path is not None:
        abstracts = pd.read_csv(path, sep="\t")["abstracts"].tolist()

    if segmented:
        return segment_abstracts(abstracts)
    return abstracts


def segment_abstracts(abstracts):
    '''
    Performs sentence boundary disambiguation (SBD) on existing abstracts.tsv to retrieve individual sentences
    from each abstract. After SBD is applied, a list of sentences is returned.

    :return: A list of sentences post segmentation
    '''
    print("Segmenting abstracts...")
    segmented_abstracts = []
    # abstracts = get_abstracts()
    nlp = spacy.blank("en")
    nlp.add_pipe(PySBDFactory(nlp))
    for i, a in enumerate(abstracts):
        doc = nlp(a)
        # print("abstract = " + a)
        for sent in list(doc.sents):
            # print("\tsent = " + str(sent))
            # df = df.append({"abstracts": str(sent)}, ignore_index=True)
            segmented_abstracts.append(str(sent))
        # print()

    # option for writing data to disk
    # df = pd.DataFrame(segmented_abstracts, columns=["abstracts"])
    # print(df)
    # write(df["abstracts"], name="segmented_abstracts")
    return segmented_abstracts


def pickler(path, name):
    '''
    Parses .xls file of enzyme symbols and their aliases. Stores a serialized mapping object of symbols --> aliases
    as a pickle file. Stores mapping as a .tsv file.

    :param path: path to excel file containing symbols and aliases
    :return: None
    '''
    # e.g. pickler("~/Desktop/data/aliases1.xlsx")
    enzymes_list = pd.read_excel(path)
    aliases = {}

    # initialize approved symbols as keys
    for symbol in enzymes_list["Approved.symbol"]:
        if symbol not in aliases:
            if isinstance(symbol, str):
                aliases[symbol] = []
        # else:
        #     print(symbol + " already exists")

    # add aliases of each enzyme symbol to mapping
    for column_name in enzymes_list:
        if column_name != "Approved.symbol":
            # this column has already been processed above
            for i, item in enumerate(enzymes_list[column_name]):
                # retrieve symbol for this row
                symbol = enzymes_list["Approved.symbol"][i]

                # assert that the elements in cell is a string
                if isinstance(symbol, str) and isinstance(item, str):
                    if column_name == "Alias.names":
                        for x in item.split('", "'):
                            # print("\t after split: " + x)
                            aliases[symbol].append(x.strip('"'))
                    elif column_name == "Alias.symbols" or column_name == "Previous.symbols":
                        for x in item.split(", "):
                            aliases[symbol].append(x)
                    elif column_name == "Approved.name":
                        aliases[symbol].append(item)

    # sanity check
    # for symbol in aliases:
    #     print(symbol + ": " + str(aliases[symbol]))

    # write to .csv
    df = pd.DataFrame.from_dict(aliases, orient="index",)
    df.to_csv(path_or_buf="data/enzyme_symbols/enzymes_" + name + ".csv", header=False, na_rep=None)

    # pickle
    pickle_file = open("data/enzyme_symbols/enzymes_" + name + ".pickle", mode="wb")
    pickle.dump(aliases, pickle_file)
    pickle_file.close()


def visualize_dependency(sentence):
    '''
    Visualize the dependency of given sentence.

    :param sentence: str
    :return: None
    '''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    displacy.serve(doc, style='dep')


if __name__ == "__main__":
    pickler("~/Desktop/data/aliases1.xlsx", name="alias1")
    pickler("~/Desktop/data/aliases2.xlsx", name="alias2")
