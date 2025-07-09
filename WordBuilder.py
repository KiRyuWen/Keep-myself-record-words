from Word import Word

class WordBuilder:

    def __init__(self):
        self.word = None
        self.synonyms = []
        self.antonyms = []
        self.definition = None
        self.example = []

    def set_word(self, word):
        self.word = word
        return self

    def add_synonym(self, synonym):
        self.synonyms.append(synonym)
        return self

    def add_antonym(self, antonym):
        self.antonyms.append(antonym)
        return self

    def set_definition(self, definition):
        self.definition = definition
        return self
    def set_example(self, example):
        self.example.append(example)
        return self

    def build(self):
        return Word(self.word, self.synonyms, self.antonyms, self.definition, self.example)

    def reset(self):
        self.word = None
        self.synonyms = []
        self.antonyms = []
        self.definition = None
        self.example = []
        return self