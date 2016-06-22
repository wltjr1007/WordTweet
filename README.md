# WordTweet Manual
######Korea University 2016-01 Data Structure(Class 02) Term Project.
######Yoon Jee Seok(윤지석) 2012210073

##Project Description
WordTweet is similar to Twitter, but it can only accept one word.

It has various search, delete, graph functions. However, input is manually
inserted into the data file.

###Requirements
Python 3
##General description
###Data file
`user.txt` contains user profile containing ID #, sign up date,
nickname in three parts.

Example
```
433072426
Sat Dec 10 03:28:31 +0000 2011
qhals0086

174670917
Wed Aug 04 14:30:51 +0000 2010
soloist_shin
```
`friends.txt` contains friendship information in two parts.

Example
```
313426093
323060839

313426093
107145933
```

`word.txt` contains tweets in three parts. It contains user ID, date, content.

Example
```
433072426
Sat Mar 17 14:31:34 +0000 2012
그건

433072426
Sat Mar 17 14:31:34 +0000 2012
혼자만의
```

##Functions
###Prompt
```
0. Read data files
1. display statistics
2. Top 5 most tweeted words
3. Top 5 most tweeted users
4. Find users who tweeted a word (e.g., ’연세대’)
5. Find all people who are friends of the above users
6. Delete all mentions of a word
7. Delete all users who mentioned a word
8. Find strongly connected components
9. Find shortest path from a given user
99. Quit
Select Menu:
```

Input: 0~9, 99

Output: Various

###Function Description
####0. Read data files
####1. display statistics
####2. Top 5 most tweeted words
####3. Top 5 most tweeted users
####4. Find users who tweeted a word (e.g., ’연세대’)
####5. Find all people who are friends of the above users
####6. Delete all mentions of a word
####7. Delete all users who mentioned a word
####8. Find strongly connected components
####9. Find shortest path from a given user
####99. Quit