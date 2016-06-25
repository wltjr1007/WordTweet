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
            tmp = f.readline().strip()
            idnum = 0
            date = datetime.datetime
            while tmp:
                try:
                    if readcount % 4 == 1 and len(tmp) > 0:
                        idnum = int(tmp)
                    elif readcount % 4 == 2:
                        date = datetime.datetime.strptime(tmp.strip(), "%a %b %d %H:%M:%S %z %Y")
                    elif readcount % 4 == 3:
                        if idnum not in users:
                            users.add(UserNode(idnum, date, tmp.strip()))
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
                if readcount % 4 != 0 and idnum not in users:
                    print("Can't find user id", tmp, "in the user profile data file!")
                elif readcount % 4 == 2:
                    date = datetime.datetime.strptime(tmp.strip(), "%a %b %d %H:%M:%S %z %Y")
                elif readcount % 4 == 3:
                    if readcount == 3:
                        tweets.append(TweetNode(idnum, date, tmp.strip()))
                    else:
                        for i in range(len(tweets)):
                            if tweets[i].idnum >= idnum:
                                tweets.insert(i, TweetNode(idnum, date, tmp.strip()))
                                break
                            elif i == len(tweets) - 1:
                                tweets.append(TweetNode(idnum, date, tmp.strip()))
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


def mosttweetword(tweets):
    sortlist = []
    maxlist = [["", -1], ["", -2], ["", -3], ["", -4], ["", -5]]
    for i in range(len(tweets)):
        content = tweets[i].content
        if i == 0:
            sortlist.append(content)
        else:
            try:
                sortlist.insert(sortlist.index(content), content)
            except ValueError:
                sortlist.append(content)
    tmp = ""
    curcnt = -1
    for word in sortlist:
        if tmp != word:
            if curcnt != -1:
                if maxlist[0][1] < curcnt:
                    maxlist[0][0] = tmp
                    maxlist[0][1] = curcnt
                elif maxlist[1][1] < curcnt:
                    maxlist[1][0] = tmp
                    maxlist[1][1] = curcnt
                elif maxlist[2][1] < curcnt:
                    maxlist[2][0] = tmp
                    maxlist[2][1] = curcnt
                elif maxlist[3][1] < curcnt:
                    maxlist[3][0] = tmp
                    maxlist[3][1] = curcnt
                elif maxlist[4][1] < curcnt:
                    maxlist[4][0] = tmp
                    maxlist[4][1] = curcnt
            tmp = word
            curcnt = 1
        else:
            curcnt += 1
    print("Top 5 most tweeted words")
    print("1.", maxlist[0])
    print("2.", maxlist[1])
    print("3.", maxlist[2])
    print("4.", maxlist[3])
    print("5.", maxlist[4])


def mosttweetuser(tweets, users):
    maxlist = [[0, "", -1], [0, "", -2], [0, "", -3], [0, "", -4], [0, "", -5]]
    tmp = -1
    curcnt = -1
    for tweet in tweets:
        if tmp != tweet.idnum:
            if curcnt != -1:
                if maxlist[0][2] < curcnt:
                    maxlist[0][0] = tmp
                    maxlist[0][2] = curcnt
                elif maxlist[1][2] < curcnt:
                    maxlist[1][0] = tmp
                    maxlist[1][2] = curcnt
                elif maxlist[2][2] < curcnt:
                    maxlist[2][0] = tmp
                    maxlist[2][2] = curcnt
                elif maxlist[3][2] < curcnt:
                    maxlist[3][0] = tmp
                    maxlist[3][2] = curcnt
                elif maxlist[4][2] < curcnt:
                    maxlist[4][0] = tmp
                    maxlist[4][2] = curcnt
            tmp = tweet.idnum
            curcnt = 1
        else:
            curcnt += 1
    for user in users:
        if user.idnum == maxlist[0][0]:
            maxlist[0][1] = user.nickname
        elif user.idnum == maxlist[1][0]:
            maxlist[1][1] = user.nickname
        elif user.idnum == maxlist[2][0]:
            maxlist[2][1] = user.nickname
        elif user.idnum == maxlist[3][0]:
            maxlist[3][1] = user.nickname
        elif user.idnum == maxlist[4][0]:
            maxlist[4][1] = user.nickname

    print("Top 5 most tweeted users [ID #, nickname, tweet count]")
    for i in range(5):
        print(i + 1, ".", maxlist[i])


def searchtweet(tweets, users):
    userin = input("Input a word to search:")
    tweetmentioned = []
    for tweet in tweets:
        if tweet.content == userin and tweet.idnum not in tweetmentioned:
            tweetmentioned.append(tweet.idnum)
    if len(tweetmentioned) != 0:
        print("These users tweeted the word", userin)
        cnt = 1
        for user in users:
            if user.idnum in tweetmentioned:
                print(cnt, ".", user.idnum, user.nickname)
                cnt += 1
    else:
        print("No one tweeted the word ", userin)
    return tweetmentioned


def searchfriend(users, search):
    if len(search) == 0:
        print("Function #4 returned 0 users.")
    else:
        cnt = 0
        print("Friends of users searched in Function #4.")
        for user in users:
            if user.idnum in search:
                cnt += 1
                if len(user.friend) == 0:
                    print(cnt, ". (", user.idnum, user.nickname, ") have no friends.")
                else:
                    print(cnt, ". (", user.idnum, user.nickname, ")'s friends are :", user.friend)
# def heapsort(tweets):
#     def heapify(tweets):
#         start = (len(tweets) - 2) / 2
#         while start >= 0:
#             godown(tweets, start, len(tweets) - 1)
#             start -= 1
#
#     def godown(tweets, start, end):
#         root = start
#         while root * 2 + 1 <= end:
#             child = root * 2 + 1
#             if child + 1 <= end and tweets[child].content < tweets[child + 1].content:
#                 child += 1
#             if child <= end and tweets[root].content < tweets[child].content:
#                 tweets[root], tweets[child] = tweets[child], tweets[root]
#                 root = child
#             else:
#                 return
#
#     heapify(tweets)
#     end = len(tweets) - 1
#     while end > 0:
#         tweets[end], tweets[0] = tweets[0], tweets[end]
#         godown(tweets, 0, end - 1)
#         end -= 1


def main():
    inputset = []
    users = None
    tweets = None
    usrin = -1
    tweetsearch = None
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
            elif usrin == 2:
                mosttweetword(tweets)
            elif usrin == 3:
                mosttweetuser(tweets, users)
            elif usrin == 4:
                tweetsearch = searchtweet(tweets, users)
            elif usrin == 5:
                if 4 not in inputset:
                    print("**********ERROR!! FUNCTION #4 IS NOT PERFORMED**********")
                else:
                    searchfriend(users, tweetsearch)
                # elif usrin ==6:
                # elif usrin ==7:
                # elif usrin ==8:
                # elif usrin ==9:
        # except ValueError:
        #     print("Input must be an integer:", sys.exc_info())
        except:
            print("Unexpected Error!!!", sys.exc_info())


main()
