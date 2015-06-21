# -*- coding: utf-8 -*-
__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
import argparse
# import datetime
import os
import glob
import pickle
# import matplotlib.pyplot as plt
import random
import  json
import networkx as nx
import twitter 
import time
import sys
''' Run it with 
    python followers.py user_list1.txt testy_userset.dmp --input testy/users  
    user_list1.txt the name of the file of users to search for followers
    testy_userset.dmp will be created by the plots.py for the testy.json
    --input testy/users the folder containing the above files
    If you run it once and fill the auth codes then this auth will be saved in 
    a auth_cred.txt file and can loaded with -a auth_cred.txt
'''


def load_login_cred(args):
    '''Loads the credentials for Twitter api from a file if exists or create a new file'''
    credentials=dict()
    if args.auth!=None:
        f=open(args.auth)
        for li in f:
            li=li.strip()
            lil=li.split(' , ')
            credentials[lil[0]]=lil[1]
        f.close()
    elif args.auth_dict!=None:
        f=open(args.auth_dict)
        credentials=pickle.load(f)
        f.close()


    else:
        print 'Go to http://twitter.com/apps/new to create an app and get these items.'
        'Consumer key, Consumer secret, Access token, Access token secret'
        credentials['CONSUMER_KEY']=raw_input('Give me the Consumer key: ')
        credentials['CONSUMER_SECRET']=raw_input('Give me the Consumer secret: ')
        credentials['OAUTH_TOKEN']=raw_input('Give me the Access token: ')
        credentials['OAUTH_TOKEN_SECRET']=raw_input('Give me the Access token secret: ')
        f=open('auth_cred.txt','w')
        for i in credentials:

            f.write(i+' , '+str(credentials[i])+'\n')
        f.close()
    return credentials


def login(credentials):
    # print credentials

    auth = twitter.Api(consumer_key=credentials['CONSUMER_KEY'], \
        consumer_secret=credentials['CONSUMER_SECRET'], \
        access_token_key=credentials['OAUTH_TOKEN'],\
         access_token_secret=credentials['OAUTH_TOKEN_SECRET'])

    return auth
def get_followers_filtered(auth,userId):

    # print auth.VerifyCredentials()
    try:
        # print auth.GetSleepTime('/followers/ids'),'b'
        results=auth.GetFollowerIDs(user_id=userId)
        # print auth.GetSleepTime('/followers/ids'),'a'
        print len(results)
    # print results
    
    # results=auth.GetFollowerIDs(user_id=userId)

    # sec = auth.GetSleepTime('/followers/list')
    # print sec
    # time.sleep(sec)
    except Exception,e:
        print e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        results=None
        print userId, results
    return results


def create_list_of_followers(users,userdic,folder_name,args):
    print "Start : %s" % time.ctime()
    credentials=load_login_cred(args)
    non_checked=[]
    follow_dic=dict()
    filenam=os.path.join('/home/sergi/Dropbox/obama','followers_ch1_f.tmp')
    filenama=os.path.join('/home/sergi/Dropbox/obama','followers_non_checked_ch1_f.tmp')
    try:
        f=open(filenam)
        fo_temp=f.readlines()
        fofo=fo_temp[-1]
        startings=fofo.split(' , ')[0]
        starting=users.index(startings)+1
        f.close()
    except Exception,e:
        print e,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        starting=0
    f=open(filenam,'a')
    fa=open(filenama,'a')

    while True:
        if args.auth_dict!=None:
            for l in credentials:
                print l
                auth=login(credentials[l])
                rates=auth.GetRateLimitStatus(resource_families='followers')
                ratesn=rates['resources']['followers']['/followers/ids']['remaining']
                print ratesn,'out'
                if ratesn < 2 :
                    continue

                print 'mm',starting,len(users)
                if starting==len(users):
                    break
                try:
                    for user in users[starting:]:
                        print user,'aaaaa'
                        rates=auth.GetRateLimitStatus(resource_families='followers')
                        ratesn=rates['resources']['followers']['/followers/ids']['remaining']

                        print ratesn,'in'
                        if ratesn < 2 :
                            # continue
                            print 'change'
                            break

                        follow=get_followers_filtered(auth,user)
                        strfoll=str(user)+' , '
                        follow_list=[]
                        if follow==None:
                            non_checked.append(user)
                            strnon='%s ==>none\n' %user
                            fa.write(strnon)
                            print user,follow,'=========='
                            continue

                        for ids in follow:
                            if ids in userdic:
                                follow_list.append(ids)
                                strfoll+=str(ids)+' , '

                        follow_dic[user]=follow_list
                        strfoll = strfoll+'\n'

                        f.write(strfoll)
                    starting=users.index(user)+1
                except Exception, e:
                    print e
                    print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)

                    print starting,users.index(user),len(users)-1,user
                    if users.index(user)==len(users)-1:
                        break 


        else:
            auth=login(credentials)
        print 'mm',starting,len(users)
        if starting==len(users):
            break
        try:
            for user in users[starting:]:
                print user,'aaaaa'
                rates=auth.GetRateLimitStatus(resource_families='followers')
                ratesn=rates['resources']['followers']['/followers/ids']['remaining']

                print ratesn
                if ratesn < 2 :
                    print 'time waiting'

                    time.sleep(15*60)
                follow=get_followers_filtered(auth,user)

                strfoll=str(user)+' , '
                follow_list=[]
                for ids in follow:
                    if ids in userdic:
                        follow_list.append(ids)
                        strfoll+=str(ids)+' , '

                follow_dic[user]=follow_list
                strfoll = strfoll+'\n'

                f.write(strfoll)
            starting=users.index(user)+1
        except Exception, e:
            print e
            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            time.sleep(16*60)
            print starting,users.index(user),len(users)-1,user
            if users.index(user)==len(users)-1:
                break 
    f.close()
    print "End : %s" % time.ctime()
    filenam=os.path.join('%s' % args.input,'non_checked.dmp')
    f=open(filenam)
    pickle.dump(non_checked, f)
    f.close()
    return follow_dic

if __name__ == '__main__':
    # Parse command-line args for output file name.
    parser = argparse.ArgumentParser(description=(
        'Proccessing the user file(s) and create network of followers'))
    parser.add_argument('-o', '--output',nargs='?', metavar='Output FILE', type=str,
        default=None, help='output folder name')
    parser.add_argument('-i', '--input',nargs='?', metavar='Input FILE', type=str,
        default=None, help='input folder path ')
    parser.add_argument('userIds', metavar='File of users', type=str,
        default=None, help='File that contains the user ids of the network')
    parser.add_argument('search', metavar='File of users', type=str,
        default=None, help='File that contains the user ids to search')
    parser.add_argument('-a', '--auth',nargs='?', metavar='Auth FILE', type=str,
        default=None, help='input the filename of credentials')
    parser.add_argument('-af', '--auth_dict',nargs='?', metavar='Auth dictionary', type=str,
        default=None, help='input the filename of credentials dictionary')
    parser.add_argument('-v','--verbose', nargs='?', metavar='Verbose set on off', type=bool,
        default=False, help='Setting verbose on off')
    args = parser.parse_args()

    if args.input !=None:
        folder_name=args.input
    else:
        folder_name=''
    
    try:
        filenam=os.path.join('%s' % folder_name,args.search)
        f=open(filenam)
        userset=pickle.load(f)
        f.close()
    except Exception,e:
        print e,"Can't find the User's set give me the input folder"
        quit()  
    try:
        filenam=os.path.join('%s' % folder_name,args.userIds)
        f=open(filenam)
        users=[ids.strip()  for ids in f]
        print len(users)
        f.close()
    except Exception,e:
        print e,"Can't find the User's file give me the input folder"
        quit() 

    follow_dic=create_list_of_followers(users,userset,folder_name,args)

