import json
import os.path
from pprint import pprint

modDict = {}
freqDict = {}


def create_mod_dict():
    print("Processing lexicon...")

    with open("dict.txt", "r") as data_file:
        for word in data_file:
            word = word.strip().lower()
            if len(word) in modDict:
                words_of_specific_length = modDict[len(word)]
                words_of_specific_length.append(word)
                modDict[len(word)] = words_of_specific_length
            else:
                words_of_specific_length = [word]
                modDict[len(word)] = words_of_specific_length

    with open("ModDict.json", "w") as outfile:
        json.dump(modDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print("Finished!")


def load_all_dicts():
    global modDict, freqDict

    mod_dict_file = "ModDict.json"
    freq_dict_file = "FreqDict.json"

    if not os.path.isfile(mod_dict_file):
        try:
            create_mod_dict()
            print(modDict)
        except Exception as e:  # Catch any exceptions
            return False

    with open(mod_dict_file, "r") as data_file:
        modDict = json.load(data_file)

    if not os.path.isfile(freq_dict_file):
        try:
            parse_freq_dict()
        except Exception as e:  # Catch any exceptions
            return False

    with open(freq_dict_file, "r") as data_file:
        freqDict = json.load(data_file)

    return True


def parse_freq_dict():
    print("Processing word frequency dictionary...")

    with open("freq.txt", "r") as data_file:
        for line in data_file:
            freq_line = list(map(lambda x: x.strip(), line.lower().split()))
            freqDict[freq_line[0]] = freq_line[1]

    with open("FreqDict.json", "w") as outfile:
        json.dump(freqDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print("Finished!")
