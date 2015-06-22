# -*- coding: utf-8 -*-

__author__ = 'Moses Boudourides <moses.boudourides@gmail.com>, Sergios Lenis <sergioslenis@gmail.com>'
__coder__ ='Sergios Lenis <sergioslenis@gmail.com>'
import argparse
import datetime
import os
import glob
import pickle
import matplotlib.pyplot as plt
import random
import  json
import networkx as nx
import itertools as it

''' Run it with:
    python plots_ts.py -h to see the optional arguments
'''



def dir_search_trees(argsr):
    ''' 
    Search the directory for folder with the preprocessed files and returns the directories
    If --input is searching that it exist
    If --join only the folders of join
    ''' 

    dir_in_search_list=[]
    dir_search=os.getcwd()
    if argsr.input !=None:
        dir_in_search_list = [os.path.join('%s' % dir_search,argsr.input)]
        return dir_in_search_list
    else:
    # print dir_search
        for jj in os.listdir(dir_search):
            dir_in_search = os.path.join('%s' % dir_search,jj)
            try:
                # print os.listdir(dir_in_search)
                dir_in_search_dm=os.path.join('%s' % dir_in_search,'*.dmp')
                dmp_files = glob.glob(dir_in_search_dm)
                already_added=[]
                if len(dmp_files) == 0:
                    continue
                else:
                    if argsr.join !=None:
                        if jj in argsr.join:
                            dir_in_search_list.append(dir_in_search)
                    else:
                        dir_in_search_list.append(dir_in_search)
                    # print dmp_files
            except Exception, e:
                print e
        # if argsr.input !=None:

    return dir_in_search_list

def dic_operations(dir_search,argsr,ploted=False,bars=False):
    colors_lists=['k','c','m','g','r','b']
    colors_list=list(colors_lists)
    fi_li=[]
    lala=[]
    labels=dict()
    lalad=dict()
    for dirpath in dir_search:
        dir_in_search_dm=os.path.join('%s' % dirpath ,'*.dmp')
        dmp_files = glob.glob(dir_in_search_dm)
        file_name_of_direct=dirpath.split('/')[-1]
        print file_name_of_direct
        # print dmp_files
        already_added=[]
        if len(dmp_files) == 0:
            print 'a'
            continue
        if len(colors_list)>0:
            col=colors_list.pop()
            g=col+'o-'

        else:
            colors_list=list(colors_lists)
            col=colors_list.pop()
            g=col+'o.-'

        for fil in dmp_files:
            # print fil
            fi=fil.split('_')
            fic=fi[-1].split('.')
            if fic[0]=='count':
                ff=open(fil)
                created_at_count=pickle.load(ff)
                ff.close()
                fi_li.append(fi[0])
            elif fic[0]=='dic':
                ff=open(fil)
                created_at_dic=pickle.load(ff)
                ff.close()
            elif fic[0]=='has':
                ff=open(fil)
                hashtags_count=pickle.load(ff)
                ff.close()
            elif fic[0]=='json':
                ff=open(fil)
                json_dic=pickle.load(ff)
                ff.close()
            elif fic[0]=='word':
                ff=open(fil)
                text_list=pickle.load(ff)
                ff.close()
            elif fic[0]=='retId':
                ff=open(fil)
                retweeted_set=pickle.load(ff)
                ff.close()
            elif fic[0]=='retweet':
                ff=open(fil)
                retweet=pickle.load(ff)
                ff.close()

            elif fic[0]=='tjson':
                ff=open(fil)
                json_time_dic=pickle.load(ff)
                ff.close()
            elif fic[0]=='user':
                ff=open(fil)
                user_set=pickle.load(ff)
                ff.close()
            elif fic[0]=='userIdName':
                ff=open(fil)
                user_id_name=pickle.load(ff)
                ff.close()
            
            elif fic[0]=='upperlevel' and 'hasthtag' in argsr.hasthags_graph:
                ff=open(fil)
                upperlevel=pickle.load(ff)
                ff.close()
            elif fic[0]=='upperlevelterms' and 'terms' in argsr.hasthags_graph :
                ff=open(fil)
                upperlevel_terms=pickle.load(ff)
                ff.close()
            elif fic[0]=='interlevel' and 'hasthtag' in argsr.hasthags_graph:
                ff=open(fil)
                interlevel=pickle.load(ff)
                ff.close()
            elif fic[0]=='interlevelterms' and 'terms' in argsr.hasthags_graph :
                ff=open(fil)
                interlevel_terms=pickle.load(ff)
                ff.close()
            elif fic[0]=='barHas':
                ff=open(fil)
                bar_has=pickle.load(ff)
                ff.close()   
            
            else:
                print fil,'no'
        if ploted:        
            x=[]
            y=[]
            label_se=[]
            for i in sorted(created_at_count.keys()):
                x.append(i)
                y.append(created_at_count[i])
                if created_at_dic[i] in lala:
                    c=lalad[created_at_dic[i]]
                    if c>i:
                        labels[i]=created_at_dic[i]
                        lalad[created_at_dic[i]]=i
                        del labels[c]
                else:
                    labels[i]=created_at_dic[i]
                    lalad[created_at_dic[i]]=i
                    lala.append(created_at_dic[i])
            g=col+'o-'
            print fi[0]
            line, = plt.plot(x, y, g,label=fi[0])

            plt.xticks(labels.keys(), labels.values(), rotation=45)

        if argsr.userId:
            users=user_set.union(retweeted_set)
            notusers=retweeted_set.intersection(user_set)
            print len(notusers),'<=== mention users added'
            print len(users),'<=== Total users found'

            filedir=os.path.join('%s' % dirpath,'users')
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            dic_filename=file_name_of_direct +'_userset.dmp'
            print dic_filename
            outfile_name = os.path.join('%s' % filedir,dic_filename)
            ff=open(outfile_name,'w')
            pickle.dump(users,ff)
            ff.close()
            json_tname='user_list.txt'
            outfile=os.path.join('%s' % filedir,json_tname)
            ff=open(outfile,'w')
            for i in users:
                # print i,type(i)
                ff.write(str(i)+'\n')
            ff.close()



        if argsr.writing:
            G=nx.DiGraph()
            for dd in json_time_dic:
                if dd[1] not in already_added:

                    filedir=filedir=os.path.join('%s' % dirpath,'time_jsons')
                    already_added.append(dd[1])
                try:
                    os.stat(filedir)
                except:
                    os.mkdir(filedir)

                json_tname=dd[1]+'_.json'
                outfile=os.path.join('%s' % filedir,json_tname)
                ostream = outfile and file(outfile, 'a+') or sys.stdout
                for kk in json_time_dic[dd]:
                    print >> ostream, json.dumps(kk)
                ostream.close()
            filedir=os.path.join('%s' % dirpath,'graphmls')
                # already_added.append(dd[1])
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)

            json_tname='retweet.graphml'
            outfile=os.path.join('%s' % filedir,json_tname)
            # ostream = outfile and file(outfile, 'a+') or sys.stdout
            for tt in retweet:
                for rtee in tt[1]:
                    if G.has_edge(rtee,tt[0]):
                        wei=G[rtee][tt[0]]['weight']
                    else:
                        wei =0

                    G.add_edge(rtee,tt[0],weight= wei+1)
            nx.write_graphml(G,outfile)

            F=nx.Graph()

            if 'hasthtag' in argsr.hasthags_graph :
                json_tname='interlevel_hashtags.graphml'
                outfile=os.path.join('%s' % filedir,json_tname)
                for user_id in interlevel:
                    for hastt in interlevel[user_id]:
                        for hasht in hastt:
                            if interlevel[user_id][hasht]>0:
                                F.add_edge(user_id,hasht,weight=interlevel[user_id][hasht])
                nx.write_graphml(F,outfile)
            if 'terms' in argsr.hasthags_graph :
                json_tname='interlevel_terms.graphml'
                outfile=os.path.join('%s' % filedir,json_tname)
                for user_id in interlevel_terms:
                    for hasht in interlevel_terms[user_id]:
                        if interlevel_terms[user_id][hasht]>0:
                            F.add_edge(user_id,hasht,weight=interlevel_terms[user_id][hasht])
                nx.write_graphml(F,outfile)

            fg=nx.Graph()
            if 'hasthtag' in argsr.hasthags_graph :
                ffffff=open('out.tst','w')
                json_tname='upperlevel_hashtags.graphml'
                outfile=os.path.join('%s' % filedir,json_tname)
                for hs in it.combinations(upperlevel,2):
                    aa=upperlevel[hs[0]]
                    bb=upperlevel[hs[1]]
                    wei=set(aa).intersection(set(bb))
                    if len(wei)>0:
                        # fg.add_edge(hs[0],hs[1],weight=len(wei))
                        try:
                            ffffff.write(unicode(hs[0])+unicode(hs[1]))
                            fg.add_edge(unicode(hs[0]),unicode(hs[1]),weight=len(wei))
                        # print hs[0],hs[1]
                        except:
                            continue

                nx.write_graphml(fg,outfile)
            if 'terms' in argsr.hasthags_graph :
                json_tname='upperlevel_terms.graphml'
                print json_tname
                outfile=os.path.join('%s' % filedir,json_tname)
                for hs in it.combinations(upperlevel_terms,2):
                    aa=upperlevel_terms[hs[0]]
                    bb=upperlevel_terms[hs[1]]
                    wei=set(aa).intersection(set(bb))
                    if len(wei)>0:
                        fg.add_edge(unicode(hs[0]),unicode(hs[1]),weight=len(wei))
                nx.write_graphml(fg,outfile)

            if argsr.bars:
                # json_tname='Hashtags_Twitter_id.xtx'
                # outfile=os.path.join('%s' % filedir,json_tname)
                # print outfile,'fdskjllllla'
                # ostream = outfile and file(outfile, 'a+') or sys.stdout
                # f=open(outfile,'a')
                for i in bar_has:
                    print i,' ==> ',len(bar_has[i])
                    # print >> ostream, i ,' ==> ',len(bar_has[i])
                    # f.write(str(i)+' ==> '+str(bar_has[i]))
                # f.close()


            #     print >> ostream, json.dumps(tt)
            # ostream.close()

    if ploted:
        plt.legend()
        plt.show()

if __name__ == '__main__':
    # json_filename = None # The json to process
    # lookup_text = None # Text to search for

    # Parse command-line args for output file name.
    parser = argparse.ArgumentParser(description=(
        'Proccessing the temp file(s) and create the time jsons and word jsons'
        'and plot the timesequence or (and) the hashtags'))
    parser.add_argument('-o', '--output',nargs='?', metavar='Output FILE', type=str,
        default=None, help='output folder name')
    parser.add_argument('-i', '--input',nargs='*', metavar='Input FILE', type=str,
        default=None, help='input folder name')
    parser.add_argument('-p', '--plot',nargs='?', metavar='Ploting seq', type=bool,
        default=False, help='ploting the tweets per sequence')
    parser.add_argument('-b', '--bars',nargs='?', metavar='plot bars', type=bool,
        default=False, help='bar plot enable')
    parser.add_argument('-w', '--writing',nargs='?', metavar='writing json graph', type=bool,
        default=True, help='writing json files and graph enable')
    parser.add_argument('-j', '--join',nargs='*', metavar='Join FILES', type=str,
        default=None, help='join files with names')
    parser.add_argument('-u', '--userId',nargs='?', metavar='Write users', type=bool,
        default=True, help='Write the list of users Id')
    parser.add_argument('-ht', '--hasthags_graph',nargs='+', metavar='hasthtags or terms', type=str,
        default='hasthtags', help='Create the hashtags or terms upperlevel interlevel graphs')
    argsr = parser.parse_args()
    print argsr
    # print aaaa
    if argsr.plot == False:
        ploting=False
    else:
        ploting=True
    if argsr.bars==False:
        bar_plot=False
    else:
        bar_plot=True
    dir_in_search_list=[]
    # print ploting,bar_plot
    dir_in_search_list=dir_search_trees(argsr)
    if len(dir_in_search_list)==0:
        print 'No folders found exiting...'
        quit()
    # print dir_in_search_list
    # print aaa
    dic_operations(dir_in_search_list,argsr,ploted=ploting,bars=bar_plot)