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
# finding the provaccine tweets within the last week
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('#GetVaccinated since:2022-09-14 until:2022-09-21').get_items()):
    if i > maxTweets:
        break
    proVaccineTweets.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
# Finding the antivaccines tweets withing the last week
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('#StopVaccination since:2022-09-14 until:2022-09-21').get_items()):
    if i > maxTweets:
        break
    antiVaxTweets.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
# Creating Dataframes for the pro and antivacines
proOutput = pd.DataFrame(proVaccineTweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
antiOutput = pd.DataFrame(antiVaxTweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# Display first 5 entries from dataframe
# tweets_df2.head()

# Exporting the panda dataframes into JSON
proOutput.to_json('proVaxJSON.json', orient='index')
antiOutput.to_json('antiVaxJSON.json', orient='index')

# Export dataframe into a CSV
# proOutput.to_csv('proVax.csv', sep=',', index=False)
# antiOutput.to_csv('antiVax.csv', sep=',', index=False)

g1 = nx.petersen_graph()
nx.draw(g1)
plt.show()

