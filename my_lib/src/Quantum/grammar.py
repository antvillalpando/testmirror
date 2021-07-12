import dictionary
import spacy
import sentence


class GrammarContract:

    def __init__(self,dictionary):
        self.dictionary = dictionary
        self.partsOfSpeech = dictionary.PartOfSpeech()
        self.nlp = spacy.load('en_core_web_lg')

    def findcups(self, spacysentence):







