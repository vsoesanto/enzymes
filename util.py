import pandas as pd
import os
import gzip
import spacy
from pysbd.utils import PySBDFactory
import re
import pickle


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


def get_abstracts(segmented=False):
    '''
    Returns a list containing abstracts from NCBI's database.

    :param segmented: Boolean value to determine whether the segmented or unsegmented file is desired.
    Default value is False.
    :return: a list of abstracts
    '''
    if segmented:
        return pd.read_csv("data/abstracts/segmented_abstracts.tsv", sep="\t")["sentences"].tolist()
    else:
        return pd.read_csv("data/abstracts/abstracts.tsv", sep="\t")["abstracts"].tolist()


def write(curated_list=None):
    '''
    Writes abstracts to a .tsv file.

    :param curated_list: Contents of curated_list will be used to write to a .tsv file.
    :return:
    '''
    # generate a pandas dataframe
    data_df = pd.DataFrame(curated_list)

    data_df.to_csv(".data/abstracts.tsv", sep="\t", index=False)
    print("Written abstracts to ../data/abstracts.tsv")
    print(data_df)


def segment_abstracts():
    '''
    Performs sentence boundary disambiguation (SBD) on existing abstracts.tsv to retrieve individual sentences
    from each abstract. After SBD is applied, writes sentences to a .tsv file.

    :return: None
    '''
    segmented_abstracts_df = pd.DataFrame(columns=["sentences"])
    abstracts = get_abstracts()
    nlp = spacy.blank("en")
    nlp.add_pipe(PySBDFactory(nlp))
    for i, a in enumerate(abstracts):
        doc = nlp(a)
        for sent in list(doc.sents):
            segmented_abstracts_df = segmented_abstracts_df.append({"sentences": sent}, ignore_index=True)

        if i < 2:
            print(list(doc.sents))

    print(segmented_abstracts_df)
    segmented_abstracts_df.to_csv("data/segmented_abstracts.tsv", sep="\t", index=False)


def convert_to_tsv(path):
    '''
    Parses .xls file of enzyme symbols and their aliases. Stores a serialized mapping object of symbols --> aliases
    as a pickle file. Stores mapping as a .tsv file.

    :param path: path to excel file containing symbols and aliases
    :return: None
    '''
    enzymes_list = pd.read_excel(path)
    aliases = {}

    for symbol in enzymes_list["Approved.symbol"]:
        if symbol not in aliases:
            if isinstance(symbol, str):
                aliases[symbol] = []
        else:
            print(symbol + " already exists")

    for column_name in enzymes_list:
        if column_name != "Approved.symbol":
            # this column has already been processed above
            print(column_name)
            for i, item in enumerate(enzymes_list[column_name]):
                # retrieve symbol for this row
                symbol = enzymes_list["Approved.symbol"][i]

                # assert that the elements in cell is a string
                if isinstance(symbol, str) and isinstance(item, str):
                    if column_name == "Alias.names":
                        for x in item.split('", "'):
                            print("\t after split: " + x)
                            aliases[symbol].append(x.strip('"'))
                    elif column_name == "Alias.symbols" or column_name == "Previous.symbols":
                        for x in item.split(", "):
                            aliases[symbol].append(x)
                    elif column_name == "Approved.name":
                        aliases[symbol].append(item)

    # sanity check
    # for symbol in aliases:
    #     print(symbol + ": " + str(aliases[symbol]))

    # write to .tsv
    df = pd.DataFrame.from_dict(aliases, orient="index")
    df.to_csv("data/enzymes_alias1.tsv", sep="\t", header=False)

    # pickle
    pickle_file = open("data/enzyme_symbols/enzymes_alias1.pickle", mode="wb")
    pickle.dump(aliases, pickle_file)
    pickle_file.close()
    print(df)


if __name__ == "__main__":
    convert_to_tsv("~/Desktop/data/aliases1.xlsx")


