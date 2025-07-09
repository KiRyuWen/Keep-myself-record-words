import yaml
import os
import time
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

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        word_list = yaml.safe_load(file)
    return word_list

def create_word_objects(word_list):
    word_objects = []
    builder = WordBuilder()

    for word_data in word_list:
        builder.reset()
        builder.set_word(word_data)

        word_data = word_list[word_data]

        if 'syn' in word_data:
            for synonym in word_data['syn']:
                builder.add_synonym(synonym)

        if 'ant' in word_data:
            for antonym in word_data['ant']:
                builder.add_antonym(antonym)

        if 'def' in word_data:
            builder.set_definition(word_data['def'])

        if 'example' in word_data:
            for example in word_data['example']:
                builder.set_example(example)

        word_objects.append(builder.build())

    return word_objects

def build_word_hash_map(words):
    word_hash_map = {}
    for word in words:

        word_hash_map[word.word] = word
    return word_hash_map

def init():
    # Initialize the word list from the YAML file
    print("Initializing the word list...")
    file_path = 'word_list.yaml'
    word_list = load_word_list(file_path)
    word_list = create_word_objects(word_list)
    all_words = build_word_hash_map(word_list)

    print(f"Loaded {len(all_words)} words from the file.")
    keys = [word.word for word in all_words.values()]
    print("Words loaded:", ", ".join(keys))

    print("Finished loading words")
    return all_words

def main():
    # Initialize the word objects
    words_dict = init()

    # Start the game loop
    game_loop(words_dict)


def search_word(word:str, words_dict):
    return words_dict.get(word, None)

def quiz_syn_or_ant(word: Word, type_of_quiz: str):

    # clear the console
    clear_screen()

    answers = set()
    if type_of_quiz == 'syn':
        answers = word.synonyms
    elif type_of_quiz == 'ant':
        answers = word.antonyms

    if not answers:
        print(f"No {type_of_quiz}onyms available for the word '{word.word}'.")
        time.sleep(1)
        return

    user_typed_list = []
    while True:
        # clear the console
        clear_screen()

        print(f"Quiz for {type_of_quiz}onyms of the word: {word.word}")
        print(f"Definition: {word.definition}")
        print("You have answered the following:")
        if user_typed_list:
            #print the answered synonyms or antonyms
            #each line
            print(f"You have already typed the following {type_of_quiz}onyms:")
            for user_typed in user_typed_list:
                print(f"- {user_typed}")

        user_input = input(f"Type a {type_of_quiz}onym for the word '{word.word}' (or 'quit' to exit): ").strip()
        if user_input.lower() == 'quit':
            print("Exiting the quiz.")
            break
        if user_input in answers:
            print(f"Correct! '{user_input}' is a {type_of_quiz}onym for '{word.word}'.")
            user_typed_list.append(user_input)
            answers.remove(user_input)
        elif user_input in user_typed_list:
            print(f"You have already typed '{user_input}'. Try another {type_of_quiz}onym.")
        else:
            print(f"'{user_input}' is not a {type_of_quiz}onym for '{word.word}'. Try again.")

        if answers.__len__() == 0:
            print(f"Congratulations! You have found all {type_of_quiz}onyms for the word '{word.word}': {', '.join(user_typed_list)}")
            break

def quiz_option(word: Word):
    # clear the console
    clear_screen()
    # Display the word and its definition
    print(f"Quiz for the word: {word.word}")
    print(f"Definition: {word.definition}")
    print("To quiz synonyms, type 'syn'")
    print("To quiz antonyms, type 'ant'")
    print("To exit the quiz, type 'quit'")

    user_input = input("Your choice: ").strip()
    if user_input.lower() == 'syn':
        return 'syn'
    elif user_input.lower() == 'ant':
        return 'ant'
    else:
        return None

def clear_screen():
    # clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

def word_state(word: Word):
    while True:
        clear_screen()
        print(f"Find the word: {word.word}")
        print(f"Definition: {word.definition}")
        print("Enter next options:")
        print("1. To show Synonyms type 'syn'")
        print("2. To show Antonyms type 'ant'")
        print("3. To show Example type 'ex'")
        print("4. To quiz yourself type 'quiz'")
        print("5. To exit type 'quit'")
        user_input = input("Your choice: ").strip()
        if user_input.lower() == 'syn':
            clear_screen()
            print(f"Synonyms: {', '.join(word.synonyms) if word.synonyms else 'No synonyms available.'}")
            input("Press Enter to continue...")  # Wait for user to press Enter
        elif user_input.lower() == 'ant':
            clear_screen()
            print(f"Antonyms: {', '.join(word.antonyms) if word.antonyms else 'No antonyms available.'}")
            input("Press Enter to continue...")  # Wait for user to press Enter
        elif user_input.lower() == 'ex':
            if not word.example:
                print("No examples available for this word.")
            else:
                clear_screen()
                for i, example in enumerate(word.example, start=1):
                    print(f"Example {i}: {example}")
                input("Press Enter to continue...")

        elif user_input.lower() == 'quiz':
            result_type = quiz_option(word)
            if result_type:
                quiz_syn_or_ant(word, result_type)
            else:
                print("Exiting the quiz.")
        elif user_input.lower() == 'quit':
            print("Exiting the word state.")
            break
        else:
            print("Invalid option. Please try again.")


def game_loop(words_dict):

    while True:
        user_input = input("Enter a word to search (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting the game. Goodbye!")
            break

        word = search_word(user_input, words_dict)
        if not word:
            print(f"Word '{user_input}' not found in the dictionary.")
            continue
        else:
            #word state
            word_state(word)


if __name__ == "__main__":
    main()