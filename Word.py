from dataclasses import dataclass

@dataclass(frozen=True)
class Word:
    word: str
    synonyms: list
    antonyms: list
    definition: str
    example: list

    # def __init__(self, word, synonyms=None, antonyms=None, definition=None, example=None):
    #     self.word = word
    #     self.synonyms = synonyms if synonyms else []
    #     self.antonyms = antonyms if antonyms else []
    #     self.definition = definition
    #     self.example = example if example else []

    def __hash__(self):
        return hash(self.word)
    def __eq__(self, other):
        if isinstance(other, Word):
            return self.word == other.word
        return False

    def __str__(self):
        return f"Word: {self.word}, Synonyms: {self.synonyms}, Antonyms: {self.antonyms}, Definition: {self.definition}, Example: {self.example}"
