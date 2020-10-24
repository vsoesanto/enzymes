import pandas as pd
import os
import gzip
import spacy
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


def get_enzymes():
    '''
    Reads a file containing enzymes to be searched in abstracts.

    :return: a list of enzymes
    '''
    return pd.read_csv("data/enzymes_list.tsv", sep="\t")["symbol"].tolist()


def get_abstracts(segmented=False):
    '''
    Returns a list containing abstracts from NCBI's database.

    :param segmented: Boolean value to determine whether the segmented or unsegmented file is desired.
    Default value is False.
    :return: a list of abstracts
    '''
    if segmented:
        return pd.read_csv("data/segmented_abstracts.tsv", sep="\t")["sentences"].tolist()
    else:
        return pd.read_csv("data/abstracts.tsv", sep="\t")["abstracts"].tolist()


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








