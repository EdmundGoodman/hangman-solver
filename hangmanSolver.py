#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#A program to optimally play hangman, by frequency analysis of all possible words
from collections import Counter
from random import sample
import re


class HangmanSolver:
    def __init__(self, wordListFileName="wordList.txt"):
        """Initialise all the state variables"""
        self.alphabet = "etaoinsrhdlucmfywgpbvkxqjz"
        self.getWordList(wordListFileName)
        self.word = []
        self.wordLength = 0

        self.guessedLetters = []
        self.suggestedLetter = self.alphabet[0] #Alphabet is ordered by frequency

        self.correctContinueTurn = True

    def getWordList(self, wordListFile):
        """Load in the wordlist file to use"""
        with open(wordListFile) as wordFile:
            self.wordList = [word.strip().lower() for word in wordFile]
        self.initialWordListLength = len(self.wordList)

    def setEmptyWord(self, prompt="How long is the word: ", length=0):
        """Update the data structure given the length of the word"""
        if length == 0:
            self.wordLength = int(input(prompt))
        else:
            self.wordLength = length
        self.word = ["_" for _ in range(self.wordLength)]


    def filterWordLengths(self, length):
        """Get rid of words of the incorrect length"""
        return [i for i in self.wordList if len(i)==length]

    def filterWordPatterns(self):
        """Narrow down the list of words to only those that fit the found letters"""
        pattern = re.compile("".join([
            x if x != "_" else "[^{}]".format("".join(self.guessedLetters))
            for x in self.word]))
        return [x for x in self.wordList if bool(pattern.match(x))]

    def fillInPositions(self, letter, positions):
        """Add the letter to the word at all of the given positions, and to correctLetters"""
        for position in positions:
            self.word[position-1] = letter


    def getBestLetter(self):
        """Suggest the best next letter to guess"""
        letterFrequencies = dict(Counter(
            [x for x in "".join(self.wordList) if x not in self.guessedLetters]
        ))

        if self.correctContinueTurn:
            #The optimum letter is the one which is most likely to be correct
            return max(letterFrequencies, key=lambda i: letterFrequencies[i])
        else:
            #The optimum letter is one which splits the possible words into
            #two even groups (binary search)
            return min(letterFrequencies,
                key=lambda i: abs(letterFrequencies[i] - round(len(self.wordList)/2))
            )


    def getHUD(self, numSuggestedWords=15):
        """Output a 'HUD', which shows data about the solver's state"""
        return "{} | ? | {}%\n{} | {} | {}\n{}".format(
            " ".join([str(x)[-1] for x in range(1, self.wordLength+1)]),
            round(self.getPercentageWordsLeft(), 4),
            " ".join(self.word),
            self.suggestedLetter,
            len(self.wordList),
            sample(self.wordList, min(numSuggestedWords, len(self.wordList)))
        )

    def getLetterInput(self):
        """Take user input on the letter to guess"""
        letter = str(input("Enter a letter to guess: "))
        while letter not in self.alphabet:
            letter = str(input("Invalid letter; please try again: "))
        return letter

    def getCorrectLetterPositions(self):
        """Take user input on the positions of the letters revealed"""
        positions = []
        while 1:
            letter = input("Enter the position of the letter in the word: ")
            try:
                intPosition = int(position)
                if 1 <= intPosition <= self.wordLength and self.word[intPosition-1] == "_":
                    positions.append(intPosition)
            except:
                print("Invalid position")
        return positions

    def getPercentageWordsLeft(self):
        """Calculate the percentage of words left from the initial number"""
        return (100*len(self.wordList)) / self.initialWordListLength


    def benchmark(self, word):
        """Given a word, use the suggested guesses to see how many moves it would take"""
        self.setEmptyWord(length=len(word))
        self.wordList = self.filterWordLengths(self.wordLength)

        count = 0
        while True:
            self.guessedLetters.append(self.suggestedLetter)
            positions = [i+1 for i,c in enumerate(word) if c == self.suggestedLetter]
            if positions != []:
                self.fillInPositions(self.suggestedLetter, positions)

            self.wordList = self.filterWordPatterns()
            if len(self.wordList) == 1:
                print("'{}' found in {} guesses: {}".format(word, count, ", ".join(self.guessedLetters)))
                break
            elif len(self.wordList) == 0:
                print("The word could not be found with the guesses: {}".format(", ".join(self.guessedLetters)))
                break

            self.suggestedLetter = self.getBestLetter()
            count += 1


    def play(self):
        """Provide a UI for the user to play a game with"""
        self.setEmptyWord()
        self.wordList = self.filterWordLengths(self.wordLength)

        count = 0
        while True:
            print(self.getHUD())

            letter = self.getLetterInput()
            self.guessedLetters.append(letter)
            positions = self.getCorrectLetterPositions()

            if positions != []:
                self.fillInPositions(letter, positions)
            self.wordList = self.filterWordPatterns()

            #If there are no possible words left
            if len(self.wordList) == 1:
                print("Done in {} guesses! The word was '{}'".format(count, self.wordList[0]))
                break
            elif len(self.wordList) == 0:
                print("Invalid word! Check for a spelling mistake or an undisclosed letter")
                break

            self.suggestedLetter = self.getBestLetter()

            count += 1
            print("\n\n")


if __name__=="__main__":
    solver = HangmanSolver()
    solver.play()
    #solver.benchmark("hello")
