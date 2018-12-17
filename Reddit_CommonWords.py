import sys
import praw
import re
from collections import Counter
import matplotlib.pyplot as plt

commonWords = {'', 'that', 'this', 'and', 'of', 'the', 'for', 'i', 'it', 'has',
'you', 'your', 'to', 'a', 'they', 'have', 'are', 'be', 'me', 'im',
'in', 'up', 'like', 'or', 'at', 'not', 'was', 'is', 'dont', 'on', "but",
'them', 'with', 'those', 'who', 'were', 'out', 'because', 'do', 'as', 'people',
'an', 'will', 'when', 'know', 'so', 'some', 'youre', 'just', 'if', 'youre',
'what', 'about', 'keep', 'go', 'their', 'yourself', 'can', 'going', 'its',
'my', 'how', 'other', 'make', 'there', 'really', 'one', 'glad', 'all', 'said',
'into', 'else', 'did', 'thats', 'someone', 'from', 'find', 'got', 'see', 'most',
'time', 'even', 'deleted', 'only', 'had', 'look', 'post', 'life', 'nice', 'good',
'get', 'great', 'actually', 'well', 'better', 'damn', 'more', 'person', 'always',
'he', 'her', 'think', 'here', 'than', 'we', 'want', 'these', 'by', 'over', 'cant',
'being', 'am', 'didnt', 'then', 'maybe', 'joke', 'posts'}

redditUsername = "[YOUR USERNAME HERE]"
redditPassword = "[YOUR PASSWORD HERE]"

clientID = "[YOUR CLIENT ID HERE]"
clientSecret = "[YOUR CLIENT SECRET HERE]"

userAgent = "[YOUR USERAGENT HERE]"

reddit = praw.Reddit(   client_id=clientID,
                        client_secret=clientSecret,
                        user_agent=userAgent,
                        username=redditUsername,
                        password=redditPassword )

def GatherWordsInPostTitles(subreddit, numOfPosts):
    words = []
    submissionCounter = 0

    for submission in reddit.subreddit(subreddit).top(limit=numOfPosts):
        submissionCounter += 1
        print("Scanning submition %d of %d" % (submissionCounter, numOfPosts))

        words += submission.title.lower().split(' ')

    return SanitiizeWordList(words)

def GatherWordsInPostComments(subreddit, numOfPosts):
    words = []
    submissionCounter = 0

    for submission in reddit.subreddit(subreddit).hot(limit=numOfPosts):
        submissionCounter += 1
        print("Scanning submition %d of %d" % (submissionCounter, numOfPosts))

        submission.comments.replace_more(limit=0)

        commentCounter = 0
        for topLevelComment in submission.comments:
            commentCounter += 1
            print("\tScanning comment %d of %d" % (commentCounter, len(submission.comments)))

            words += topLevelComment.body.lower().split(' ')

    return SanitiizeWordList(words)

def SanitiizeWordList(list):
    list = [re.sub(r"[\W]", "", word) for word in list]
    list = [word for word in list if word not in commonWords]

    return list

def CreatePieChart(subreddit, words, numOftopWords):
    word_count = Counter(words)

    top_words = dict(word_count.most_common(numOftopWords))

    plt.title("Top {0} most common words on r/{1} frontpage".format(len(top_words), subreddit))
    plt.pie(top_words.values(), labels=list(top_words.keys()), startangle=90)
    plt.axis('equal')

    plt.show()

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print("Usage: Reddit_CommonWords.py <titles or comments> <subreddit> <number of posts to search> <number of words to display>")
        sys.exit()

    mode = str(sys.argv[1])
    subreddit = str(sys.argv[2])
    NoOfPosts = int(sys.argv[3])
    NoOfWords = int(sys.argv[4])

    allWords = []

    if (mode == "titles"):
        allWords = GatherWordsInPostTitles(subreddit, NoOfPosts)
    else:
        allWords = GatherWordsInPostComments(subreddit, NoOfPosts)

    CreatePieChart(subreddit, allWords, NoOfWords)