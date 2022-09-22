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

    # initiating a set to hold unique words
    # initiating arrays to hold the edges
    uniqueProWords = set()
    uniqueAntiWords = set()
    proEdges = []
    antiEdges = []
    # exclusion pattern to not accept any https which are gifs or any @ signs or most emojis
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

    # Same as the previous but with is for antiVax
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

    # This function is for page rank
    def plot_pagerank_dist(graph, fileName):
        pagerank_list = list(nx.pagerank(graph).values())
        plt.hist(pagerank_list, alpha=0.85)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Histogram for Page Rank')
        plt.savefig(fileName + ".png")

    # this function is for clustering
    def plot_clustering_dist(graph, fileName):
        clustering_coeffs_list = list(nx.clustering(graph).values())
        plt.hist(clustering_coeffs_list, bins=100, range=(0.0, 1.0), density=False)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Histogram for Clustering')
        plt.savefig(fileName + ".png")

    # This function is for degree distribution
    def plot_degree_dist(importedGraph, fileName):
        degrees = [importedGraph.degree(n) for n in importedGraph.nodes()]
        plt.hist(degrees, bins=50, rwidth=20)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution of Nodes')
        plt.savefig(fileName + ".png")

    # Creating a graph and then saving it into a png
    g = nx.Graph()
    # adding the nodes from the unique words for pro-vaccine
    g.add_nodes_from(list(uniqueProWords))
    # adding the edges
    g.add_edges_from(proEdges)
    # drawing the graph
    nx.draw(g, with_labels=True, node_size=100)
    # styling the graph
    plt.title("Network Graph for Pro-Vaccine")
    # Saving the figure as a png
    plt.savefig("networkGraphProVaccine.png")
    # clearing the plt
    plt.clf()
    # making three calls to functions and passing the graph to make histograms
    plot_degree_dist(g, "proVaxHistogram")
    plt.clf()
    plot_clustering_dist(g, "proClusteringHistogram")
    plt.clf()
    plot_pagerank_dist(g, "proPageRankHistogram")

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
    plt.clf()
    plot_clustering_dist(g, "antiClusteringHistogram")
    plt.clf()
    plot_pagerank_dist(g, "antiPageRankHistogram")


if __name__ == "__main__":
    kyle()
