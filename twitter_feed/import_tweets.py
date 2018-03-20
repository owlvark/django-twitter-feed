import tweepy
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from twitter_feed.models import Tweet


class ImportTweets:

    def __init__(self):
        self.consumer_key = settings.TWITTER_FEED_CONSUMER_PUBLIC_KEY_2
        self.consumer_secret = settings.TWITTER_FEED_CONSUMER_SECRET_2
        self.o_auth_token = settings.TWITTER_FEED_OPEN_AUTH_TOKEN_2
        self.o_auth_secret = settings.TWITTER_FEED_OPEN_AUTH_SECRET_2

    def update_tweets(self):
        raw_tweets = self._get_latest_tweets_from_api()       
        tweets = [self._tweepy_status_to_tweet(status=status) for status in raw_tweets]
        print "Imported {} tweets".format(len(tweets))
        self._replace_all_tweets(tweets)

    def _get_latest_tweets_from_api(self):
        """
        http://pythonhosted.org/tweepy/html/index.html
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.o_auth_token, self.o_auth_secret)
        api = tweepy.API(auth)

        return api.user_timeline()

    def _tweepy_status_to_tweet(self, status):
        """
        Fields documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
        """
        tweet = Tweet()
        
        # Make published at timezone aware
        tweet.published_at = timezone.make_aware(status.created_at,  timezone.get_current_timezone())
        tweet.content = status.text

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