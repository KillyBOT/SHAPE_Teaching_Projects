"""
Word Ladders

This program's purpose is to find a string of "connected" words which connect one word to another.
For each word, to find the words that can "connect" to it, we can either replace a letter, add a letter, or delete a letter.
Focus on same length words first, then branch off to words of different length.

An example of the string of words:

apple -> ample -> amble -> ramble -> rumble -> bumble -> burble -> burgle -> bungle -> bungee -> bunged -> banged -> ranged -> range -> orange

By [First name here][Last name here]

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


#This is the heuristic function. Play around with this however you like!

def distance_to_goal(currentWord, desiredWord):
    
    #TODO: Create a heuristic function to compute the cost from the current word to the end word

    return 0 

#Breadth first search
def bfs(start, end):

    """
    TODO: Use breadth first search to find the shortest path between words. 
    Return a list of the words.
    Optionally, also returns the maximum size of the stack, and the number of words explored.
    """

    return ["No solution"] # No solution found

#Best first search
def best_first(start, end):

    """
    TODO: Use best first search to find a fairly short between words. 
    Return a list of the words.
    Optionally, also returns the maximum size of the stack, and the number of words explored.
    """

    return ["No solution"] # No solution found

#A* search
def astar(start, end):
    
    """
    TODO: Use A* search to find the shortest path between words. 
    Return a list of the words.
    Optionally, also returns the maximum size of the stack, and the number of words explored.
    """

    return ["No solution"] # No solution found


"""
Optionally, here you can make even more search algorithms to implement for this problem.
"""
    
if __name__ == "__main__":

    pairs = []
    for word in wordDict.readlines():
        wordList.append(word.split()[0])

    wordList = set(wordList)

    for line in inputFile.readlines():
        pairs.append(line.split("\n")[0].split(","))

    for x in range(len(pairs)):
        outFile.writelines("=== Breadth First Search ===\n")
        outFile.writelines(" -> ".join(bfs(pairs[x][0],pairs[x][1])))
        outFile.write("\n")
        outFile.writelines("=== Best First Search ===\n")
        outFile.writelines(" -> ".join(best_first(pairs[x][0],pairs[x][1])))
        outFile.write("\n")
        outFile.writelines("=== A* Search ===\n")
        outFile.writelines(" -> ".join(astar(pairs[x][0],pairs[x][1])))
        outFile.write("\n")
        outFile.write("\n")

    wordDict.close()
    inputFile.close()
    outFile.close()
