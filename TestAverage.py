import Hangman
import sys
import traceback


def getAverage():

    TOTAL_TESTS = 1000000
    correct = 0
    try:
        for x in range(TOTAL_TESTS):
            tries = Hangman.Hangman(True)
            if tries != 0:
                correct += 1
            print("\rTests Done: {}/{}".format(x + 1, TOTAL_TESTS), end="")
            sys.stdout.flush()
    except Exception as e:
        print(traceback.format_exc())

    return correct / float(TOTAL_TESTS)


if __name__ == "__main__":

    avg = getAverage()
    print("\nAverage: {:.4f}%".format(avg * 100))
