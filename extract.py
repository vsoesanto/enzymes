import spacy
from spacy import displacy
import visualise_spacy_tree
import util
from pysbd.utils import PySBDFactory


nlp = spacy.load('en_core_web_sm')
enzymes = util.get_enzymes()  # get list of enzymes
# sentences = ["ABCG2 is believed to be a functional homodimer that has been proposed to be linked by disulfide bridges.",
#              "Upon mutation of Cys-592 or Cys-608 to alanine (C592A and C608A), ABCG2 migrated as a dimer in SDS-PAGE under non-reducing conditions; however, mutation of Cys-603 to Ala (C603A) caused the transporter to migrate as a single monomeric band."]

sentences = util.get_abstracts(segmented=True)
subj_patterns = ["nsubj", "nsubjpass",  "csubj", "xsubj"]
obj_patterns = ["dobj", "pobj", "iobj"]

relations = []
extracted_from = []
relationships = {}
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
    # flag denotes the number of unique enzymes that exist in the abstract
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



out = open("data/relationships", "w")
# print("RELATIONSHIPS EXTRACTED:")
for i, r in enumerate(relations):
    print(extracted_from[i])
    out.write(extracted_from[i] + "\n")
    print(r)
    out.write(str(r) + "\n\n")

    # extract entity relationships
    strings = ["" for x in range(len(r))]
    noun_chunk_list = [list(item.keys())[0] for item in r]
    for i, item in enumerate(r):  # each element in list is a mapping chunk: (dependency, head)
        tup = list(item.values())[0]
        noun = list(item.keys())[0]
        dependency = tup[0]
        head = tup[1]
        if dependency in subj_patterns:
            strings[i] = head + " " + noun
        elif dependency in obj_patterns:
            # find the head of this object in r's keys
            insert_here = i
            if head in noun_chunk_list:
                insert_here = noun_chunk_list.index(head)
            strings[insert_here] = strings[insert_here] + " --> " + head + " " + noun
        elif dependency == "conj":
            insert_here = i
            for nc in noun_chunk_list:
                if head in nc:
                    insert_here = noun_chunk_list.index(nc)
                    break
            strings[insert_here] = strings[insert_here] + " and " + noun

    print("".join(strings))
    print()





print(str(len(relations)) + " relations")
out.close()



