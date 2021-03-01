# coding:utf-8
from __future__ import division
import sys
from db_trans import *
from User import User
import copy
import time
import math

'''
1st-stage:create users,include their reposted and retweeted
2nd-stage:create eges,it is a dict,the key is a truple of user,the value is the weight
'''


class CreateGraph:
    def __init__(self, time_cstrt, weibo_num_cstrt=50, edge_weight_cstrt=10, graph_file=None):
        self.month_list = time_cstrt
        self.weibo_num_cstrt = weibo_num_cstrt
        self.edge_weight_cstrt = edge_weight_cstrt
        self.users_dict = dict()
        self.edges_dict = dict()
        if graph_file:
            file = open(graph_file, 'r')
            for line in file:
                user_ID, user_ID_other, weight, mood_list = line.strip().split('\t')
                user_ID = int(user_ID)
                user_ID_other = int(user_ID_other)
                weight = int(weight)
                mood_list = eval(mood_list)
                if not user_ID in self.users_dict:
                    self.users_dict[user_ID] = User(None, [], mood_list)
                if not user_ID in self.edges_dict:
                    self.edges_dict[user_ID] = dict()
                if not user_ID_other in self.edges_dict[user_ID]:
                    self.edges_dict[user_ID][user_ID_other] = weight
            file.close()

    def create_users(self):
        users = get_users(0)
        for user in users:
            if len(user[u'tweet_list']) > self.weibo_num_cstrt:
                try:
                    user_obj = User(user, self.month_list)
                except:
                    user_obj = None
                if user_obj and user_obj.tweet_num >= self.weibo_num_cstrt:
                    self.users_dict[user[u'ID']] = user_obj

    def create_edges(self):
        for user_ID in self.users_dict.keys():
            user = self.users_dict[user_ID]
            retweeted_dict = user.retweeted_dict
            if not user_ID in self.edges_dict:
                self.edges_dict[user_ID] = dict()
            for user_ID_other in user.retweeted_dict:
                if user_ID_other != user_ID and user_ID_other in self.users_dict:
                    user_other = self.users_dict[user_ID_other]
                    weight = user.retweeted_dict[user_ID_other]
                    if user_ID in user_other.retweeted_dict:
                        weight += user_other.retweeted_dict[user_ID]
                    if weight > self.edge_weight_cstrt:
                        if not user_ID_other in self.edges_dict[user_ID]:
                            self.edges_dict[user_ID][user_ID_other] = weight
                        if not user_ID_other in self.edges_dict:
                            self.edges_dict[user_ID_other] = dict()
                        if not user_ID in self.edges_dict[user_ID_other]:
                            self.edges_dict[user_ID_other][user_ID] = weight
            if len(self.edges_dict[user_ID]) == 0:
                del self.edges_dict[user_ID]
                del self.users_dict[user_ID]

    def output(self, file_path):
        file = open(file_path, 'w')
        for user_ID in self.edges_dict:
            for user_ID_other in self.edges_dict[user_ID]:
                file.write(str(user_ID) + '\t' + str(user_ID_other) + '\t' + str(
                    self.edges_dict[user_ID][user_ID_other]) + '\t' + str(self.users_dict[user_ID].mood_list) + '\n')
        file.close()


if __name__ == '__main__':
    graph = CreateGraph([4, 5, 6, 7, 8, 9], 90, 10, 'graph.txt')
    graph.output("10_graph.txt")
