import datetime
import tokens
import tweepy
import xw_reader

if __name__ == "__main__":
    
    # Set up the authentication.
    auth = tweepy.OAuthHandler(tokens.API_KEY, tokens.API_SECRET_KEY) 
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send a tweet.
    tweet_text = xw_reader.get_text()
    api.update_status(tweet_text)
