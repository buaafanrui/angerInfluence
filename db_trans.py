# coding:utf-8

import sys
import traceback

import pymongo as pm

db = pm.Connection('192.168.104.108', 30000)['trans']
posts_users = db['users']


def get_user(ID):
    try:
        rst = posts_users.find({u'ID': ID}).limit(1)
        for user in rst:
            return user
    except:
        traceback.print_exc(file=sys.stdout)
        return {}


def is_exist_user(ID):
    try:
        rst = posts_users.find({u'ID': ID})
        if rst.count() > 0:
            return True
        else:
            return False
    except:
        traceback.print_exc(file=sys.stdout)
        return False


def insert_user(user_dic):
    try:
        posts_users.insert(user_dic)
    except:
        traceback.print_exc(file=sys.stdout)


def update_user(userid, key, value):
    try:
        posts_users.update({u'ID': userid}, {'$set': {key: value}})
    except:
        traceback.print_exc(file=sys.stdout)


def del_user(userid):
    try:
        posts_users.remove({u'ID': userid})
    except:
        traceback.print_exc(file=sys.stdout)


def get_users(num):  # if num=0,return all users
    try:
        if num > 0:
            rst = posts_users.find().limit(num)
        else:
            rst = posts_users.find()
        return rst
    except:
        traceback.print_exc(file=sys.stdout)
        return []
