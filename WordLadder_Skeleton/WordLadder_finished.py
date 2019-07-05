"""
Word Ladders

This program's purpose is to find a string of "connected" words which connect one word to another.
For each word, to find the words that can "connect" to it, we can either replace a letter, add a letter, or delete a letter.
Focus on same length words first, then branch off to words of different length.

An example of the string of words:

apple -> ample -> amble -> ramble -> rumble -> bumble -> burble -> burgle -> bungle -> bungee -> bunged -> banged -> ranged -> range -> orange

By Kyle Edwards

In wordladder_input.txt, format your entries by writing the start word, a comma, and then the end word. Press enter for a new pair.

Here is an example:

head,tail
start,end
[start word],[end word]


Any perpetrators caught trying to illegally copy this code will be shot. Survivors will be shot again.
"""

import sys,os
import copy

wordDict = open("dictall.txt","r")
inputFile = open("wordladder_input.txt","r")
outFile = open("wout.txt","w+")
wordList = []
    
#Find all successors
def find_word_successors(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    wordSplit = list(word)
    #Sets are much easier to compare to each other than lists, so we're using them for our list of similar words
    similarWords = set()

    #Replace one of the letters
    for letter in range(len(wordSplit)):
        for replaceLetter in letters:
            current = wordSplit[:]
            current[letter] = replaceLetter
            currentWord = "".join(current)
            if currentWord != word:
                similarWords.add(currentWord)

    #Add a letter to the beginning and the end of the word
    for addLetter in letters:
        currentBeginning = addLetter + word
        currentEnd = word + addLetter
        similarWords.add(currentBeginning)
        similarWords.add(currentEnd)

    #Remove a letter from the beginning and the end of the word
    similarWords.add("".join(wordSplit[1:]))
    similarWords.add("".join(wordSplit[:-1]))

    #We use an intersection between our dictionary of words and the words we found
    return list(wordList.intersection(similarWords))

#This only works when the words are of the same length
def distance_to_goal(current, end):
    cost = len(current)

    smaller = current if len(current) < len(end) else end
    larger = current if len(current) >= len(end) else end

    if len(smaller) != len(larger):
        cost += len(larger) - len(smaller)

        currentSmallest = 999999999
        for offset in range(len(larger)-len(smaller)):
            toBeSmallest = cost
            for currentLetter in range(len(smaller)):
                if smaller[currentLetter] != larger[currentLetter + offset]:
                    toBeSmallest -= 1

            currentSmallest = toBeSmallest if toBeSmallest < currentSmallest else currentSmallest


        cost += currentSmallest

    else:
        for letter in range(len(current)):
            if current[letter] == end[letter]:
                cost -= 1

    return cost

def astar(start, end):
    frontier = [(distance_to_goal(start,end),start,0)]
    seen = {start}
    path = {}
    current = frontier.pop(0)
    while current[1] != end:
        for newWord in find_word_successors(current[1]):
            if newWord not in seen:
                seen = seen | {newWord}
                frontier.append( (distance_to_goal(newWord,end) + current[2] + 1,newWord,current[2] + 1) )
                path[newWord] = current[1]
        frontier.sort()
        if len(frontier) == 0:
            return ['No solution'] #No solution found
        current = frontier.pop(0)

    current = current[1]
    retList = [current]
    while current != start:
        current = path[current]
        retList.insert(0,current)

    return retList
    
if __name__ == "__main__":

    start = "head"
    end = "tail"

    #otherPair = [["head","tail"],["five","four"],["like","flip"],["drive","sleep"]]
    pairs = []
    for word in wordDict.readlines():
        wordList.append(word.split()[0])

    wordList = set(wordList)

    if len(sys.argv) > 2:

        start = str(sys.argv[1])
        end = str(sys.argv[2])

        print(",".join(astar(start,end)))

    else:

        for line in inputFile.readlines():
            pairs.append(line.split("\n")[0].split(","))

        for x in range(len(pairs)):
            """outFile.writelines("=== Breadth First Search ===\n")
            outFile.writelines(" -> ".join(bfs(pairs[x][0],pairs[x][1])))
            outFile.write("\n")
            outFile.write("=== Best First Search ===\n")
            outFile.writelines(" -> ".join(best_first(pairs[x][0],pairs[x][1])))
            outFile.write("\n")"""
            outFile.write("=== A* Search ===\n")
            outFile.writelines(" -> ".join(astar(pairs[x][0],pairs[x][1])))
            outFile.write("\n")
            outFile.write("\n")

        outFile.read()
        wordDict.close()
        inputFile.close()
        outFile.close()
    
