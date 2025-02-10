# imports
import pandas as pd
from csv import reader
from itertools import permutations
from itertools import combinations
import ipyplot# We should add some filtering to the clue words so that commas and other punctuation does not impact our program
def filterSentence(sentence):
    """input is a user defined sentence, this is filtered 
    by taking out all punctuation leaving just characters"""
    filterWords = [",", ".", "!", "?"]

    for word in filterWords:
        sentence = sentence.replace(word, "")
    
    return sentence
# This is a initial list of songs, just the top 100 songs from each year from 1964
# We are using pandas to grab the CSV data into a form that we can work with
songs_url = 'https://raw.githubusercontent.com/walkerkq/musiclyrics/master/billboard_lyrics_1964-2015.csv'
songs = pd.read_csv(songs_url, encoding="ISO-8859-1")
# We also keep track of the artist name in case we want to use it later for our output
# Creating two lists to hold the songs and the artist of that same song
songList = []
artistList = []
for song in songs['Song']:
    songList.append(song)

for artist in songs["Artist"]:
    artistList.append(artist)
songDict = {}
# We are making a dictionary of the songs so the search time is faster. Hash tables are faster to search through than lists
# We could use the lists too, but if we want to incorperate the artist name in anyway we can easily access the info with the dictionary
for i in range(len(songList)):
    songDict[songList[i]] = artistList[i]
# Just a simple funciton that returns True or False weather or not the song is in our song list
def inDict(sentence):
    if sentence in songDict:
        return True
    else:
        return False
def getIndexWord(sentenceList, sentence):

    word = sentence.split()[-1]

    return sentenceList.index(word)
# This method will look for all the possible matches greedy but on large inputs it will not run fast enough 
# For longer sentence inputs, we are going to do another matching of sentences 
def songSentence(sentence):
    sentence = filterSentence(sentence)
    res = []
    
    #splitting words in sentence into a list
    sentenceList = sentence.split()

    start = 0
    end = len(sentenceList)
    track = 0 

    if len(sentenceList) == 1: 
        if inDict(sentenceList[0]): 
            res.append(sentenceList[0])
            return res 
        else: 
            print("No songs found")
            return []

    b = True
    while b:
        if len(sentenceList[start:end]) == 1 and track != len(sentenceList): 
            start = track + 1 
            end = len(sentenceList)
            track += 1 
        
        tempSentence = " ".join(sentenceList[start:end])
        # print(tempSentence)

        if inDict(tempSentence):
            res.append(tempSentence)
            start = end
            end = len(sentenceList)
            index = getIndexWord(sentenceList, res[-1]) + 1 
            if index < end: 
                start = index 
                track = index
        else:
            end -= 1

        if start == end: 
            b = False 

    return res
d = songSentence("i like it when you buy me this diamond ring")
# This is an even greedier method for matching the songs
# for large inputs, we should use this funciton
# The way it works is that we only look for matches that are a given range of words long 
# Once we match, we say that it is the best match and move on thinking that it is the best match 
# Then once we have a list of lists of songs, we can filter by the length and choose the list that has the most matches or vice versa 
def songSentenceImprove2(sentence):

    sentence = filterSentence(sentence)
    res = []
    sentenceList = sentence.split()

    if len(sentenceList) == 1:
        if inDict(sentenceList[0]):
            res.append(sentenceList[0])
            return res
        else:
            print("No songs found")
            return []

    stepLower = 2
    stepHigher = 7

    for step in range(stepLower, stepHigher): 
        start = 0
        end = len(sentenceList)
        tempRes = []
        b = True
        e = end 
        while b:
            if start+step > len(sentenceList): 
                tempSentence = " ".join(sentenceList[start:end])
                e = end 
                if inDict(tempSentence):
                    tempRes.append(tempSentence)
                    res.append(tempRes)
                    b = False 
            else: 
                tempSentence = " ".join(sentenceList[start:start+step])
                e = start + step
            # print(tempSentence)
            if b: 
                if inDict(tempSentence):
                    tempRes.append(tempSentence)
                    start = e
                    if start >= len(sentenceList):
                        res.append(tempRes)
                        b = False
                else:
                    start += 1

    # print(res)
    return res 

var = songSentenceImprove2("wooly bully how are you doing. I want you to hold me thrill me kiss me, because ill never find another you")
sList = ["i", "like", "it"]
sentence = "i like it"

y = getIndexWord(sList, sentence)
d = songSentence("i like it when you buy me this diamond ring do you know that")
# From this example, we can see that the function can seperate the sentence into the two songs that are present in the sentence
t = songSentence(
    "mrs brown youve got a lovely daughter, ill never find another you")
# The main funciton that we will be calling to get the song names
# we chose to return the list with the most songs for our improved song filtering 
# we can also choose to return the one with the min or anything like that 
def runSong(sentence): 

    sentenceList = sentence.split()
    if len(sentenceList) > 8: 
       listOSongs = songSentenceImprove2(sentence)
       longestList = max(listOSongs,key=len)
       return longestList
    else: 
        return songSentence(sentence)s = runSong("you were on my mind unchained melody")

o = runSong("wooly bully how are you doing. I want you to hold me thrill me kiss me, because ill never find another you")
n = runSong("i like it when you buy me this diamond ring silhouettes")
g = runSong("mr tambourine man ill never find another you")
# Imports 
from youtubesearchpython import VideosSearch
# Practice to show how the results are given back from the library 
videosSearch = VideosSearch(song, limit=1)
print(videosSearch.result())# Testing the function to extract the urls given a list of songs 
# Important to note that we are returning the first result from the youtube search 
listSongs = ['i like it', 'this diamond ring', 'silhouettes']
# listSongs = ["i like it"]
urlLinks = []
for song in listSongs: 
    videosSearch = VideosSearch(song, limit=1)
    link = videosSearch.result()["result"][0]["link"]
    urlLinks.append(link)

print(urlLinks)
def getUrlLinks(listSongs): 
    urlLinks = []

    if len(listSongs) == 0: 
        return []

    for song in listSongs:
        videosSearch = VideosSearch(song, limit=1)
        link = videosSearch.result()["result"][0]["link"]
        urlLinks.append(link)
    
    return urlLinks
def getSongThumbnail(listSongs):
    thumbnails = []

    if len(listSongs) == 0:
        return []

    for song in listSongs:
        videosSearch = VideosSearch(song, limit=1)
        link = videosSearch.result()["result"][0]["thumbnails"][0]["url"]
        thumbnails.append(link)

    return thumbnails
# testing to see if the url of the thumbnail images are returned 
listSongs = ['i like it', 'this diamond ring', 'silhouettes']

thumbnails = getSongThumbnail(listSongs)

from IPython import display
display.Image('https://i.ytimg.com/vi/xTlNMmZKwpA/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBMyKLeZvTxSi89EBrCg5cUEnNe0w.jpg')
# Final fucntion that can take a sentence and return urls to videos and thumbnail images 
def songafy(sentence): 
    listSongs = runSong(sentence)
    urlLinks = getUrlLinks(listSongs)
    thumbnails = getSongThumbnail(listSongs)
    
    if thumbnails == []: 
        return 

    for i in range(len(thumbnails)):
        thumbnails[i] = thumbnails[i] + ".jpg" 
    for song in listSongs:
        print(song)
    ipyplot.plot_images(thumbnails, max_images=20, img_width=150)

    for url in urlLinks: 
        print(url)

    return testSentence = "i like it when you buy me this diamond ring silhouettes"
songafy(testSentence)
testSentence = "I love being together. Dancing under the moonlight in the stars is beautiful. "
songafy(testSentence)
testSentence = "its not unusual to love stacys mom"
songafy(testSentence)
testSentence = "secret agent man the sound of silence is just like me"
songafy(testSentence)
testSentence = "i fought the law in a yellow submarine with zorba the greek and died hungry"
songafy(testSentence)