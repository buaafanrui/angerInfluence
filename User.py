# coding:utf-8
from __future__ import division
from db_trans import *
import re


class User:
    def __init__(self, user, time_cstrt, mood_list=[]):
        if mood_list:
            self.mood_list = mood_list
        else:
            self.month_list = time_cstrt
            self.ID = user[u'ID']
            self.name = user[u'name']
            self.tweet_num = 0
            self.retweeted_dict = dict()
            self.mood_list = [0, 0, 0, 0]
            self.__general(user[u'tweet_list'])

    def __general(self, raw_tweet_list):
        for tweet in raw_tweet_list:
            if self.__is_mid_intime(tweet):
                self.tweet_num += 1
                moodnum = tweet[u'mood']
                if moodnum != -1:
                    self.mood_list[moodnum] += 1
                if u'retweeted_ID' in tweet:
                    if tweet[u'retweeted_ID'] in self.retweeted_dict:
                        self.retweeted_dict[tweet[u'retweeted_ID']] += 1
                    else:
                        self.retweeted_dict[tweet[u'retweeted_ID']] = 1
        all_num = sum(self.mood_list)
        if all_num != 0:
            for i in range(0, len(self.mood_list)):
                self.mood_list[i] = self.mood_list[i] / all_num

    def __is_mid_intime(self, tweet):
        if u'date' in tweet:
            date = tweet[u'date']
            p_date = re.compile(r'2010\d{4}')
            if p_date.match(date):
                if int(date[4:6]) in self.month_list:
                    return True
        return False

    def test(self):
        if self.__is_mid_intime(0):
            print 'match'
        else:
            print 'notmatch'


if __name__ == '__main__':
    user = User(get_user(1714957665), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    print user.ID
    print user.mood_list
    print user.retweeted_dict
    a = raw_input('end:')
