userinput = 0
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


def getinput():
    userinput = input(prompt)
    print(userinput)


def main():
    getinput()


main()
