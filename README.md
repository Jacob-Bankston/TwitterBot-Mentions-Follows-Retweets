# Tweepy Twitter Bot

__The overview of the bot has 2 main functions.__

### Function 1 - Subscription-Like Service via Following and Unfollowing users

* Checks recent mentions starting from the last id it searched.
* If the a user @ mentions the bot with the phrase "boost my posts" it will then follow that user.
* If the a user @ mentions the bot with the phrase "stop boosting" it will then unfollow that user.

### Function 2 - Retweeting specific hastags

* Using the Cursor functionality of tweepy, the bot searches through recent posts for the hashtag #codingbootcamp
* When it finds a tweet with that hashtag it checks to see if it is following that user
* If the bot is following that user then it will retweet the post

That's it! There are a lot of tutorials for simple bots out there, but I didn't want my bot to be spamming the masses.
Thanks for reading, and I hope you like the bot!
