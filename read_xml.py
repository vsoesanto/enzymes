import xml.etree.ElementTree as ET
import os
import pandas as pd

dir = "./pubmed/baseline-2018-sample"
abstracts = []

# iterate over XML files in directory
for file in os.listdir(dir):
    if file.endswith(".xml"):
        print("Reading file: " + file)

        # generate ElementTree object for current file
        tree = ET.parse(dir + "/" + file)
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
                    abstracts.append(abstract)

# generate a pandas dataframe
data_df = pd.DataFrame(abstracts)
data_df.to_csv("abstracts.tsv", sep="\t", index=False)
print(data_df)


