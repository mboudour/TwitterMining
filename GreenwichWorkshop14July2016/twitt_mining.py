
# coding: utf-8

# # Mining (together with a bit of web scraping) of large social networks from Twitter using Python (and Ruby)
# ## By Moses Boudourides and Sergios Lenis 
# ## University of Patras, Greece

import pandas as pd
import json 
import os
import imp


# !pip install python-twitter
# import twitter
input_dir='/home/mab/github_repos/TwitterMining'
output_dir='/home/mab/Desktop/twitTemp'
cred_dic='/home/mab/Desktop/twitTemp/credentials/auth_cred.txt'

# cred_dic=None

# pp = get_ipython().getoutput(u'pwd')
# os.chdir(input_dir)
# print os.getcwd()


from test_class_tpa import create_df
import collect_tweets_notebook as ctn

# os.chdir(pp[0])

def create_beaker_com_dict(sps):
    nsps={}
    for k,v in sps.items():
        nsps[k]=[]
        if k=='date_split':
            for kk in sorted(v.keys()):
                nsps[k].append(v[kk].strftime('%Y%m%d'))
        else:
            for kk in sorted(v.keys()):
                nsps[k].append(v[kk])

    return nsps

vv=ctn.UserAuth(auth_file=cred_dic)

vv.login()

vv.check_login()
twi_api=vv.get_auth()

search_term='@MediaGovGr'
sea=ctn.TwitterSearch(twi_api,search_text=search_term,working_path=output_dir,out_file_dir=None,
max_pages=10,results_per_page=100,sin_id=None,max_id=None,verbose=True)

sea.streamsearch()
