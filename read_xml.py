import xml.etree.ElementTree as ET
import re
import pandas as pd


class XMLReader:

    def __init__(self, path):
        '''
        Initializes the XMLReader object.

        :param path: path to an XML file to read
        '''
        self.abstracts = []
        self.path = path

    def read(self):
        '''
        An XML file contains many papers, and this function will return all abstracts from each paper in the
        XML file.

        :return: None
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

    def get(self, enzyme=None, enzyme_list=None):
        '''
        Retrieve only abstracts that contain enzyme.

        :param enzyme: Optional argument used as key to find in abstracts. If None, enzyme_list must be supplied.
        :param enzyme_list: Optional argument used to iterate over. The enzyme in the list will be matched to tokens in
         abstracts. If None, enzyme must be supplied.
        :return: a list of abstracts containing desired enzyme(s)
        '''
        containing = []
        for a in self.abstracts:
            # print("\treading: " + a)
            if isinstance(a, str):
                for token in a.split():  # split string by whitespace
                    token = self.clean(token)
                    # need to ensure that both "(AOC1)" and "AOC1" contain the enzyme "AOC1"
                    # in this setting, "(AOC1)" also contains the enzyme "A0" which may not be desired
                    if enzyme is not None:
                        if enzyme == token:
                            containing.append(a)  # if there is a match, add abstract to a list immediately
                            break  # and terminate loop that iterates over tokens
                    else:  # use enzyme list
                        for e in enzyme_list:  # iterate over given enzyme list
                            if e == token:  # check if enzyme is contained by the token
                                containing.append(a)  # if there is a match, add abstract to a list immediately
                                print("\tFOUND: " + e)
                                print("\t" + a +"\n")
                                break  # and terminate loop that iterates over tokens
                    break
        self.abstracts = containing

    def clean(self, string):
        '''
        Removes unwanted character(s) from string

        :param string: string from which unwanted characters are removed
        :return: cleaned string
        '''
        string = string.lstrip("(")
        string = string.rstrip(")")
        return string





