import pandas as pd
import os
import gzip


def unzip(path):
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
    path = "../data/enzymes_list.tsv"
    enzymes_list = pd.read_csv(path, sep="\t")["symbol"].tolist()
    # print(enzymes_list)
    # print(len(enzymes_list))
    return enzymes_list