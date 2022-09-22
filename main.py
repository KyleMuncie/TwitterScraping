# Kyle Muncie
# CSE472 Project 1
# Importing
import matplotlib.pyplot as plt
import networkx as nx
import snscrape.modules.twitter as sntwitter
import re


def kyle():
    # Creating global variables for the amount of tweets I want to pull, and also two arrays for the tweets
    maxTweets = 200
    proVaccineTweets = []
    antiVaxTweets = []

    # finding the pro-vaccine tweets within the last week
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper('#GetVaccinated since:2022-09-14 until:2022-09-21').get_items()):
        if i > maxTweets:
            break
        proVaccineTweets.append(tweet.content)

    # Finding the anti-vaccines tweets withing the last week
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper('#antivax since:2022-09-14 until:2022-09-21').get_items()):
        if i > maxTweets:
            break
        antiVaxTweets.append(tweet.content)

    uniqueProWords = set()
    uniqueAntiWords = set()
    proEdges = []
    antiEdges = []
    exclusionPattern = re.compile(r'(^https|[\U00010000-\U0010ffff]|^@|\U0000231B)', flags=re.UNICODE)

    # node vals
    # edge list
    for tweet in proVaccineTweets:
        # splitting the tweet to get rid of spaces
        rawWords = tweet.split()
        words = []
        for word in rawWords:
            # using the exclusionPattern to check to see if there are emojis, urls, or @s
            m = re.search(exclusionPattern, word.strip())
            if m:
                continue
            words.append(word)
        for i in range(len(words)):
            uniqueProWords.add(words[i])
            if i < len(words) - 1 and len(words) > 1:
                proEdges.append((words[i], words[i + 1]))

    for tweet in antiVaxTweets:
        rawWords = tweet.split()
        words = []
        for word in rawWords:
            m = re.search(exclusionPattern, word.strip())
            if m:
                continue
            words.append(word)
        for i in range(len(words)):
            uniqueAntiWords.add(words[i])
            if i < len(words) - 1 and len(words) > 1:
                antiEdges.append((words[i], words[i + 1]))

    string_list = ["#GetVaccinated", "#antivax", "the", "to", 'to']

    def plot_degree_dist(importedGraph, fileName):
        degrees = [importedGraph.degree(n) for n in importedGraph.nodes() if n not in string_list]
        plt.hist(degrees, bins=50, rwidth=20)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution of Nodes')
        plt.savefig(fileName + ".png")

    # Creating a graph and then saving it into a png
    g = nx.Graph()
    g.add_nodes_from(list(uniqueProWords))
    g.add_edges_from(proEdges)
    nx.draw(g, with_labels=True, node_size=100)
    plt.title("Network Graph for Pro-Vaccine")
    plt.savefig("networkGraphProVaccine.png")
    plt.clf()
    plot_degree_dist(g, "proVaxHistogram")

    # clearing the graph and then also clearing the plt
    g.clear()
    plt.clf()

    # creating a new graph for the antivaccines and then also exporting to png
    g = nx.Graph()
    g.add_nodes_from(list(uniqueAntiWords))
    g.add_edges_from(antiEdges)
    nx.draw(g, with_labels=True, node_size=100)
    plt.title("Network Graph for Anti-Vaccine")
    plt.savefig("networkGraphAntiVaccine.png")
    plt.clf()
    plot_degree_dist(g, "antiVaxHistogram")

    g.clear()
    plt.clf()


if __name__ == "__main__":
    kyle()
