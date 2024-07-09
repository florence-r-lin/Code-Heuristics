#
# textmodel.py
#
# TextModel project!
#
# Name(s): Florence Lin and Annette Chang
#

import string 
from porter import create_stem
import math

class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence length
        self.repeatedPhrase2 = {}     # For counting phrases length 2
        self.repeatedPhrase3 = {}     # For counting phrases length 3
        self.repeatedPhrase4 = {}     # For counting phrases length 4
        self.repeatedPhrase5 = {}     # For counting phrases length 5

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'Phrases of length 2:\n{str(self.repeatedPhrase2)}\n\n'
        s += f'Phrases of length 3:\n{str(self.repeatedPhrase3)}\n\n'
        s += f'Phrases of length 4:\n{str(self.repeatedPhrase4)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:len(self.text)]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:len(self.cleanedtext)]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.

           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """

        LoW = self.text.split()
        count = 0
        for i in LoW:
            count += 1
            if i[-1] in '.?!':
              if count in self.sentencelengths:
                self.sentencelengths[count] += 1
              else: 
                self.sentencelengths[count] = 1 
              count = 0



    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        s = s.encode("ascii", "ignore")   # Ignores non-ASCII characters
        s = s.decode()       

        result = s.lower()  # converts to lowercase 

        for p in string.punctuation: # gets rid of punctuation
          result = result.replace(p, "")

        return result


    def makeWordLengths(self):
      """creates the dictionary of word-length features using
          self.cleanedtext
      """
      
      LoW = self.cleanedtext.split()
      count = 0
      for i in LoW:
        for x in range(len(i)):
          count += 1
        if count in self.wordlengths:
          self.wordlengths[count] += 1
        else:
          self.wordlengths[count] = 1
        count = 0
    
    def makeWords(self):
      """ creates the dictionary of words using self.cleanedtext
      """
      LoW = self.cleanedtext.split()
      for i in LoW:
        if i in self.words:
          self.words[i] += 1
        else:
          self.words[i] = 1
      

    def makeStems(self):
       """ creates the dictionary of the stems of the words themselves
       """
       LoW = self.cleanedtext.split()
       for i in LoW:
            if create_stem(i) in self.stems:
               self.stems[create_stem(i)] += 1
            else:
               self.stems[create_stem(i)] = 1

    #looking for common phrases in song lyrics (groups of 2, 3, 4)
    def repeatedPhrasesLen2(self):
       """ creates the dictionary for every two word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+2])
        if phrase in self.repeatedPhrase2:
            self.repeatedPhrase2[phrase] += 1
        else:
            self.repeatedPhrase2[phrase] = 1
        i += 1
    
    def repeatedPhrasesLen3(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+3])
        if phrase in self.repeatedPhrase3:
            self.repeatedPhrase3[phrase] += 1
        else:
            self.repeatedPhrase3[phrase] = 1
        i += 1
    
    def repeatedPhrasesLen4(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+4])
        if phrase in self.repeatedPhrase4:
            self.repeatedPhrase4[phrase] += 1
        else:
            self.repeatedPhrase4[phrase] = 1
        i += 1

    def repeatedPhrasesLen5(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+5])
        if phrase in self.repeatedPhrase5:
            self.repeatedPhrase5[phrase] += 1
        else:
            self.repeatedPhrase5[phrase] = 1
        i += 1
       
 
    def normalizeDictionary(self, d):
      """accepts any model dictionary D and returns a normalized version
      """
      nd = {}
      for k in d:
        nd[k] = d[k] / float(sum(d.values()))
      return nd

    def smallestValue(self, nd1, nd2):
      """accepts two model dictionaries and returns the smallest positive 
        value across them both
      """
      minNd1 = 1
      minNd2 = 1
      for k in nd1:
         if nd1[k] <= minNd1:
            minNd1 = nd1[k]
      for k in nd2:
         if nd2[k] <= minNd2:
            minNd2 = nd2[k]

      if minNd1 <= minNd2:
        return minNd1
      else:
        return minNd2
      
    def compareDictionaries(self, d, nd1, nd2):
      """computes the log probabilities that the dictionary d came from
         the distribution of data in the normalized dictionaries nd1 
         and nd2 and returns the value of the log probabilities.
      """
      total_log_prob = 0.0
      epsilon = 0.5*(self.smallestValue(nd1, nd2))
      for k in d:
        if k in nd1:
           total_log_prob += d[k]*math.log(nd1[k])
        else:
           total_log_prob += d[k]*math.log(epsilon)
        lp1 = total_log_prob
      total_log_prob = 0.0
      for k in d:
        if k in nd2:
           total_log_prob += d[k]*math.log(nd2[k])
        else:
           total_log_prob += d[k]*math.log(epsilon)
        lp2 = total_log_prob
      return [lp1, lp2]


    def createAllDictionaries(self):
      """Create out all of self's
         dictionaries in full.
      """
      self.makeSentenceLengths()
      self.makeWords()
      self.makeStems()
      self.makeWordLengths()
      self.repeatedPhrasesLen2()     
      self.repeatedPhrasesLen3()    
      self.repeatedPhrasesLen4()     
      self.repeatedPhrasesLen5()


    def compareTextWithTwoModels(self, model1, model2):
      """runs compareDictionaries for each feature dictionaries in self   
          against corresponding dictionaries
      """

      #create normalized dictionaries for each dictionary
      ndWords1 = self.normalizeDictionary(model1.words)
      ndWords2 = self.normalizeDictionary(model2.words)
      ndWordLengths1 = self.normalizeDictionary(model1.wordlengths)
      ndWordLengths2 = self.normalizeDictionary(model2.wordlengths)
      ndStems1 = self.normalizeDictionary(model1.stems)
      ndStems2 = self.normalizeDictionary(model2.stems)
      ndSentenceLengths1 = self.normalizeDictionary(model1.sentencelengths)
      ndSentenceLengths2 = self.normalizeDictionary(model2.sentencelengths)
      ndRepeatedPhrase2_1 = self.normalizeDictionary(model1.repeatedPhrase2)
      ndRepeatedPhrase2_2 = self.normalizeDictionary(model2.repeatedPhrase2)
      ndRepeatedPhrase3_1 = self.normalizeDictionary(model1.repeatedPhrase3)
      ndRepeatedPhrase3_2 = self.normalizeDictionary(model2.repeatedPhrase3)
      ndRepeatedPhrase4_1 = self.normalizeDictionary(model1.repeatedPhrase4)
      ndRepeatedPhrase4_2 = self.normalizeDictionary(model2.repeatedPhrase4)
      ndRepeatedPhrase5_1 = self.normalizeDictionary(model1.repeatedPhrase5)
      ndRepeatedPhrase5_2 = self.normalizeDictionary(model2.repeatedPhrase5)

      #compute the two log-probability values of each dictionary
      LogProbs1 = self.compareDictionaries(self.words, ndWords1, ndWords2)
      LogProbs2 = self.compareDictionaries(self.wordlengths, ndWordLengths1, ndWordLengths2)
      LogProbs3 = self.compareDictionaries(self.stems, ndStems1, ndStems2)
      LogProbs4 = self.compareDictionaries(self.sentencelengths, ndSentenceLengths1, ndSentenceLengths2)
      LogProbs5 = self.compareDictionaries(self.repeatedPhrase2, ndRepeatedPhrase2_1, ndRepeatedPhrase2_2)
      LogProbs6 = self.compareDictionaries(self.repeatedPhrase3, ndRepeatedPhrase3_1, ndRepeatedPhrase3_2)
      LogProbs7 = self.compareDictionaries(self.repeatedPhrase4, ndRepeatedPhrase4_1, ndRepeatedPhrase4_2)
      LogProbs8 = self.compareDictionaries(self.repeatedPhrase5, ndRepeatedPhrase5_1, ndRepeatedPhrase5_2)
      print("LogProbs1 is", LogProbs1)
      print("LogProbs2 is", LogProbs2)
      print("LogProbs3 is", LogProbs3)
      print("LogProbs4 is", LogProbs4)
      print("LogProbs5 is", LogProbs5)
      print("LogProbs6 is", LogProbs6)
      print("LogProbs7 is", LogProbs7)
      print("LogProbs8 is", LogProbs8)
      print("Overall comparison: \n" )

      #generate comparison chart
      print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
      print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")
      d_name = 'words'
      print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 
      d_name = 'word lengths'
      print(f"     {d_name:>20s}   {LogProbs2[0]:>10.2f}   {LogProbs2[1]:>10.2f} ") 
      d_name = 'word stems'
      print(f"     {d_name:>20s}   {LogProbs3[0]:>10.2f}   {LogProbs3[1]:>10.2f} ")
      d_name = 'sentence lengths'
      print(f"     {d_name:>20s}   {LogProbs4[0]:>10.2f}   {LogProbs4[1]:>10.2f} ")  
      d_name = 'repeated Phrases length 2'
      print(f"     {d_name:>20s}   {LogProbs5[0]:>10.2f}   {LogProbs5[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 3'
      print(f"     {d_name:>20s}   {LogProbs6[0]:>10.2f}   {LogProbs6[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 4'
      print(f"     {d_name:>20s}   {LogProbs7[0]:>10.2f}   {LogProbs7[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 5'
      print(f"     {d_name:>20s}   {LogProbs8[0]:>10.2f}   {LogProbs8[1]:>10.2f} ") 
      
      #compare the two text models
      textMod1 = [LogProbs1[0], LogProbs2[0], LogProbs3[0], LogProbs4[0], LogProbs5[0], LogProbs6[0], LogProbs7[0], LogProbs8[0]]
      textMod2 = [LogProbs1[1], LogProbs2[1], LogProbs3[1], LogProbs4[1], LogProbs5[1], LogProbs6[1], LogProbs7[1], LogProbs8[1]]
      model1Wins = 0
      model2Wins = 0
      print(textMod1)

      for i in range(len(textMod1)):
         if textMod1[i] > textMod2[i]:
            model1Wins += 1
         if textMod1[i] < textMod2[i]:
            model2Wins += 1

      print("--> Text model 1 wins on ", model1Wins, "features")
      print("-->  Text model 2 wins on ", model2Wins, "features")
      if model1Wins > model2Wins:
         print("Text model 1 is the better match!")
      else:
         print("Text model 2 is the better match!")
      

      


# And let's test things out here...
TMintro = TextModel()

# Add a call that puts information into the model
TMintro.addRawText("""This is a small sentence. This isn't a small
sentence, because this sentence contains more than 10 words and a
number! This isn't a question, is it?""")

# Put the above triple-quoted string into a file named test.txt, then run this:
#  TMintro.addFileText("test.txt")   # "comment in" this line, once the file is created

# Print it out
print("TMintro is", TMintro)

print(" +++++++++++ TextModel 1 +++++++++++ ")
TM1 = TextModel()
TM1.addFileText("hungerGames.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ TextModel 2 +++++++++++ ")
TM2 = TextModel()
TM2.addFileText("divergent.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ test +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.addFileText("percyJackson.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)



