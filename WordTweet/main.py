import datetime
import sys


class UserNode:
    def __init__(self, idnum, date, nickname):
        self.idnum = idnum
        self.date = date
        self.nickname = nickname
        self.friend = []

    def __hash__(self):
        return self.idnum

    def __eq__(self, other):
        return self.idnum == other

    def addfriend(self, friend):
        if friend not in self.friend:
            self.friend.append(friend)


class TweetNode:
    def __init__(self, idnum, date, content):
        self.idnum = idnum
        self.date = date
        self.content = content


def readuserfile():
    users = set()
    while True:
        userfile = input("Path for User Profile file (Default: .\\user.txt): ")
        if "" == userfile:
            userfile = "user.txt"
        try:
            f = open(userfile, "r", encoding="utf8")
            readcount = 1
            tmp = f.readline()
            idnum = 0
            date = datetime.datetime
            while tmp:
                try:
                    if readcount % 4 == 1 and len(tmp) > 0:
                        idnum = int(tmp)
                    elif readcount % 4 == 2:
                        date = datetime.datetime.strptime(tmp, "%a %b %d %H:%M:%S %z %Y\n")
                    elif readcount % 4 == 3:
                        if idnum not in users:
                            users.add(UserNode(idnum, date, tmp))
                        else:
                            print("Duplicate user id", idnum, "omitted.")
                except ValueError:
                    print("Wrong input from user profile file!!! Line #", readcount, sys.exc_info())
                tmp = f.readline()
                readcount += 1
            print("Total users:", int(readcount / 4))
            f.close()
            break
        except FileNotFoundError:
            print("Wrong path for user profile file!!!", sys.exc_info())
    return users


def readfriendfile(users):
    while True:
        frdfile = input("Path for Friendship file (Default: .\\friend.txt): ")
        if "" == frdfile:
            frdfile = "friend.txt"
        try:
            f = open(frdfile, "r", encoding="utf8")
            read = f.readline()
            readcount = 1
            frdcount = 0
            frdone = -1
            while read:
                if readcount % 3 != 0:
                    tmp = int(read)
                if readcount % 3 != 0 and tmp not in users:
                    print("Can't find user id", tmp, "in the user profile data file!")
                elif readcount % 3 == 1:
                    frdone = tmp
                elif readcount % 3 == 2:
                    for e in users:
                        if frdone == e.idnum:
                            frdcount += 1
                            e.addfriend(tmp)
                            break
                readcount += 1
                read = f.readline()
            print("Total friendship records (excluding duplicates):", frdcount)
            f.close()
            break
        except FileNotFoundError:
            print("Wrong path for friendship file!!!", sys.exc_info())


def readtweet(users):
    tweets = []
    while True:
        wordfile = input("Path for Word Tweet file (Default: .\\word.txt): ")
        if "" == wordfile:
            wordfile = "word.txt"
        try:
            f = open(wordfile, "r", encoding="utf8")
            tmp = f.readline()
            readcount = 1
            idnum = -1
            date = datetime.datetime
            while tmp:
                if readcount % 4 == 1:
                    idnum = int(tmp)
                elif readcount % 4 == 2:
                    date = datetime.datetime.strptime(tmp, "%a %b %d %H:%M:%S %z %Y\n")
                elif readcount % 4 == 3:
                    if readcount == 3:
                        tweets.append(TweetNode(idnum, date, tmp))
                    else:
                        for i in range(len(tweets)):
                            if tweets[i].idnum >= idnum:
                                tweets.insert(i, TweetNode(idnum, date, tmp))
                                break
                            elif i == len(tweets) - 1:
                                tweets.append(TweetNode(idnum, date, tmp))
                                break
                readcount += 1
                tmp = f.readline()
            print("Total tweets:", int(readcount / 4))
            f.close()
            break
        except FileNotFoundError:
            print("Wrong path for word tweet file!!!", sys.exc_info())
    return tweets

def getinput():
    prompt = "0. Read data files\n" \
             "1. display statistics\n" \
             "2. Top 5 most tweeted words\n" \
             "3. Top 5 most tweeted users\n" \
             "4. Find users who tweeted a word (e.g., ’연세대’)\n" \
             "5. Find all people who are friends of the above users\n" \
             "6. Delete all mentions of a word\n" \
             "7. Delete all users who mentioned a word\n" \
             "8. Find strongly connected components\n" \
             "9. Find shortest path from a given user\n" \
             "99. Quit\n" \
             "Select Menu: "
    return int(input(prompt))


def statistics(users, tweets):
    frdmin = 9999999999999999999999999999
    frdmax = -1
    frdsum = 0
    usrcnt = 0
    tweetmin = 9999999999999999999999999999
    tweetmax = -1
    tweetsum = len(tweets)
    for user in users:
        tmp = len(user.friend)
        if tmp < frdmin: frdmin = tmp
        if tmp > frdmax: frdmax = tmp
        frdsum += tmp
        usrcnt += 1
    tmpuser = -1
    tmpcnt = -1
    for tweet in tweets:
        if tmpuser != tweet.idnum:
            tmpuser = tweet.idnum
            if tmpcnt != -1:
                if tmpcnt < tweetmin: tweetmin = tmpcnt
                if tmpcnt > tweetmax: tweetmax = tmpcnt
            tmpcnt = 1
        else:
            tmpcnt += 1
    print("Average number of friends:", frdsum / usrcnt)
    print("Minimum friends:", frdmin)
    print("Maximum friends:", frdmax)

    print("Average tweets per user:", tweetsum / usrcnt)
    print("Minimum tweet(s) from a user:", tweetmin)
    print("Maximum tweet(s) from a user:", tweetmax)


# def mosttweetword(tweets):
# wordlist = [0, 0, 0, 0, 0]
# currank = 0
# while currank < 5:
#     for tweet in tweets:


def main():
    inputset = []
    users = None
    tweets = None
    usrin = -1
    while usrin != 99:
        try:
            usrin = getinput()
            inputset.append(usrin)
            if usrin != 0 and 0 not in inputset:
                print("**********ERROR!! DATA IS NOT READ**********")
            elif usrin == 0:
                users = readuserfile()
                readfriendfile(users)
                tweets = readtweet(users)
            elif usrin == 1:
                statistics(users, tweets)
                # elif usrin == 2:
                # mosttweetword(tweets)
                # elif usrin ==3:
                # elif usrin ==4:
                # elif usrin ==5:
                # elif usrin ==6:
                # elif usrin ==7:
                # elif usrin ==8:
                # elif usrin ==9:
        except ValueError:
            print("Input must be an integer:", sys.exc_info())
        except:
            print("Unexpected Error!!!", sys.exc_info())




main()
