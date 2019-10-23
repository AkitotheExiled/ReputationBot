# ReputationBot
A bot that allows users to give reputation using a command as a reply to a helpful comment.  Perfectly configurable.

### Config.ini
```
[main]
USER =yourusername
PASSWORD=yourpassword
CLIENT_ID=yourclientid
SECRET=yoursecret
SUBREDDIT=yoursubreddit
FLAIR_TEMPLATE=yourflair: 0
SUB_FLAIR_SETUP=False
MULTIPLE_KUDOS=False
COMMAND=!thanks
```

##### SUB_FLAIR_SETUP

If you do not have a default template in place, the bot will automatically add FLAIR_TEMPLATE to your subreddits flairs.

If you do have a default template in place, set SUB_FLAIR_SETUP to True and MAKE SURE your default template is equal to FLAIR_TEMPLATE.

##### MULTIPLE_KUDOS

True, allows user to receive multiple reputation from a singular helpful comment(think upvoting a comment).

False, only allows user to receive ONE reputation per helpful comment.
