import re
from urllib.parse import urlparse
from collections import defaultdict
import time


url_re     = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
user_re    = re.compile(r"(\B\@\w+)")
hashtag_re = re.compile(r"(\B\#\w+)")

def get_urls(message):
    websites = []
    for m in url_re.findall(message):
        website = urlparse(m[0]).hostname
        if website:
            websites.append(website)
    return websites

def get_users(message):
    users = []
    for m in user_re.findall(message):
        user = m
        users.append(user)
    return users

def get_hashtags(message):
    hashtags = []
    for m in hashtag_re.findall(message):
        hashtag = m
        hashtags.append(hashtag)
    return hashtags


def print_list(title, plist):
    print(f"-{title}----")
    for l in plist:
        print(f"\t{l}")
    print("\n")


def print_counter(title, counter):
    print(f"-{title}----")
    for name, count in counter.items():
        print(f"\t{name:20.20}\t{count}")
    print("\n")


def get_content_matches(message):

    urls     = get_urls(message)
    #print_list("urls", urls)

    users    = get_users(message)    
    #print_list("users", users)

    hashtags = get_hashtags(message)
    #print_list("hashtags", hashtags)


    return urls, users, hashtags



class RegexCounter():

    def __init__(self):
        self.urls     = defaultdict(int)
        self.users    = defaultdict(int)
        self.hashtags = defaultdict(int)


    def add_message(self, message):
        new_urls, new_users, new_hashtags = get_content_matches(message)

        for u in new_urls:
            self.urls[u] += 1
        #self.urls = sorted(self.urls)
        
        for u in new_users:
            self.users[u] += 1
        #self.users = sorted(self.users)

        for u in new_hashtags:
            self.hashtags[u] += 1
        #self.hashtags = sorted(self.hashtags)

    def reset(self):
        self.urls     = defaultdict(int)
        self.users    = defaultdict(int)
        self.hashtags = defaultdict(int)


    def print(self):
        print_counter("URLS", self.urls)
        print_counter("USERS", self.users)
        print_counter("HASHTAGS", self.hashtags)


def test_counter(message):

    counter = RegexCounter()

    while True:
        counter.add_message(message)
        counter.print()
        time.sleep(1)

