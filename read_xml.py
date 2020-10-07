import xml.etree.ElementTree as ET
import os
import pandas as pd


class XMLReader:

    def __init__(self, path):
        self.abstracts = []
        # self.directory = "./pubmed/baseline-2018-sample"
        self.path = path

    def read(self):
        '''
        An XML file contains many papers, and this function will return

        :return:
        '''
        file = self.path
        if file.endswith(".xml"):
            print("Reading file: " + file)

            # generate ElementTree object for current file
            tree = ET.parse(self.path)
            # get the root of this XML file
            root = tree.getroot()
            # get all articles in this XML file
            # by searching for all "PubmedArticle" tags
            # which denote the start of an article
            pubmed_article = root.findall("PubmedArticle")

            # iterate over the articles in this XML file
            for article in pubmed_article:
                # iterate over the nodes in the current article
                for node in article.getiterator():
                    if node.tag == "Abstract":
                        abstract = node[0].text
                        self.abstracts.append(abstract)

    def write(self, curated_list=None):
        '''
        Writes abstracts to a .tsv file.

        :param curated_list: Optional argument. If None, contents of self.abstracts will be used
        :return:
        '''
        # generate a pandas dataframe
        if curated_list is not None:
            data_df = pd.DataFrame(curated_list)
        else:
            data_df = pd.DataFrame(self.abstracts)
        data_df.to_csv("../data/abstracts.tsv", sep="\t", index=False)
        data_df.to_csv("../data/abstracts.tsv", sep="\t", index=False)
        print("Written abstracts to ../data/abstracts.tsv")
        print(data_df)

    def get(self, enzyme=None, enzyme_list=None):
        '''
        Retrieve only abstracts that contain enzyme

        :param enzyme:
        :return:
        '''
        containing = []
        for a in self.abstracts:
            print("\treading: " + a)
            for token in a.split():
                if enzyme is not None:
                    if token == enzyme:
                        containing.append(a)
                        break
                else:
                    if token in enzyme_list:
                        containing.append(a)
                        break
        return containing




