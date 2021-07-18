import spacy


class PartOfSpeech:
    def __init__(self, parts=["NOUN",
                              "PROPN",
                              "TVERB",
                              "ITVERB",
                              "ADP",
                              "ADJ"],
                 cats=[["n"],
                       ["n"],
                       ["nr", "s", "nl"],
                       ["nr","s"],
                       ["sr","nrr","nr","s","nl"],
                       ["n", "nr"]]):
        self.cats = dict()
        for i, part in enumerate(parts):
            self.cats[part] = cats[i]


class QuantumDict:

    def __init__(self, words,qn=2,qs=1,random=True,**params):
        self.nlp = spacy.load('en_core_web_lg')
        self.dictionary = dict()
        self.partsOfSpeech = PartOfSpeech()
        self.qn = qn
        self.qs = qs


    def checkverbtype(self,token):
        indirect_object = False
        direct_object = False
        for item in token.children:
            if (item.dep_ == "iobj" or item.dep_ == "pobj"):
                indirect_object = True
            if (item.dep_ == "dobj" or item.dep_ == "dative"):
                direct_object = True
        if indirect_object and direct_object:
            return 'DTVERB'
        elif direct_object and not indirect_object:
            return 'TVERB'
        elif not direct_object and not indirect_object:
            return 'ITVERB'
        else:
            return 'VERB'


    def addwords(self, mysentence):
        pos=0
        for token in mysentence.sentence:
            wordstring = token.string.strip()
            if wordstring not in self.dictionary.keys():

                self.dictionary[wordstring] = QuantumWord(token)
                self.dictionary[wordstring].setwordproperties(self,mysentence)
                self.dictionary[wordstring].pos=pos
                pos+=1







class QuantumWord:

    def __init__(self,token):
        self.token = token
        self.word = token.string.strip()
        self.lemma = self.token.lemma_

    def setwordproperties(self, mydict, mysentence):

        wordtype = mysentence.nlp(self.token.string)[0].pos_
        if (wordtype == "NOUN") or (wordtype == "PROPN"):
            mydict.dictionary[self.word].nqubits = mydict.qn
        elif wordtype == "ADJ":
            mydict.dictionary[self.word].nqubits = 2 * mydict.qn
        elif wordtype == "ADP":
            mydict.dictionary[self.word].nqubits = 3 * mydict.qn + 2 * mydict.qs
        elif wordtype == "VERB":
            wordtype = mydict.checkverbtype(self.token)
            if wordtype == "TVERB":
                mydict.dictionary[self.word].nqubits = 2 * mydict.qn + mydict.qs
            elif wordtype == "ITVERB":
                mydict.dictionary[self.word].nqubits = mydict.qn + mydict.qs

        mydict.dictionary[self.word].partofspeech = wordtype
        mydict.dictionary[self.word].category = mydict.partsOfSpeech.cats[wordtype]





