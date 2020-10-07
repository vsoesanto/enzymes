import spacy
import pandas as pd
import textacy

nlp = spacy.load('en_core_web_sm')
data = pd.read_csv("~/Desktop/data/abstracts.tsv", sep="\t").values.tolist()
enzymes = pd.read_csv("~/Desktop/data/enzymes_list.tsv", sep="\t")

# pattern = r'(<NOUN>*<VERB>?<ADV>*<VERB>+<NOUN>*)'

# extract (PROPN+|NOUN+)VERB?OP*VERB+(PROPN+|NOUN+)
pattern = [{"POS": "PROPN", "OP": "+"}, {"POS": "NOUN", "OP": "+"},
           {"POS": "VERB", "OP": "?"}, {"POS": "ADV", "OP": "*"},
           {"POS": "VERB", "OP": "+"},
           {"POS": "PROPN", "OP": "+"}, {"POS": "NOUN", "OP": "+"}]

# pattern = [{"POS": "PROPN", "OP": "+"},
#            {"POS": "VERB", "OP": "?"}, {"POS": "ADV", "OP": "*"},
#            {"POS": "VERB", "OP": "+"},
#            {"POS": "PROPN", "OP": "+"}]

for i, d in enumerate(data):
    # the code block below prints the pos tag of every token in row
    # row = nlp(d)
    # for token in row:
    #     print(token, token.tag_, token.pos_)

    # for e in enzymes:
    #     if e in d:
    #         print("enzyme " + e + " in:\n" + d)
    #         # search for chunks based on pattern
    #         row_doc = textacy.make_spacy_doc(str(d), lang="en_core_web_sm")
    #         verb_phrases = textacy.extract.matches(row_doc, pattern)
    #
    #         print(d)
    #         for vp_chunk in verb_phrases:
    #             print("\t" + vp_chunk.text)

    # search for chunks based on pattern
    row_doc = textacy.make_spacy_doc(str(d), lang="en_core_web_sm")
    verb_phrases = textacy.extract.matches(row_doc, pattern)

    print(d)
    for vp_chunk in verb_phrases:
        print("\t" + vp_chunk.text)
    print()
