#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sample script that collects tweets matching a string.

'''Collect tweets matching a text pattern and store them
continuously in JSON-formatted lines of a local file.'''

__author__ = 'Giorgos Keramidas <gkeramidas@gmail.com>'
__moderator__ = 'sergioslenis@gmail.com'

import argparse
import errno
import json
import os
import sys
import twitter ##pip install --user python-twitter
import ast
import time
import pickle
import glob
import fnmatch
import os


class UserAuth(object):
    """docstring for UserAuth
        Create authentication for Twitter Api
        creddir: directory containing the credentials for login default /credentials
        auth_cr: a tuple with credentials (CONSUMER_KEY,CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
        auth_file: filename of the txt file that has stored the credentials
        auth_dict: filename of the credential file that has the dictionary of credentials stored

        """
    def __init__(self,auth_cr=(),auth_file=None,auth_dict=None, creddir=None,working_path=None):
        
        # self.args = arg
        if working_path==None:
            self.working_path=os.getcwd()
        else:
            self.working_path=working_path
        if creddir ==None:
            self.creddir=os.path.join('%s' % self.working_path,'credentials/') 
        else:
            self.creddir=os.path.join('%s' % self.working_path,creddir)
        try:
            os.stat(self.creddir)
        except:
            os.mkdir(self.creddir)
        self.auth_cr=auth_cr
        self.auth_file=auth_file 
        self.auth_dict=auth_dict
        self.credentials={}#load_login_cred()
        self.auth=None

    def load_login_cred(self):#.auth,args.auth_dict):
        '''Loads the credentials for Twitter api from a file if exists or create a new file'''

        if len(self.auth_cr)==4:
            # cons_key,cons_sec,oa_tok,oa_tok_sec=self.auth_cr
            self.credentials['CONSUMER_KEY']=self.auth_cr[0]
            self.credentials['CONSUMER_SECRET']=self.auth_cr[1]
            self.credentials['OAUTH_TOKEN']=self.auth_cr[2]
            self.credentials['OAUTH_TOKEN_SECRET']=self.auth_cr[3]
            out_file_name=os.path.join('%s' % self.creddir,'auth_cred.txt')

            f=open(out_file_name+,'w')
            for i in self.credentials:
                f.write(i+' , '+str(self.credentials[i])+'\n')
            f.close()
        if self.auth_file!=None:
            f=open(self.auth_file)
            for li in f:
                li=li.strip()
                lil=li.split(' , ')
                self.credentials[lil[0]]=lil[1]
            f.close()
        elif self.auth_dict!=None:
            f=open(self.auth_dict)
            self.credentials=pickle.load(f)
            f.close()


        else:
            print 'Go to http://twitter.com/apps/new to create an app and get these items.'
            'Consumer key, Consumer secret, Access token, Access token secret'
            self.credentials['CONSUMER_KEY']=raw_input('Give me the Consumer key: ')
            self.credentials['CONSUMER_SECRET']=raw_input('Give me the Consumer secret: ')
            self.credentials['OAUTH_TOKEN']=raw_input('Give me the Access token: ')
            self.credentials['OAUTH_TOKEN_SECRET']=raw_input('Give me the Access token secret: ')
            out_file_name=os.path.join('%s' % self.creddir,'auth_cred.txt')
            f=open(out_file_name+,'w')
            for i in self.credentials:

                f.write(i+' , '+str(self.credentials[i])+'\n')
            f.close()

    def login(self):
        if len(self.credentials)==0:
            self.load_login_cred()

        self.auth = twitter.Api(consumer_key=self.credentials['CONSUMER_KEY'], \
            consumer_secret=self.credentials['CONSUMER_SECRET'], \
            access_token_key=self.credentials['OAUTH_TOKEN'],\
             access_token_secret=self.credentials['OAUTH_TOKEN_SECRET'])
    def check_login(self):
        print(self.auth.VerifyCredentials())

class TwitterSearch(object):
    """docstring for TwitterSearch
        

"""
    def __init__(self, search_text,auth,working_path=None,out_file_dir=None):
        
        self.search_text=unicode(search_text,'utf-8')
        self.auth=auth
        if working_path==None:
            self.working_path=os.getcwd()
        else:
            self.working_path=working_path
        if out_file_dir==None:
            self.out_file_dir=os.path.join('%s' % self.working_path,'Output')
        else:
            self.out_file_dir=os.path.join('%s' % self.working_path,out_file_dir)
        try:
            os.stat(self.out_file_dir)
        except:
            os.mkdir(self.out_file_dir)
        filename=''
        for term in search_text.split():
            filename+=term+'_'

        self.out_file_name=os.path.join('%s' % self.out_file_dir,filename[:-1]+'.json')
        self.out_file_name_ids=os.path.join('%s' % self.out_file_dir,filename[:-1]+'.ids')

        self.seen=preload_tweets()

    def preload_tweets(self):
        """Preload previously seen tweets from a text file.

    
    Returns:
    A set() containing all the numeric 'id' attributes of tweets we have
    already seen.
    """
        
        if not os.path.isfile(self.out_file_name_ids):
            return set()

        else:
            try:
                seen = set()

                filename_o=open(self.out_file_name_ids)
                # print filename
                for k in filename_o:
                    # print k
                    try:
                        kk=json.loads(k)

                        seen.add(kk)
                    except Exception, e:
                        print e
                        print 'Minor Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        continue
                    
            except Exception, e:
                seen = set() # Avoid returning partial results on error
                print len(seen),e
                print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        filename_o.close()
        return seen


    def search(text,args, max_pages=10, results_per_page=100,sin_id=None):#,args.auth,args.auth_dict):
        """Generator for searching 'text' in Twitter content

    Search the public Twitter timeline for tweets matching a 'text' string,
    which can also be a hash tag, and yield a batch of matched tweets every
    time we have some results.

    Args:
    text str, the text to search for in Twitter. This can
    be a plain text string or a '#hashtag' to look
    for tweets of this topic only.
    max_pages int, maximum number of result 'pages' to obtain
    from Twitter's backlog of archived tweets. When
    not specified, default to 10 pages.
    results_per_page int, maximum number of results per page to fetch
    from Twitter's backlog of archived tweets. When
    not specified, default to 100 tweets per page.

    Returns:
    An array of dicts. Every dict in the returned array is a 'result' from
    twitter.Twitter.search and represents a single tweet.
    """
        credentials=load_login_cred(args)#.auth,args.auth_dict)
        if 'CONSUMER_KEY' in credentials:
            auth=login(credentials)
        else:
            credentials=credentials[credentials.keys()[0]]
            auth=login(credentials)

        while True:

            for page in range(1, max_pages + 1):
                print MAX_ID,'================'
                yield auth.GetSearch(term=text,until=sin_id,count=results_per_page,max_id=MAX_ID)

    def preload_tweets(filename):
        """Preload previously seen tweets from a text file.

    Args:
    filename str, Name of the file where we preload tweets from.

    Returns:
    A set() containing all the numeric 'id' attributes of tweets we have
    already seen.
    """
        if not filename:
            return set()
        try:
            seen = set()
            filename_o=open(filename)

            for k in filename_o:

                try:
                    kk=json.loads(ast.literal_eval(k))
                    for key, value in kk.iteritems():

                        if key=='id':
                            # print key
                            iid=value

                    seen.add(iid)
                except Exception, e:
                    print e
                    continue
                
        except Exception, e:
            seen = set() # Avoid returning partial results on error
            print len(seen),e
        return seen

    def streamsearch(ofile, text,args, max_pages=2000, results_per_page=200,from_date=FROM_DATE):
        """Stream the results of searching for 'text' to the 'ofile' output file

    Args:
    ofile str, the name of a file where we will write any tweets
    we find. Tweets are written in JSON format, with every
    tweet being stored in a separate line as a Python dict.
    text str, the text to search for in Twitter. This can
    be a plain text string or a '#hashtag' to look
    for tweets of this topic only.
    max_pages int, maximum number of result 'pages' to obtain
    from Twitter's backlog of archived tweets. When
    not specified, default to 10 pages.
    results_per_page int, maximum number of results per page to fetch
    from Twitter's backlog of archived tweets. When
    not specified, default to 100 tweets per page.

    Returns:
    None
    """
        # Load the id of already seen tweets, if there are any.
        global MAX_ID
        ofilename = ofile or 'standard output'
        seen = ofile and preload_tweets(ofile) or set()

        # from_date=FROM_DATE
        if seen:
            print '%d tweets preloaded from %s', len(seen), ofilename
        try:
            ostream = ofile and file(ofile, 'a+') or sys.stdout
            u=0
            for matches in search(text,args, max_pages=max_pages, sin_id=from_date,
                                  results_per_page=results_per_page):#,args.auth,args.auth_dict):
                
                u+=1
                newmatches = 0
                uu=0
                for tweet in matches:
                    # print uu
                    uu+=1
                
                    (tid, tuser, text, cr_at) = (tweet.GetId() ,tweet.GetUser(),
                                          tweet.GetText(), tweet.GetCreatedAt()) #['id'], ['from_user'] ['text']
                    tweet=tweet.AsJsonString()
                    # print tid,cr_at
                    if not tid in seen:
                        newmatches += 1
                        seen.add(tid)
                        print >> ostream, json.dumps(tweet)
                 
                if newmatches > 0:
                    print '%d new tweets logged at %s' %(newmatches, ofilename)
                print u,len(matches),'aa',MAX_ID,cr_at
                MAX_ID=tid
                
            ostream.close()
                
        except IOError, e:
            if ostream and ostream != sys.stdout:
                ostream.close()
            print 'Error writing at file "%s". %s' %(ofilename, e)
        

# FROM_DATE=None#'2015-01-15'
# MAX_ID=None




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=(
        'Collect tweets matching a text pattern and store them'
    'continuously in JSON-formatted lines of a local file.'))
    parser.add_argument('-o', '--output',nargs='?', metavar='Output FILE', type=str,
        default='Out_json', help='output folder name')
    parser.add_argument('-s', '--search',nargs='?', metavar='Search term', type=str,
        default=None, help='Search term')

    parser.add_argument('-c', '--auth_dict',nargs='?', metavar='credentials dict', type=str,
        default=None, help='credentials dictionary file name') 
    parser.add_argument('-d', '--auth',nargs='?', metavar='credentials file', type=str,
        default=None, help='credentials file name') 
    argsr = parser.parse_args()
    filedir=argsr.output
    try:
        os.stat(filedir)
    except:
        os.mkdir(filedir)
    filenam=argsr.search
    filename=''
    for l in filenam.split():
        filename+=l+'_'

    json_filename = filename[:-1]+'.json' # Where to store matching tweets
    lookup_text = unicode(argsr.search,'utf-8')# Text to search for

    outfile_name = os.path.join('%s' % filedir,json_filename)
   
    while True:
        try:
            streamsearch(outfile_name, lookup_text,argsr)#,maid_id=maid)
        except twitter.TwitterError, e:
            print 'Skipping HTTP error %s [...]' %str(e).split('\n')[0]
            time.sleep(900)

            pass
