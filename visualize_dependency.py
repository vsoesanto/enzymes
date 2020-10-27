import spacy
from spacy import displacy


# given a string, visualize the dependency of the string
nlp = spacy.load('en_core_web_sm')
doc = nlp('MAOA preferentially oxidizes serotonin (5-hydroxytryptamine, or 5-HT) and norepinephrine (NE), whereas MAOB preferentially oxidizes beta-phenylethylamine (PEA).')
displacy.serve(doc, style='dep')
