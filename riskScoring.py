
def setupJson():
    import json

    #intial list of banned words.
    bannedWords = ["hate", "ugly", "stupid", "loser", "bad", "evil"]

    #Dumps the initial list of banned words into a json file.
    with open('wordList.json', 'w') as f:
        json.dump(bannedWords, f)

#function that takes a string input and returns the number of violations held within.
def checkContent(content):
    import json
    import re

    #gets the list of banned words from json
    with open('wordList.json', 'r') as f:
        bannedWords = json.load(f)

    content = str(content).lower()

    #This loops to clear all of the punctuation because that was breaking it.
    for punc in ["!", ".", ",", "?", "/", "'", "#"]:
        content = content.replace(punc, " ")

    words = content.split()

    violationCount = 0

    #Violation counter
    for word in words:
        if word in bannedWords:
            violationCount += 1

    #The comments on everything are not because this was written with AI it's because none of us know how this works
    return violationCount
setupJson()

print(checkContent("I hate how evil you are loser."))

    