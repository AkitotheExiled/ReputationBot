import praw
from configparser import ConfigParser
import re
import requests, requests.auth



class Rep_Bot():

    def __init__(self):
        CONFIG = ConfigParser()
        CONFIG.read('config.ini')
        self.user = CONFIG.get('main', 'USER')
        self.password = CONFIG.get('main', 'PASSWORD')
        self.client = CONFIG.get('main', 'CLIENT_ID')
        self.secret = CONFIG.get('main', 'SECRET')
        self.subreddit = CONFIG.get('main', 'SUBREDDIT')
        self.token_url = "https://www.reddit.com/api/v1/access_token"
        self.command = CONFIG.get('main', 'COMMAND')
        self.token = ""
        self.t_type = ""
        self.user_agent = "'RepBot/V1.0 by ScoopJr'"
        print('Starting up...', self.user_agent)
        self.multiple_kudos = bool(CONFIG.get('main', 'MULTIPLE_KUDOS'))
        self.flair_template = CONFIG.get('main', 'FLAIR_TEMPLATE')
        self.sub_flair_setup = bool(CONFIG.get('main', 'SUB_FLAIR_SETUP'))
        print(self.multiple_kudos == True)
        self.reddit = praw.Reddit(client_id=self.client,
                             client_secret=self.secret,
                             password=self.password,
                             user_agent=self.user_agent,
                             username=self.user)
        try:
            with open('thanked_comments.txt', 'r') as g:
                self.thanked_comments = g.read()
        except FileNotFoundError:
            with open('thanked_comments.txt', 'w') as e:
                e.write('')
        self.checker = True


    def get_token(self):
        client_auth = requests.auth.HTTPBasicAuth(self.client, self.secret)
        post_data = {'grant_type': 'password', 'username': self.user, 'password': self.password}
        headers = {'User-Agent': self.user_agent}
        response = requests.Session()
        response2 = response.post(self.token_url, auth=client_auth, data=post_data, headers=headers)
        self.token = response2.json()['access_token']
        self.t_type = response2.json()['token_type']

    def check_posts(self):
        for post in self.reddit.subreddit(self.subreddit).new():
            if not post.archived:
                for comment in post.comments:
                    if self.multiple_kudos:
                        with open('thanked_comments.txt', 'r') as g:
                            self.thanked_comments = g.read()
                        for com in comment.replies:
                            if com.id in self.thanked_comments:
                                print(com.id, com.body, com.author)
                                continue
                            if (com.body == self.command) & (comment.body == self.command):
                                print(com.id, com.body, com.author, comment.id, comment.body, comment.body)
                                continue
                            else:
                                if ((com.body == self.command) & (not comment.is_submitter)):
                                    print("1", com.id, com.author, comment.author)
                                    with open('thanked_comments.txt', 'a') as f:
                                        f.write(com.id + ',')
                                        f.close()
                                    self.update_flair(comment.author)
                        break
                    if not self.multiple_kudos:
                        with open('thanked_comments.txt', 'r') as g:
                            self.thanked_comments = g.read()
                        for com in comment.replies:
                            if com.id in self.thanked_comments:
                                continue
                            else:
                                if (com.body == self.command) & (not comment.is_submitter):
                                    print("2", com.id, com.author, comment.author)
                                    with open('thanked_comments.txt', 'w+') as f:
                                        f.write(comment.id + ',')
                                        f.close()
                                    self.update_flair(comment.author)
                                    break
                    break
        self.checker = False
        return print('Done')


    def update_flair(self, user):
        # grab current flair
        try:
            print('Current User:', user)
            cur_flair = self.reddit.subreddit(self.subreddit).flair(redditor=user)
            for user2 in cur_flair:
                print(user2)
                flair_text = user2['flair_text']
            print(flair_text)
            regex = re.match(r"(\D+)(\d+)", flair_text)
            print(regex.group(1))
            # add rep to current flair
            num = int(regex.group(2))
            update_flair = self.reddit.subreddit(self.subreddit).flair.set(redditor=user,
                                                                       text=(regex.group(1) + str(num + 1)))
            return update_flair
        except TypeError:
            self.reddit.subreddit(self.subreddit).flair.set(user, text=self.flair_template)
            self.update_flair(user=user)

    def flair_template_setup(self):
        if self.sub_flair_setup:
            return print('Flair templates have already been setup for this sub!  If you believe this to be in error, \
                         contact www.github.com/user/AkitoTheExiled.')
        else:
            if self.flair_template not in self.reddit.subreddit(self.subreddit).flair.templates:
                self.reddit.subreddit(self.subreddit).flair.templates.add(self.flair_template)
            with open('config.ini', 'r') as c:
                data = c.readlines()
            print(data)
            data[7] = 'SUB_FLAIR_SETUP=True'
            with open('config.ini', 'w') as f:
                f.writelines(data)
                f.close()
            c.close()
            return print('Done adding and setting user flairs.')

if __name__ == '__main__':
    bot = Rep_Bot()
    bot.flair_template_setup()
    while bot.checker:
        bot.check_posts()

