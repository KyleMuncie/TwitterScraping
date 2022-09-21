# Kyle Muncie
# CSE472 Project 1
# Importing
import matplotlib.pyplot as plt
import networkx as nx
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating global variables for the amount of tweets I want to pull, and also two arrays for the tweets
maxTweets = 200
proVaccineTweets = []
antiVaxTweets = []

# finding the pro-vaccine tweets within the last week
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('#GetVaccinated since:2022-09-14 until:2022-09-21').get_items()):
    if i > maxTweets:
        break
    proVaccineTweets.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Finding the anti-vaccines tweets withing the last week
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('#antivax since:2022-09-14 until:2022-09-21').get_items()):
    if i > maxTweets:
        break
    antiVaxTweets.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating Dataframes for the pro and anti-vaccines
proOutput = pd.DataFrame(proVaccineTweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
antiOutput = pd.DataFrame(antiVaxTweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

proOutput.head()
antiOutput.head()

uniqueWords = []
listWords = []
iterator = -1

# We are going to create an array of unique words
for x in proOutput.Text:
    iterator = iterator + 1
    listWords.append([])
    for word in x.split():
        listWords[iterator].append(word)
        if uniqueWords.count(word) < 1:
            uniqueWords.append(word)

# appending a new column with a list of words
proOutput['Unique'] = listWords

# Exporting the panda dataframes into JSON
hey = proOutput.to_json('proVaxJSON.json', orient='index')
ayo = antiOutput.to_json('antiVaxJSON.json', orient='index')

# g = nx.from_pandas_dataframe(proOutput, source='Username', target='Text')
# nx.draw(g)
# plt.show()
