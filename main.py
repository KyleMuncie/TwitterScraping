# Kyle Muncie
# CSE472 Project 1
# Importing
import matplotlib.pyplot as plt
import networkx as nx
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating global variables for the amount of tweets I want to pull, and also two arrays for the tweets
maxTweets = 100
proVaccineTweets = []
antiVaxTweets = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('#covidvaccines since:2022-09-14 until:2022-09-21').get_items()):
    if i > maxTweets:
        break
    proVaccineTweets.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(proVaccineTweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# Display first 5 entries from dataframe
# tweets_df2.head()

# Export dataframe into a CSV
tweets_df2.to_csv('proVax.csv', sep=',', index=False)

g1 = nx.petersen_graph()
nx.draw(g1)
plt.show()

