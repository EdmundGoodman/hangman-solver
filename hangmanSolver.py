#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#A program to optimally play hangman, by frequency analysis of all possible words
from os import system; system('clear') #If windows, change to: system('cls')
from collections import Counter
from random import choice
import re

#Read in all the allowed words
with open("wordList.txt") as wordFile:
    possibleWords = [word.strip().lower() for word in wordFile]

#Generate the board
wordLen = int(input("How long is the word: "))
word = ["_" for _ in range(wordLen)]

#Remove all possibleWords of the wrong length
possibleWords = [i for i in possibleWords if len(i)==wordLen]

totalPossibleWords = len(possibleWords)
correctLetters, incorrectLetters,  = [], []
guessedLetters, suggestedLetter = [], "e"
count = 0

#While it is not totally guessed
while True:
    #Print the HUD
    system('clear') #If windows, change to: system('cls')
    percentageLeft = str(round((100/totalPossibleWords)*len(possibleWords), 2))+"%"
    print("{} | ? | ? | {}".format(" ".join([str(x)[-1] for x in range(1,wordLen+1)]), percentageLeft))
    print("{} | {} | {}".format(" ".join(word), suggestedLetter, len(possibleWords)))
    if len(possibleWords) < 25:
        print(" ".join(possibleWords))
    else:
        print(" ".join(list(map(lambda _: choice(possibleWords), range(10)))))

    #Read in the guess, where it is/if it's right and validate it
    letter = str(input("Enter a letter to guess: "))
    while letter not in list("etaoinsrhdlucmfywgpbvkxqjz"):
        letter = str(input("Invalid letter; please try again: "))
    guessedLetters.append(letter)

    #Enter and validate the positions of the guessed letter
    positions = input("Enter all of the positions of the letter [1-n]: ").split(" ")
    validPositions = []
    for position in positions:
        #If the position isn't a number, ignore it
        try:
            position = int(position)
        except:
            continue
        #If the position is out of range
        if not 1 <= position <= wordLen:
            continue
        #If the position was previously a space, allow it
        if word[position-1] == "_":
            validPositions.append(position)
    #Remove duplicates from the input
    positions = list(set(validPositions))


    if positions != []:
        #Add the letter to the word at all of the given positions, and to correctLetters
        for position in positions:
            word[position-1] = letter
            correctLetters.append(letter)

        #Narrow down the list of words to only those that fit the found letters
        pattern = re.compile("".join([x if x!="_" else "[a-z]" for x in word]))
        possibleWords = [x for x in possibleWords if bool(pattern.match(x))]

    else:
        #Add the letter to incorrectLetters
        incorrectLetters.append(letter)

        #Narrow down the list of words to those without the letter in
        possibleWords = [x for x in possibleWords if letter not in x]

    #Remove correctLetters from the filteredPossibleWords to stop reguessing letters
    filteredPossibleWords = []
    for nWord in possibleWords:
        for nLetter in correctLetters:
            nWord = nWord.replace(nLetter, "")
        filteredPossibleWords.append(nWord)

    #Suggest the best next letter to guess
    d = dict(Counter("".join(filteredPossibleWords)))

    #If there are no possible words left
    if len(possibleWords) <= 1:
        break

    #The optimum value is the value closest to half of the percentage left (binary search)
    optimumValue = round(len(possibleWords)/2)
    suggestedLetter = min(d, key=lambda i: abs(d[i]-optimumValue))

    #Increment the count variable
    count += 1

system('clear') #If windows, change to: system('cls')
if len(possibleWords) == 1:
    print("Done in {} moves! The word was \"{}\"".format(count, possibleWords[0]))
else:
    print("Invalid word! Check for a spelling mistake or an undisclosed letter")
