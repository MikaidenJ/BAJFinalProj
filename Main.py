#################################################################################################
#                                                                                               #
#                                                                                               #
#                                            Imports                                            #
#                                                                                               #
#                                                                                               #
#################################################################################################

import requests
import pandas as pd
import json

#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Json Word File                                      #
#                                                                                               #
#                                                                                               #
#################################################################################################

#function that starts up a json file
def setupJson():
    

    #intial list of banned words.
    bannedWords = ['annoying', 'stupid', 'terrible', 'worst', 'awful', 'bad', 'corrupt', 'criminal', 'cruel', 'dirty', 'dreadful', 'filthy', 'hideous', 'ugly', 'ignorant']

    #Dumps the initial list of banned words into a json file.
    with open('wordList.json', 'w') as f:
        json.dump(bannedWords, f)

#function that gets the json file and if it does not exist makes one.
def getJson():

    try:
        #Attempts to load a pre-existing file if found.
        with open('wordList.json', 'r') as f:
            bannedWords = json.load(f)
            return bannedWords;

    except FileNotFoundError:
        #Makes a new file if the file is not found.
        setupJson();
        with open('wordList.json', 'r') as f:
            bannedWords = json.load(f)
            return bannedWords;

#adds items to the json file.
def appendJson(bannedWords):

    #Gets the existing words or makes a new file if needed.
    existingWords = getJson()

    #removes any duplicates from the submitted list.
    for word in existingWords:
        if word in bannedWords:
            bannedWords.remove(word)

    #concatenates the lists together.
    bannedWords += existingWords

    #saves the updated list to file.
    with open('wordList.json', 'w') as f:
        json.dump(bannedWords, f)

#removes items from the json file
def removeJson(bannedWords):

    #Gets the existing words or makes a new file if needed.
    existingWords = getJson()
    newWords = list(existingWords)

    #removes the submitted words from the list
    for word in existingWords:
        if word in bannedWords:
            newWords.remove(word)

    #saves the updated list to file.
    with open('wordList.json', 'w') as f:
        json.dump(newWords, f)

#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Content Checker                                     #
#                                                                                               #
#                                                                                               #
#################################################################################################

#Function that takes a string input and returns the number of violations held within.
def checkContent(content):

    #Gets the list of banned words from json
    bannedWords = getJson()

    content = str(content).lower()

    riskAssessmentCount = 0



    #This loops to clear all of the punctuation because that was breaking it.
    for punc in ['!', '.', ',', '?', '/', '\'', '#', '\"']:
        content = content.replace(punc, ' ')

    words = content.split()

    #Violation counter.
    #The assignment states we need to assign more points if multiple words are used in the same line,
    #but I do not see any point in that other than complicating things. We can find an average number of violations that
    #occur in regular posts with no hate and be fine.
    for word in words:
        if word in bannedWords:
            riskAssessmentCount += 1

        #Add more points if an exclamation mark is included.
    if '!' in content and riskAssessmentCount > 0:
        riskAssessmentCount += 2

    return riskAssessmentCount

#Function that replaces naughty bad words with [REDACTED]
def cleanseContent(content):

    #Open the banned words json
    bannedWords = getJson()

    content = str(content)

    #Split the input into a list
    words = content.split()

    
    for i, word in enumerate(words):
        #Turn each word in the list, strip it down to its purest form.
        processedWord = word
        for punc in ['!', '.', ',', '?', '/', '\'', '#', '\"']:
            processedWord = processedWord.replace(punc, '')
        processedWord = str(processedWord).lower()

        #Check if the new word is naughty, if so, redact it
        if processedWord in bannedWords:
            words[i] = '[REDACTED]'

    #join back together the list of words.
    return ' '.join(words)

#################################################################################################
#                                                                                               #
#                                                                                               #
#                                           Load file                                           #
#                                                                                               #
#                                                                                               #
#################################################################################################

def loadFromWeb(url, filename):
    response = requests.get(url)
    response.raise_for_status() #Raise an exception for HTTP errors
    with open(filename, 'w') as f:
        f.write(response.text)

    return loadFromFile(filename)

def loadFromFile(filename):
    #Makes the chat logs a dataframe
    return pd.read_csv(filename)

#################################################################################################
#                                                                                               #
#                                                                                               #
#                                       Main functionality                                      #
#                                                                                               #
#                                                                                               #
#################################################################################################

url = 'https://raw.githubusercontent.com/fpunavarro/cop1009_final_project_chat_logs/f103a66b561dbb087273f9f186d206b0277a0d0d/face_magazine_posts.csv'

local_filename = 'face_magazine_posts.csv'

df = loadFromWeb(url, local_filename)

#Makes it so the user can do multiple options related to the menu
while(True):

  #Printing the menu options
  print('\n\t     MENU     ' + 
        '\t\nSelect the option you want to use\n' +
        '\n1)Load Chat Log\n' +
        '2)Configure Keywords\n' + 
        '3)Scan Log & View Report\n' + 
        '4)Generate Cleaned Log\n' + 
        '5)Load CSV file from web\n' +
        '6)Load CSV file from file\n'
        '7)Exit\n')
  option = int(input('Chose what you want to do: '))


  #If user selcts Option 1, it prints the  dataframe of the chat log
  if(option == 1):
    print(df)
    print('Enter to continue.')
    input()

  #If user selects Option 2, it asks them to add, remove, or view keywords
  elif(option == 2):
    while(True): #Loops until the user wants to stop maniplating the keywords
      keyword_option = input('Would you like to (A)dd, (R)emove, (V)iew keywords or return to (M)enu\n').upper()

      if(keyword_option == 'A'): #Adding words
        banned_words_list = []
        while(True):
          
          ban_word = str(input('Enter a word would you like to censor or type \'EOF\' to stop\n'))

          if(ban_word == 'EOF'): #If EOF is typed, stops adding, if not, keeps adding words
            if (len(banned_words_list) > 0):
                appendJson(banned_words_list)
            break
          else:
            banned_words_list.append(ban_word)

      elif(keyword_option == 'R'): #Removing words
        banned_words_list = []
        while(True):
          word_to_remove = input('Type the word you would like to remove from the keyword list or type \'EOF\' to stop\n')

          if(word_to_remove == 'EOF'): #If EOF is typed, stops removing, if not, keeps removing words
            if (len(banned_words_list) > 0):
                removeJson(banned_words_list)
            break
          else:
             banned_words_list.append(word_to_remove)

      elif(keyword_option == 'V'): #Viewing words
        print(getJson())
        print('Enter to continue.')
        input()

      elif(keyword_option == 'M'): #Returning back to the menu
        break

      else:
        print('Command not recognized. Enter to continue.')
        input()

  #If user selects option 3, it called the functions to scan log and view reports
  elif(option == 3):

    topFlaggedCount = int(input('Input number of highest-ranking results: '))
    topFlagged = {}
    totalLines = 0
    flaggedLines = 0
    totalRisk = 0

    for i, row in df.iterrows():
       risk = checkContent(row['post'])

       if risk > 0:
          flaggedLines += 1
          totalRisk += risk

       totalLines += 1

       if len(topFlagged) < topFlaggedCount:
          topFlagged[i] = risk
       else:

            lowestTopFlaggedIndex = list(topFlagged)[0]

            for index, value in topFlagged.items():
                if value < topFlagged[lowestTopFlaggedIndex]:
                    lowestTopFlaggedIndex = index
                    break

            if risk > topFlagged[lowestTopFlaggedIndex]:
          
                topFlagged.pop(lowestTopFlaggedIndex)
                topFlagged[i] = risk
          

    print('\tResults\t\n' +
          f'Total Lines: {totalLines}\n' +
          f'Flagged Lines: {flaggedLines}\n' +
          f'Flagged percentage: {(flaggedLines / totalLines * 100):.2f}%\n' +
          f'Average risk: {totalRisk / totalLines}')
    print(f'Press enter to see top {topFlaggedCount} highest risk posts')
    input()

    for index, pos in enumerate(topFlagged):
       print(df.loc[[pos]])
       print(f'Risk: {topFlagged[pos]}')

    print('Press enter to continue')
    input()

  #If user selects option 4, it calls the function with the cleaned logs and prints it
  elif(option == 4):

    for i, row in df.iterrows():
       content = str(df.at[i, 'post'])
       df.at[i, 'post'] = cleanseContent(content)


    print('Content cleansed. Enter to continue.')
    input()

    print(df)
    print('Enter to continue.')
    input()

  #If user selects option 5, calls the function to load a file from the web.
  elif(option == 5):
    url = input('Input URL:\n')
    local_filename = input('Input file name:\n')
    loadFromWeb(url, local_filename)
  #If user selects option 6, calls the function to load a file from file.
  elif(option == 6):
    local_filename = input('Input file name:\n')
    loadFromFile(url, local_filename)
  #Ends the program
  elif(option == 7):
    print('Thank you for using our Chat Sentinel! Good-Bye!')
    break

  else:
    print('Command not recognized. Enter to continue.')
    input()



