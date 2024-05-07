import random
import sys
# from ModDict import modDict


class HangmanInputProcessor:
    MAX_WORDS = 10  # default
    MIN_WORDS = 1
    MAX_STR_LEN = 15  # largest len found in dictionary provided

    def __init__(self, toAvg):
        self.toAvg = toAvg
        self.split_input_list = []
        self.input_choice = 0
        self.preProcessor()

    def requireInput(self):
        while True:
            str_input = input("--> Enter input: ")
            self.split_input_list = str_input.lower().split()

            if len(self.split_input_list) > HangmanInputProcessor.MAX_WORDS:
                print("Maximum string length is 10\n")
                continue
            from ModDict import modDict
            dirty_list = list(
                filter(
                    lambda x: self.binarySearch(x, modDict.get(str(len(x)))) == 0,
                    self.split_input_list,
                )
            )

            if not dirty_list:  # Check for empty list
                print("Entered Input:", " ".join(self.split_input_list))
                break
            else:
                print(
                    "The following words are not found in the dictionary:",
                    ",".join(dirty_list),
                    ". Re-enter input.\n",
                )

    def generate_input(self):
        ret_list = []
        word_num = random.randint(
            HangmanInputProcessor.MIN_WORDS, HangmanInputProcessor.MAX_WORDS
        )

        for _ in range(word_num):
            str_len = str(
                random.randint(
                    HangmanInputProcessor.MIN_WORDS, HangmanInputProcessor.MAX_STR_LEN
                )
            )
            from ModDict import modDict
            while str_len not in modDict:
                str_len = str(
                    random.randint(
                        HangmanInputProcessor.MIN_WORDS,
                        HangmanInputProcessor.MAX_STR_LEN,
                    )
                )
            print(str_len)
            array = modDict.get(str_len)
            chosen_word = array[random.randint(0, len(array) - 1)].lower()
            ret_list.append(chosen_word)
        return ret_list

    def preProcessor(self):
        if self.toAvg:
            self.input_choice = 1
            self.split_input_list = self.generate_input()
            return

        while True:
            print("1 : Generate input for me")
            print("2 : Enter custom input")
            print("Type 'out' to exit program")

            try:
                self.input_choice = input("--> ")

                if self.input_choice == "1":
                    # list of strings
                    self.split_input_list = self.generate_input()
                    print("Generated Input:", " ".join(self.split_input_list))
                    break

                elif self.input_choice == "2":
                    self.requireInput()
                    break
                elif self.input_choice == "out":
                    sys.exit(0)
                else:
                    print("Not a possible option\n")
            except Exception as e:
                print("Error:", str(e))

    def binarySearch(self, word, wordList):
        list_len = len(wordList)
        if not list_len:
            return False

        mid = list_len // 2
        chosenWord = wordList[mid].lower()
        if chosenWord == word:
            return True
        elif chosenWord > word:
            return self.binarySearch(word, wordList[:mid])
        elif chosenWord < word:
            return self.binarySearch(word, wordList[mid + 1 :])
