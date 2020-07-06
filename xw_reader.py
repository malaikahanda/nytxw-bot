import datetime
import requests

from bs4 import BeautifulSoup

URL_TEXT = "https://nytcrosswordanswers.org/nyt-crossword-answers-{}-{}-{}/"
TABLE_CLASS = "nywrap"
WORDS_OF_INTEREST = ["TEATS", "TEAT", "TIT", "TITS"]

# Get formatted date.
def get_date():
    td = datetime.date.today()
    d = td.strftime('%d')
    m = td.strftime('%m')
    y = td.strftime('%y')
    return d, m, y


# Request puzzle data from nytcrosswordanswers.org 
def request_page():

    # Format the url.
    d, m, y = get_date()
    url = URL_TEXT.format(d, m, y)

    # Grab the full content of the page.
    page = requests.get(url)
    html = BeautifulSoup(page.content)
    return html


# Pull the clues from the page: returns a list of string tuples.
def get_clues(html):
    t = html.find("div", class_=TABLE_CLASS)

    clues = []
    # There are two tables of clues: iterate through both.
    for ul in t.find_all("ul"):
        for li in ul.find_all("li"):
            hint = li.find("a").text
            answer = li.find("span").text
            clues.append((hint, answer))

    return clues
    

# Return a list of the words-of-interest that are in the puzzle.
def check_words(clues):
    words_of_interest = []
    for (hint, answer) in clues:
        if answer in WORDS_OF_INTEREST:
            words_of_interest.append((hint, answer))
    return words_of_interest

# Create the tweet based on whether the words-of-interest were present.
def format_tweet_text(words):

    # Format the date
    d, m, y = get_date()
    date = "\n\n({}/{}/{})".format(d, m, y)
    
    # No words of interest.
    if len(words) == 0:
        text = "No. #NYTXW"
    else:
        text = "Yes. #NYTXW"

    # Extensible, if I add more than one word-of-interest.
    for (hint, answer) in words:
        text += "\n\nHint: {}".format(hint)

    return text + date

# Wrapper that is called from tweet.py
def get_text():
    page = request_page()
    clues = get_clues(page)
    words = check_words(clues)
    text = format_tweet_text(words)
    return text