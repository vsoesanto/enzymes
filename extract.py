import spacy
from spacy import displacy
import util


nlp = spacy.load('en_core_web_sm')
enzymes = util.get_enzymes()  # get list of enzyme_symbols
sentences = util.get_abstracts(segmented=True)  # get segmented abstracts (sentences)

# define patterns of dependency relations to be captured
subj_patterns = ["nsubj", "nsubjpass",  "csubj", "xsubj"]
obj_patterns = ["dobj", "pobj", "iobj"]

# define global data structures for storing information about relationships
relations = []
extracted_from = []
relationships = {}

# maintain a running list of noun chunks for each sentence
for i, s in enumerate(sentences):
    # print(s)
    sent = nlp(s)
    # print pos tag for each token in sentence
    # for token in doc:
    #     print(token.text + " -> " + token.pos_)

    # # print subtrees of each token in sentence
    # for token in doc:
    #     print("token = " + str(token))
    #     for node in token.subtree:
    #         print("\t" + node.text + " -> " + node.pos_)
    #     print()

    # check if noun chunks in sentence contains enzyme; if yes, flag this sentence
    # flag denotes the number of unique enzyme_symbols that exist in the abstract
    flag = 0
    chunk_set = set()
    for nchunk in sent.noun_chunks:
        if (nchunk.root.text in enzymes) and (nchunk.root.text not in chunk_set):
            flag += 1
            chunk_set.add(nchunk.root.text)
        elif (nchunk.root.head.text in enzymes) and (nchunk.root.head.text not in chunk_set):
            flag += 1
            chunk_set.add(nchunk.root.head.text)

        if flag == 2:
            break

    # process noun chunks only if this sentence has been flagged
    if flag == 2:
        s_relations = []
        for nchunk in sent.noun_chunks:
            # print("original chunk: " + str(nchunk.text))
            # print("\troot text: " + str(nchunk.root.text))
            # print("\troot dependency: " + str(nchunk.root.dep_))
            # print("\troot: " + str(nchunk.root.head.text))
            # if nchunk.root.dep_ in noun_patterns or nchunk.:
            s_relations.append({nchunk.text: (nchunk.root.dep_, nchunk.root.head.text)})
            # print()

        relations.append(s_relations)
        extracted_from.append(s)
    # else:
    #     print("Abstract does not contain target enzyme\n")
        # for nchunk in sent.noun_chunks:
        #     print("original chunk: " + str(nchunk.text))
        #     print("\troot text: " + str(nchunk.root.text))
        #     print("\troot dependency: " + str(nchunk.root.dep_))
        #     print("\troot: " + str(nchunk.root.head.text))
        #     print()

    # if i == 1000:
    #     break

# process noun chunks
out = open("output/relationships", "w")
# print("RELATIONSHIPS EXTRACTED:")
for i, r in enumerate(relations):
    # each r is a list of dictionary entries [{text: (dep reln, head)}, ...]
    # each item in extracted_from is the original sentence of r
    print(extracted_from[i])
    out.write(extracted_from[i] + "\n")
    print(r)
    out.write(str(r) + "\n")

    # extract entity relationships
    strings = ["" for x in range(len(r))]  # create a list of empty strings of len(r), num of noun chunks in r
    noun_chunk_list = [list(item.keys())[0] for item in r]  # obtain all of the noun chunks from the r

    for i, item in enumerate(r):  # each element in r is a mapping {text: (dep rln, head)}
        tup = list(item.values())[0]
        noun = list(item.keys())[0]
        dependency = tup[0]
        head = tup[1]

        # generate noun --> noun relationship
        if dependency in subj_patterns:
            strings[i] = noun
        elif dependency in obj_patterns:
            # find the head of this object in r's keys
            insert_here = i
            if head in noun_chunk_list:
                insert_here = noun_chunk_list.index(head)
            strings[insert_here] = strings[insert_here] + " --> " + noun
        elif dependency == "conj":
            insert_here = i
            for nc in noun_chunk_list:
                if head in nc:
                    insert_here = noun_chunk_list.index(nc)
                    break
            strings[insert_here] = strings[insert_here] + " and " + noun

    print(" ".join(strings) + "\n")
    out.write(" ".join(strings) + "\n\n")

print(str(len(relations)) + " relations")
out.write(str(len(relations)) + " relations")
out.close()



