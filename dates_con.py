# -*- coding: utf-8 -*-
__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"
import argparse
import  json
import ast
from json import JSONDecoder
from functools import partial
import time
import datetime 
import pytz
import re
from dateutil import parser as par
from collections import Counter
import glob
import pickle
import os
import sys
import itertools as it

''' Run it with:
    python dates_con.py -i filename.json
    filename.json the json file(s) to be analized
    additional argumments can be found by python dates_con.py -h
'''



def json_cut_in_arg(fil,args):

    # print fil,args
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    words=args.words
    fifi=fil.split('_')

    utc = pytz.utc
    timtim=datetime.datetime(2015,1,01)
    filename_o=open(fil)
    u=0
    uu=0
    hashtags_dic=set()
    
    id_list=[]
    jfifi=None
    if args.join !=None:
        for ii in args.join:
            if ii in fifi[0]:
                jfifi=ii
# If multiple copies of a json
    if jfifi!=None:

        filedir=jfifi
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        # Loading if already saved
        try:
            dic_filename=jfifi+'_count.dmp'
            outfile_name = os.path.join('%s' % filedir,dic_filename)
            ff=open(outfile_name)
            created_at_count=pickle.load(ff)
            dic_user=jfifi+'_user.dmp'
            outfile_name = os.path.join('%s' % filedir,dic_user)
            ff=open(outfile_name)
            user_set=pickle.load(ff)
            ff.close()
            dic_filename=jfifi+'_dic.dmp'
            outfile_name = os.path.join('%s' % filedir,dic_filename)
            ff=open(outfile_name)
            created_at_dic=pickle.load(ff)
            ff.close()
            dic_filename=jfifi+'_has.dmp'
            outfile_name = os.path.join('%s' % filedir,dic_filename)
            ff=open(outfile_name)
            hashtags_count=pickle.load(ff)
            ff.close()
            json_name=jfifi+'_json.dmp'
            outfile_name = os.path.join('%s' % filedir,json_name)
            ff=open(outfile_name)
            json_dic=pickle.load(ff)
            ff.close()
            text_fname=jfifi+'_list_word.dmp'
            outfile_name = os.path.join('%s' % filedir,text_fname)
            ff=open(outfile_name)
            text_list=pickle.load(ff)
            ff.close()
            json_tname=jfifi+'_time_tjson.dmp'
            outfile_name = os.path.join('%s' % filedir,json_tname)
            ff=open(outfile_name)
            json_time_dic=pickle.load(ff)
            ff.close()
            jsont_retweet=jfifi+'_retweet.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            retweeted_dic=pickle.load(ff)
            ff.close()
            jsont_retweet=jfifi+'_retId.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            retweeted_set=pickle.load(ff)
            ff.close()
            jsont_retweet=jfifi+'_userIdName.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            user_id_name=pickle.load(ff)
            ff.close()
            jsont_retweet=jfifi+'_interlevel.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            interlevel=pickle.load(ff)
            ff.close()
            jsont_retweet=jfifi+'_barHas.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            bar_has=pickle.load(ff)
            ff.close()
            if words !=None:
                jsont_retweet=jfifi+'_interlevelterms.dmp'
                outfile_name = os.path.join('%s' % filedir,jsont_retweet)
                ff=open(outfile_name)
                interlevel_terms=pickle.load(ff)
                ff.close()
            jsont_retweet=jfifi+'_upperlevel.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name)
            upperlevel=pickle.load(ff)
            ff.close()
            if words !=None:
                jsont_retweet=jfifi+'_upperlevelterms.dmp'
                outfile_name = os.path.join('%s' % filedir,jsont_retweet)
                ff=open(outfile_name)
                upperlevel_terms=pickle.load(ff)
                ff.close()

            # retweeted_dic=Counter()
        # Initialiting as emptys
        except:
            created_at_dic=dict()
            user_set=set()
            created_at_count=Counter()
            hashtags_count=Counter()
            json_dic=dict()
            json_time_dic=dict()
            text_list=dict()
            retweeted_dic=[]
            mention_dic={}
            retweeted_set=set()
            user_id_name=dict()
            interlevel=dict()
            upperlevel=dict()
            bar_has=dict()
            if words !=None:
                upperlevel_terms=dict()
                interlevel_terms=dict()
    else:       
        created_at_dic=dict()
        created_at_count=Counter()
        user_set=set()
        hashtags_count=Counter()
        json_dic=dict()
        json_time_dic=dict()
        text_list=dict()
        retweeted_dic=[]
        mention_dic={}
        retweeted_set=set()
        user_id_name=dict()
        interlevel=dict()
        upperlevel=dict()
        bar_has=dict()
        if words !=None:
            upperlevel_terms=dict()
            interlevel_terms=dict()

        if args.output == None:
            filedir=fil[:-5]
        else:
            filedir=args.output
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
    for k in filename_o:

        t_list=[ 'created_at', 'hashtags', 'urls',  'retweeted', 'text' ]
        user_l=['name','id', 'location', 'time_zone']
        mli=['media_url']
        u+=1

        try:
            kk=json.loads(ast.literal_eval(k))
            # kk=json.loads(k)
            # for ke,ve in kk.items():
            #     print ke,ve
            # print 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
            # print kk
            rt_or=[]
            hasht=None
            text_set=None
            for key, value in kk.iteritems():

                if key=='id':
                    iid=value
                    
                if key=='created_at':
                    cr_at=value
                    t_list.remove(key)
                if key== 'hashtags':
                    hasht=value
                    t_list.remove(key)
                if key == 'urls':
                    urs=value
                    t_list.remove(key)
                if key== 'retweeted':
                    rtd=value
                    t_list.remove(key)
                if key== 'text':
                    tx=value
                    t_list.remove(key)
                if key== "user_mentions":

                    for cvc in value:
                        for cc,vv in cvc.iteritems():

                            if cc=='id':
                                rtid=vv
                                retweeted_set.add(vv)
                                rt_or.append(rtid)
                            if cc=='screen_name':
                                scnam=vv

                        user_id_name[scnam]=rtid

                    if words!=None:
                        keyk=None
                        text_set=set()
                        if len(words)>=2:
                            for wwordl in range(2,len(words)+1):
                                for ww in it.combinations(words,wwordl):
                                    for www in ww:
                                        wwww=' '+www.lower()+' '
                                        if wwww in tx.lower():
                                            text_set.add(www)
                        else:
                            ww=words[0]
                            if ' '+ww.lower()+' ' in tx.lower():
                                text_set.add(ww)
                        if len(text_set)>0:
                            keyk=tuple(sorted(text_set))

                            if keyk not in text_list :
                                text_list[keyk]=set()
                                text_list[keyk].add(k)
                            else:
                                text_list[keyk].add(k)
                if key == 'user':
                    for c,v in kk['user'].iteritems():
                        if c == 'name':
                            nam=v
                            user_l.remove(c)

                        if c== 'id' :

                            idc=v
                            user_l.remove(c)
                            user_set.add(idc)
                        if c == 'location':
                            lc=v
                            user_l.remove(c)
                        if c== 'time_zone':
                            tz=v
                            user_l.remove(c)
            if iid in id_list:
                continue
            else:
                # print rt_or
                user_id_name[nam]=idc
                id_list.append(iid)
                json_dic[iid]=k
                uu+=1

                if len(rt_or)>0:
                    retweeted_dic.append((idc,rt_or))
            if hasht!=None:
                
                if idc not in interlevel.keys():
                    interlevel[idc]=Counter()
                for hashtag in hasht:
                    if hashtag not in bar_has:
                        bar_has[hashtag]=[iid]
                    else:
                        bar_has[hashtag].append(iid)


                    interlevel[idc][tuple(hasht)]+=1
            if text_set !=None:
                if idc not in interlevel_terms.keys():
                    interlevel_terms[idc]=Counter()
                for txts in text_set:
                    interlevel_terms[idc][txts]+=1
                    if txts not in upperlevel_terms:
                        upperlevel_terms[txts]=[iid]
                    else:
                        upperlevel_terms[txts].append(iid)
                
            dates=args.Time
            dt_cr_at= par.parse(cr_at) 

            ssa=dt_cr_at.timetuple()
            if dates==None:
                tim=datetime.datetime(ssa.tm_year,ssa.tm_mon,ssa.tm_mday,ssa.tm_hour,ssa.tm_min,ssa.tm_sec)
                ddtat= 'Sec_'+str(ssa.tm_sec)+'_'+ str(ssa.tm_min)+'_'+ str(ssa.tm_hour)+'_' + str(ssa.tm_mday)+'_'+str(ssa.tm_mon)+'_'+str(ssa.tm_year)
            elif dates == 'Min':
                tim=datetime.datetime(ssa.tm_year,ssa.tm_mon,ssa.tm_mday,ssa.tm_hour,ssa.tm_min)
                ddtat=  'Min_'+str(ssa.tm_min)+'_'+ str(ssa.tm_hour)+'_' + str(ssa.tm_mday)+'_'+str(ssa.tm_mon)+'_'+str(ssa.tm_year)
            elif dates=='Hour':
                tim=datetime.datetime(ssa.tm_year,ssa.tm_mon,ssa.tm_mday,ssa.tm_hour)
                ddtat= 'Hour_'+str(ssa.tm_hour)+'_' + str(ssa.tm_mday)+'_'+str(ssa.tm_mon)+'_'+str(ssa.tm_year)
                
            elif dates=='Day':
                tim=datetime.datetime(ssa.tm_year,ssa.tm_mon,ssa.tm_mday)
                ddtat= 'Day_'+ str(ssa.tm_mday)+'_'+str(ssa.tm_mon)+'_'+str(ssa.tm_year)
            elif dates=='Month':
                tim=datetime.datetime(ssa.tm_year,ssa.tm_mon)
                ddtat= 'Month_'+ str(ssa.tm_mon)+'_'+str(ssa.tm_year)
            ttim =  tim -timtim    
            dtat=str(ssa.tm_mday)+' / '+str(ssa.tm_mon)
            created_at_count[ttim.total_seconds()]+=1
            created_at_dic[ttim.total_seconds()]=dtat
            if (ttim.total_seconds(),ddtat) not in json_time_dic.keys():
                json_time_dic[(ttim.total_seconds(),ddtat)]=[k]
            else:
                json_time_dic[(ttim.total_seconds(),ddtat)].append(k)


            if 'hashtags' not in t_list:

                for ha in hasht:
                    hashtags_dic.add(ha)

                    if ha not in upperlevel.keys():
                        upperlevel[ha]=[iid]
                    else: 
                        upperlevel[ha].append(iid)

                if len(hasht)>1:
                    hashtags_count[str(sorted(hasht))]+=1
        except Exception, e:
            print u,uu,fil,e

            continue
    print u,uu,len(created_at_count.keys()),'final'
    print len(hashtags_count.keys()),'<== hashtags'
    print len(json_dic.keys()),'<== Jsons'
    print len(retweeted_set),'retweet ids'

    print len(json_time_dic.keys()),'<== Time intervals'
    print len(text_list),'<== words found'
    if jfifi !=None:

        dic_filename=jfifi+'_dic.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        pickle.dump(created_at_dic,ff)
        ff.close()
        dic_filename=jfifi+'_count.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        pickle.dump(created_at_count,ff)
        ff.close()
        dic_filename=jfifi+'_has.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        
        pickle.dump(hashtags_count,ff)
        ff.close()

        json_name=jfifi+'_json.dmp'
        outfile_name = os.path.join('%s' % filedir,json_name)
        ff=open(outfile_name,'w')
        pickle.dump(json_name,ff)
        ff.close()
        text_fname=jfifi+'_list_word.dmp'
        outfile_name = os.path.join('%s' % filedir,text_fname)
        ff=open(outfile_name,'w')
        pickle.dump(text_list,ff)
        ff.close()
        # ff.close()
        json_tname=jfifi+'_time_tjson.dmp'
        outfile_name = os.path.join('%s' % filedir,json_tname)
        ff=open(outfile_name,'w')
        pickle.dump(json_time_dic,ff)
        ff.close()
        json_ret=jfifi+'_retweet.dmp'
        outfile_name = os.path.join('%s' % filedir,json_ret)
        ff=open(outfile_name,'w')
        pickle.dump(retweeted_dic,ff)
        ff.close()
        dic_user=jfifi+'_user.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_user)
        ff=open(outfile_name,'w')
        pickle.dump(user_set,ff)
        ff.close()
        jsont_retweet=jfifi+'_retId.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(retweeted_set,ff)
        ff.close()
        jsont_retweet=jfifi+'_userIdName.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(user_id_name,ff)
        ff.close()
        jsont_retweet=jfifi+'_interlevel.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(interlevel,ff)
        ff.close()
        jsont_retweet=jfifi+'_upperlevel.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(upperlevel,ff)
        ff.close()
        jsont_retweet=jfifi+'_barHas.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(bar_has,ff)
        ff.close()
        if words !=None:
            jsont_retweet=jfifi+'_upperlevelterms.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name,'w')
            pickle.dump(upperlevel_terms,ff)
            ff.close()

            jsont_retweet=jfifi+'_interlevelterms.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name,'w')
            pickle.dump(interlevel_terms,ff)
            ff.close()
    else:

        dic_filename=fil[:-5]+'_dic.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        pickle.dump(created_at_dic,ff)
        ff.close()
        dic_filename=fil[:-5]+'_count.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        pickle.dump(created_at_count,ff)
        ff.close()
        dic_filename=fil[:-5]+'_has.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_filename)
        ff=open(outfile_name,'w')
        
        pickle.dump(hashtags_count,ff)
        ff.close()
        json_name=fil[:-5]+'_json.dmp'
        outfile_name = os.path.join('%s' % filedir,json_name)
        ff=open(outfile_name,'w')
        pickle.dump(json_name,ff)
        ff.close()
        text_fname=fil[:-5]+'_list_word.dmp'
        outfile_name = os.path.join('%s' % filedir,text_fname)
        ff=open(outfile_name,'w')
        pickle.dump(text_list,ff)
        ff.close()
        json_tname=fil[:-5]+'_time_tjson.dmp'
        outfile_name = os.path.join('%s' % filedir,json_tname)
        ff=open(outfile_name,'w')
        pickle.dump(json_time_dic,ff)
        ff.close()

        json_ret=fil[:-5]+'_retweet.dmp'
        outfile_name = os.path.join('%s' % filedir,json_ret)
        ff=open(outfile_name,'w')
        pickle.dump(retweeted_dic,ff)
        ff.close()
        dic_user=fil[:-5]+'_user.dmp'
        outfile_name = os.path.join('%s' % filedir,dic_user)
        ff=open(outfile_name,'w')
        pickle.dump(user_set,ff)
        ff.close()
        jsont_retweet=fil[:-5]+'_retId.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(retweeted_set,ff)
        ff.close()
        jsont_retweet=fil[:-5]+'_userIdName.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(user_id_name,ff)
        ff.close()
        jsont_retweet=fil[:-5]+'_interlevel.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(interlevel,ff)
        ff.close()
        jsont_retweet=fil[:-5]+'_upperlevel.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(upperlevel,ff)
        ff.close()
        jsont_retweet=fil[:-5]+'_barHas.dmp'
        outfile_name = os.path.join('%s' % filedir,jsont_retweet)
        ff=open(outfile_name,'w')
        pickle.dump(bar_has,ff)
        ff.close()
        if words !=None:
            jsont_retweet=fil[:-5]+'_upperlevelterms.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name,'w')
            pickle.dump(upperlevel_terms,ff)
            ff.close()
            jsont_retweet=fil[:-5]+'_interlevelterms.dmp'
            outfile_name = os.path.join('%s' % filedir,jsont_retweet)
            ff=open(outfile_name,'w')
            pickle.dump(interlevel_terms,ff)
            ff.close()
    # print text_list.keys()

if __name__ == '__main__':

    # Parse command-line args for output file name.
    parser = argparse.ArgumentParser(description=(
        'Proccessing the json file(s) and cutting them in time sequences and'
        'or word(s) sequences'))
    parser.add_argument('-o', '--output',nargs='?', metavar='Output FILE', type=str,
        default=None, help='output file name')
    parser.add_argument('-i', '--input',nargs='*', metavar='Input FILE', type=str,
        default=None, help='input file name')
    parser.add_argument('-j', '--join',nargs='*', metavar='Join FILES', type=str,
        default=None, help='join files with names')
    parser.add_argument('-w','--words', nargs='*', metavar='Word(s) to search',type=str, default=None,
        help='Word(s) to search for in tweet content')
    parser.add_argument('-t','--Time', nargs='?', type=str, default='Day',
        help='time intervals can be ( Min Day Month Year)')
    args = parser.parse_args()
    # print args

    json_filename = args.input # json to process

    if json_filename == None:
        json_files = glob.glob('*.json')
        if len(json_files) == 0:
            raise RuntimeError('No json files to convert.')
        for fil in json_files:
            print fil
            json_cut_in_arg(fil,args)
    else:
        for ff in json_filename:
            json_cut_in_arg(ff,args)


