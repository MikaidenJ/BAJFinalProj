
#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Title Card.                                         #
#                                                                                               #
#                                                                                               #
#################################################################################################







#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Content Checker                                     #
#                                                                                               #
#                                                                                               #
#################################################################################################


#function that starts up a json file (temporary for testing the content checker)
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

    #gets the list of banned words from json
    with open('wordList.json', 'r') as f:
        bannedWords = json.load(f)

    content = str(content).lower()

    riskAssessmentCount = 0

    #Add more points if an exclamation mark is included.
    if "!" in content:
        riskAssessmentCount += 2

    #This loops to clear all of the punctuation because that was breaking it.
    for punc in ["!", ".", ",", "?", "/", "'", "#"]:
        content = content.replace(punc, " ")

    words = content.split()

    #Violation counter.
    #The assignment states we need to assign more points if multiple words are used in the same line,
    #but I do not see any point in that other than complicating things. We can find an average number of violations that
    #occur in regular posts with no hate and be fine.
    for word in words:
        if word in bannedWords:
            riskAssessmentCount += 1

    return riskAssessmentCount
setupJson()

#Function that replaces naughty bad words with [REDACTED]
def cleanseContent(content):
    import json

    #Open the banned words json
    with open('wordList.json', 'r') as f:
        bannedWords = json.load(f)

    content = str(content)

    #Split the input into a list
    words = content.split()

    
    for i, word in enumerate(words):
        #Turn each word in the list, strip it down to its purest form.
        processedWord = word
        for punc in ["!", ".", ",", "?", "/", "'", "#"]:
            processedWord = processedWord.replace(punc, "")
        processedWord = str(processedWord).lower()

        #Check if the new word is naughty, if so, redact it
        if processedWord in bannedWords:
            words[i] = "[REDACTED]"

    #join back together the list of words.
    return ' '.join(words)

#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Title Card.                                         #
#                                                                                               #
#                                                                                               #
#################################################################################################



