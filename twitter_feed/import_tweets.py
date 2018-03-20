import tweepy
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from twitter_feed.models import Tweet


class ImportTweets:

    def __init__(self):
        self.consumer_key_1 = settings.TWITTER_FEED_CONSUMER_PUBLIC_KEY_1
        self.consumer_secret_1 = settings.TWITTER_FEED_CONSUMER_SECRET_1
        self.o_auth_token_1 = settings.TWITTER_FEED_OPEN_AUTH_TOKEN_1
        self.o_auth_secret_1 = settings.TWITTER_FEED_OPEN_AUTH_SECRET_1
        self.consumer_key_2 = settings.TWITTER_FEED_CONSUMER_PUBLIC_KEY_2
        self.consumer_secret_2 = settings.TWITTER_FEED_CONSUMER_SECRET_2
        self.o_auth_token_2 = settings.TWITTER_FEED_OPEN_AUTH_TOKEN_2
        self.o_auth_secret_2 = settings.TWITTER_FEED_OPEN_AUTH_SECRET_2

    def update_tweets(self):
        tweets = []
        raw_tweets = self._get_latest_tweets_from_api()
        for status in raw_tweets:
            tweets.append(self._tweepy_status_to_tweet(status=status))
        raw_tweets = self._get_latest_tweets_from_api(use_second_account=True)
        for status in raw_tweets:
            tweets.append(self._tweepy_status_to_tweet(status=status, use_second_account=True))
        print "Imported {} tweets".format(len(tweets))
        self._replace_all_tweets(tweets)

    def _get_latest_tweets_from_api(self, use_second_account=False):
        """
        http://pythonhosted.org/tweepy/html/index.html
        """
        auth = tweepy.OAuthHandler(self.consumer_key_1, self.consumer_secret_1)
        auth.set_access_token(self.o_auth_token_1, self.o_auth_secret_1)
        if use_second_account:
            auth = tweepy.OAuthHandler(self.consumer_key_2, self.consumer_secret_2)
            auth.set_access_token(self.o_auth_token_2, self.o_auth_secret_2)
        api = tweepy.API(auth)
        return api.user_timeline()

    def _tweepy_status_to_tweet(self, status, use_second_account=False):
        """
        Fields documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
        """
        tweet = Tweet()
        
        # Make published at timezone aware
        tweet.published_at = timezone.make_aware(status.created_at,  timezone.get_current_timezone())
        tweet.content = status.text
        tweet.api_key = self.consumer_key_1
        if use_second_account:
            tweet.api_key = self.consumer_key_2
        return tweet

    @transaction.atomic
    def _replace_all_tweets(self, new_tweets):
        try:
            with transaction.atomic():
                Tweet.objects.remove_all()

                for tweet in new_tweets:
                    tweet.save()

        except Exception as e:
            print e
            pass