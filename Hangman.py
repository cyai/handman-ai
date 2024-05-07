import Automate
from ModDict import modDict
import ModDict
import sys
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from HangmanInputProcessor import HangmanInputProcessor


class Hangman:
    def __init__(self, get_avg=False):
        self.weighted_list = []
        self.fill_factor_list = []
        self.indices_list = []
        self.to_avg = False
        self.TRIES = 7
        self.res_list = None

        if get_avg:
            self.to_avg = True

        self.setup_graphviz()
        self.rerun_game()

    def setup_graphviz(self):
        # Run the code below whether or not the module is imported or run directly
        self.graphviz = GraphvizOutput()
        self.graphviz.output_file = "flow_graph.png"
        with PyCallGraph(output=self.graphviz):
            is_passed = ModDict.load_all_dicts()
            # print("Loading dictionary...")
            # print(modDict)
            if not is_passed:
                sys.exit("File not found in current directory")

    def rerun_game(self):
        self.inp = HangmanInputProcessor(self.to_avg)
        self.run_game()

    def run_game(self):
        self.res_list = []
        self.TRIES = 7
        Automate.clearAll()
        self.weighted_list = [None] * len(self.inp.split_input_list)

        from ModDict import modDict

        self.weighted_list = list(
            map(
                lambda x: list(modDict.get(str(len(x)))),
                self.inp.split_input_list,
            )
        )
        Automate.calculateLetterWeightOfList(self.weighted_list, True)

        self.fill_factor_list = [0] * len(self.inp.split_input_list)
        self.indices_list = [[]] * len(self.inp.split_input_list)

        self.initialize_state()
        if not self.to_avg:
            self.print_state()
        self.play_game()

    def print_state(self):
        print("".join(self.res_list) + "\n")

    def display_stats(self):
        print("\nTRIES LEFT:", str(self.TRIES) + " out of 7\n")

    def initialize_state(self):
        list_len = sum(map(len, self.inp.split_input_list)) + (
            len(self.inp.split_input_list) - 1
        )
        self.res_list = ["_"] * list_len

        # Insert spaces
        inc = 0
        for x in self.inp.split_input_list:
            inc += len(x)
            if inc < len(self.res_list):
                self.res_list[inc] = " "
                inc += 1

    def play_game(self):
        while self.TRIES != 0:
            ret = self.update_state()  # Retrieve the highest probabilistic character
            if not self.to_avg:
                self.print_state()
            if ret == 1 or (ret == -1 and self.TRIES == 0):
                if not self.to_avg:
                    if ret == -1:
                        print("DEAD -- Game Over")
                    else:
                        print("ALL COMPLETED! SOLVED!")
                    self.display_stats()
                    self.rerun_game()
                break

            # If only our guess was correct
            # if any(self.weighted_list):
            if len(Automate.sortedList) == 0 or (
                Automate.sortedList[-1][0] != 2 and Automate.sortedList[-1][0] != 1.5
            ):
                Automate.calculateLetterWeightOfList(self.weighted_list, False)

    def update_state(self):
        prev_inc = 0
        letter_found = 0

        guess = Automate.popMaxWeightChar()

        if not self.to_avg:
            print("Guess:", guess)

        if guess is not None:
            guess = guess.lower()

            for index, word in enumerate(self.inp.split_input_list):
                if self.fill_factor_list[index] == 1.0:
                    prev_inc += len(word) + 1
                    continue

                idx_list = [x for x, val in enumerate(word) if val == guess]
                # Merge lists
                self.indices_list[index].extend(
                    idx_list
                )  # Use extend for list concatenation

                for x in idx_list:
                    self.res_list[prev_inc + x] = guess

                if len(idx_list) > 0:
                    # Our guess was correct
                    letter_found |= 1

                    temp_weighted_list = []

                    for i in self.weighted_list[index]:
                        idx_matches = 1
                        for idx_num in idx_list:
                            if i[idx_num] == guess:
                                idx_matches &= 1
                            else:
                                idx_matches &= 0
                                break
                        if idx_matches:
                            temp_weighted_list.append(i)

                    self.weighted_list[index] = temp_weighted_list

                    # Add for fill factor of each word
                    self.fill_factor_list[index] = len(
                        self.indices_list[index]
                    ) / float(len(word))

                    # We found the word; now pick the letters in the word as our next guesses
                    if (
                        len(self.weighted_list[index]) == 1
                        and self.fill_factor_list[index] < 1
                    ):
                        Automate.prepForValidFoundSet(
                            set(self.weighted_list[index][0])
                        )

                else:
                    # Character we guessed was not in any of the words
                    letter_found |= 0

                    # Remove characters in the list that don't match
                    self.weighted_list[index] = [
                        i for i in self.weighted_list[index] if guess not in i
                    ]

                prev_inc += len(word) + 1  # Account for space
        else:
            print("no guess")
            if not self.to_avg:
                print("Cannot generate any more guesses.")
                self.rerun_game()

        not_filled_list = [i for i, val in enumerate(self.fill_factor_list) if val < 1]

        # There is no point of picking a word with highest frequency if the
        # word was chosen randomly by generator
        dirty_list = [
            x
            for i, x in enumerate(self.indices_list)
            if len(self.inp.split_input_list[i]) - len(x) <= 2
        ]
        if (
            self.inp.input_choice != "1"
            and len(dirty_list) == 0
            and len(not_filled_list) != 0
        ):
            if len(Automate.sortedList) == 0 or Automate.sortedList[-1][0] != 2:
                # All chars are distinct at this condition, so look for word frequency
                for x in not_filled_list:
                    idx_left = set(range(len(self.inp.split_input_list[x]))) - set(
                        self.indices_list[x]
                    )
                    if len(idx_left) > 0:
                        idx_left = idx_left.pop()
                        max_freq_set = Automate.createWordFreqSortedList(
                            self.weighted_list[x]
                        )
                        Automate.addMostUniqueCharToList(max_freq_set[-1][1][idx_left])

        if len(not_filled_list) == 0:
            return 1

        if letter_found == 0:
            self.TRIES -= 1
            if not self.to_avg:
                self.display_stats()
            return -1

        return 0


if __name__ == "__main__":
    Hangman()
