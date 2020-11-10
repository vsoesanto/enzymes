import spacy
import util
import pickle

'''
Author: Vincent Soesanto
Wang Research Lab
Paul G. Allen School of Computer Sciencen and Engineering

Enzyme relationship extractor using dependency parsing
'''

# GLOBAL VARIABLES
nlp = spacy.load('en_core_web_sm')

# define patterns of dependency relations to be captured
subj_patterns = ["nsubj", "nsubjpass",  "csubj", "xsubj"]
obj_patterns = ["dobj", "pobj", "iobj"]


def get_abstracts():
    '''
    Returns abstracts, segmented into sentences
    :return: list of sentences
    '''
    return util.get_abstracts(path="data/abstracts/abstracts.tsv", segmented=True)


def chunk_hunter_v1(sent):
    '''
    Finds two enzyme symbols from the same list (as opposed to two enzymes from two different lists,
    see chunk_hunter_v2) in given spacy.load() object.

    :param sent: spacy.load() object encoding individual sentences in abstract
    :return: list of dependencies in sent
    '''
    s_chunks = []
    enzymes = util.get_enzymes()
    subj_found = False
    obj_found = False
    subj = ""

    for nchunk in sent.noun_chunks:
        # find subject
        if not subj_found:
            if nchunk.root.dep_ in subj_patterns and nchunk.text in enzymes:
                subj_found = True
                subj = nchunk.text

        # find object
        if subj_found:
            if nchunk.root.dep_ in obj_patterns and nchunk.text in enzymes and nchunk.text != subj:
                obj_found = True
                break

    # add to output if subject and object are found
    if subj_found and obj_found:
        for nchunk in sent.noun_chunks:
            s_chunks.append({nchunk.text: (nchunk.root.dep_, nchunk.root.head.text)})

    return s_chunks


def check_aliases(alias, enzyme_file):
    ''''
    Finds alias in the mapping of symbols to aliases

    :param alias: possible alias of an enzyme
    :param enzyme_file: mapping of enzyme symbols to aliases
    :return: Boolean value. True = enzyme alias found; False = enzyme alias not found
    '''
    for ef_sym in enzyme_file:
        if alias in enzyme_file[ef_sym]:
            return True
    return False


def item_hunter(nchunk, enzymes_file, patterns):
    '''
    Hunts for subject in given enzymes_file

    :param nchunk: noun chunk from dependency parsing
    :param enzymes_file: mapping of enzyme symbols to aliases
    :return:
    '''
    if nchunk.root.dep_ in patterns and nchunk.text in enzymes_file:
        return True
    else:
        return check_aliases(nchunk.text, enzymes_file)


def chunk_hunter_v2(sent):
    '''
    Finds two enzyme symbols from two different lists in given spacy.load() object.

    :param sent: spacy.load() object encoding individual sentences in abstract
    :return: list of dependencies in sent
    '''
    s_chunks = []
    enzymes1 = pickle.load(open("data/enzyme_symbols/enzymes_alias1.pickle", "rb"))
    enzymes2 = pickle.load(open("data/enzyme_symbols/enzymes_alias2.pickle", "rb"))
    subj_found = False
    obj_found = False
    subj = ""
    obj = ""
    subj_loc = 0
    obj_loc = 0
    info = []

    for nchunk in sent.noun_chunks:
        # get subject
        if not subj_found:
            subj_found = item_hunter(nchunk, enzymes1, subj_patterns)
            if subj_found:
                subj = nchunk.text
                subj_loc = 1

        if not subj_found:
            subj_found = item_hunter(nchunk, enzymes2, subj_patterns)
            if subj_found:
                subj = nchunk.text
                subj_loc = 2

        # get object
        if subj_found and nchunk.text != subj:
            if subj_loc == 1:
                obj_found = item_hunter(nchunk, enzymes2, obj_patterns)
                if obj_found:
                    obj_loc = 2
                    obj = nchunk.text
            elif subj_loc == 2:
                obj_found = item_hunter(nchunk, enzymes1, obj_patterns)
                if obj_found:
                    obj_loc = 1
                    obj = nchunk.text

        if subj_found and obj_found:
            info.append("\tsubj = " + subj + " from file " + str(subj_loc))
            info.append("\tobj = " + obj + " from file " + str(obj_loc))
            print("\tsubj = " + subj + " from file " + str(subj_loc))
            print("\tobj = " + obj + " from file " + str(obj_loc))
            break

    # add relation
    if subj_found and obj_found:
        for nchunk in sent.noun_chunks:
            s_chunks.append({nchunk.text: (nchunk.root.dep_, nchunk.root.head.text)})

    return s_chunks, info


def main():
    '''
    Performs the computation of the relationship extraction in whole

    :return: None
    '''
    # define data structures for storing information about enzyme relationships
    relations = []  # stores dependency parse of sentences
    original = []  # stores original sentences
    source = []

    abstracts_sents = get_abstracts()

    for i, s in enumerate(abstracts_sents):
        sent = nlp(s)
        # s_chunks = chunk_hunter_v1(sent)
        s_chunks, source_info = chunk_hunter_v2(sent)
        if len(s_chunks) != 0:
            print(s + "\n")
            relations.append(s_chunks)
            original.append(s)
            source.append(source_info)

    write(relations, original, source)


def write(relations, original, source):
    '''
    Writes output of parser to a file

    :param source:
    :param relations: list containing a list of chunks found in a sentence containing enzyme relationship
    :param original: list of original sentences corresponding to the entries in relations
    :return: None
    '''
    out = open("output/relationships_aliases_experiment.txt", "w")
    for i, r in enumerate(relations):
        # each r is a list of dictionary entries [{text: (dep reln, head)}, ...]
        # each item in extracted_from is the original sentence of r
        # print(original[i])
        out.write(original[i] + "\n")
        # print(r)
        out.write(str(r) + "\n")
        for s in source[i]:
            out.write(s + "\n")

    print(str(len(relations)) + " relations")
    out.write("\n\n" + str(len(relations)) + " relations")
    out.close()


# DRIVER
main()
