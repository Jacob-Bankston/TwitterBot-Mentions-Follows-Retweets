# Python Twitter API
import tweepy

# To Delay the forever loop for the bottom
import time

# Import your consumer_key, consumer_secret, access_token and access_token_secret
from keys import keys

consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

# oauth for developer account
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# shortcut to tie into account
api = tweepy.API(auth)

# .txt file to pull recent id that we last responded to
the_text_file_name = 'last_seen_id.txt'

# retrieving the last id from the file to not have to search something we've already searched
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# storing id to file to not waste time re-searching through tweets
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# list to store who we follow for our 'subscription' feature
friends = []

# adding all users we follow to a list to check against so we don't have to constantly hit the API with multiple requests each time.
def store_friend_list():
    for friend in tweepy.Cursor(api.friends).items():
        friends.append(friend.id_str)

# function to check for mentions and whether or not they said the specific phrase to 'subscribe' or 'unsubscribe'
def respond_to_mentions():
    print('responding to mentions...')
    last_seen_id = retrieve_last_seen_id(the_text_file_name)

    # Need the tweet_mode='extended' to cover grabbing the full text of the tweet.
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    # Going from the previous search in mentions up through the present search
    for mention in reversed(mentions):
        
        # Storing new mention.id as the new location for the last_seen_id point to the file
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, the_text_file_name)

        # Checking for the phrase to 'subscribe' to my retweet service from my bot!
        if 'boost my tweets' in mention.full_text.lower():
            print('following...')
            api.create_friendship(mention.user.id)

            # Appending to the list so I do not have to hit the API for the friend list again during the loop
            friends.append(mention.user.id_str)

        # Checking for the phrase to 'unsubscribe' to my retweet service from my bot!    
        elif 'stop boosting' in mention.full_text.lower():
            print('unfollowing...')
            api.destroy_friendship(mention.user.id)

            # Taking out the friend from the list so they are not accidentally retweeted while the system is running.
            friends.remove(mention.user.id_str)

# function to retweet the hashtag #codingbootcamp in recent tweets if they are followed by the account
def retweet_the_hashtag():
    print('retrieving and retweeting the hashtag #CodingBootcamp...')

    # Setting the search term for the retweet
    search = ("#codingbootcamp")

    # Setting the number of tweets to retweet
    numberofTweets = 5

    # Iterating through tweets with Cursor to find tweets with the hashtag
    for tweet in tweepy.Cursor(api.search, q=search, tweet_mode='extended').items(numberofTweets):

        # Catching errors and printing them while searching
        try:
            
            # Finding the user's id in the post and checking against the friend list
            if tweet.author._json['id_str'] in friends:
                print("We're buddies so I'm gonna retweet your post!")
                tweet.retweet()
            else:
                print("We're so not friends, so no retweet from me...")

        # Printing the error to find out what is wrong        
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

while True:
    respond_to_mentions()
    retweet_the_hashtag()
    time.sleep(20)
