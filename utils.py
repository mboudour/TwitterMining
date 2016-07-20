import pandas as pd
from collections import Counter
import itertools as it
import networkx as nx
import math

def create_beaker_com_dict(sps,time_freq='D'):
    nsps={}
    for k,v in sps.items():
        nsps[k]=[]
        if k=='date_split':
            for kk in sorted(v.keys()):
                if time_freq=='D':
                    nsps[k].append(v[kk].strftime('%Y%m%d'))
                elif time_freq=='H':
                    nsps[k].append(v[kk].strftime('%Y%m%d %H:%M:%S'))
        else:
            for kk in sorted(v.keys()):
                nsps[k].append(v[kk])

    return nsps
def compare_val_with_tw(pdf,val,oval,time_freq='D',query_count=None):
    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    # print ss

    ssdss=ss.groupby('date_split')
    vold={'date_split':[],val:[],oval:[]}
    for v,k in ssdss:
        vold['date_split'].append(v.strftime('%Y%m%d'))
        
        vold[val].append(len(k[val].unique()))
        vold[oval].append(sum(k['count']))
    return vold

def compare_val_with(pdf,val,time_freq='D',query_count=None):
    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    # print ss

    ssdss=ss.groupby('date_split')
    vold={'date_split':[],val:[],'tweets':[]}
    for v,k in ssdss:
        vold['date_split'].append(v.strftime('%Y%m%d'))
        
        vold[val].append(sum(k['count']*k[val]))
        vold['tweets'].append(sum(k['count']))
        # vold[oval].append(sum(k['count']))
    return vold
def compare_val_for_ret(pdf,val,time_freq='D',query_count=None):
    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    # print ss

    ssdss=ss.groupby('date_split')
    vold={'date_split':[],'retweets':[]}
    for v,k in ssdss:
        vold['date_split'].append(v.strftime('%Y%m%d'))
        
        # vold[val].append(sum(k['count']*k[val]))
        vold['retweets'].append(sum(k['count']))
        # vold[oval].append(sum(k['count']))
    return vold

def prepare_plot_for(pdf,val,time_freq='D',query_count=None):
    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    ssp=ss.pivot(index='date_split',columns=val,values='count').fillna(0).reset_index()
    sps=ssp.to_dict()
    nsps=create_beaker_com_dict(sps)
    nk=nsps.keys()
    print len(nk)
    nsps['volume']=[]
    for i,v in enumerate(nsps['date_split']):
        vk=0
        for k in nk:
            if k !='date_split':
                vk+=nsps[k][i]
        nsps['volume'].append(vk)
    return nsps

def prepare_plot_ids(pdf,val,time_freq='D',query_count=None,verbo=False):

    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    if verbo:
        print 'done first'
    ssp=ss.pivot(index='date_split',columns=val,values='count').fillna(0).reset_index()
    if verbo:
        print 'done pivot'
    sps=ssp.to_dict()
    if verbo:
        print 'done dict'
    nsps=create_beaker_com_dict(sps)
    if verbo:
        print 'nsps'
    nk=nsps.keys()
    nsps['volume']=[]
    vold={}
    vold['date_split']=nsps['date_split']
    vold['volume']=[]
    for i,v in enumerate(nsps['date_split']):
        vk=0
        for k in nk:
            if k !='date_split':
                vk+=nsps[k][i]
        vold['volume'].append(vk)
    return vold
    # beaker.datid=vold
    # 
def search_in_list_lists(x,name,columnname):
    l=x[columnname]
    if any([name in i for i in l]):
        return True
    else: 
        return False

def most_common_of(pdf,val,httoadd=[],counts=10,verbo=False):

    htdic=pdf[val].tolist()
    # print len(htdic)
    # print aa
    ll=[]
    # tes=5000
    # u=0
    for l in htdic:
        # print l
        for li in l:
            ll.append(li)

    htcoun=Counter(ll)
    if verbo:
        # for k in sorted(htcoun,key=htcoun.get,reverse=True):
        #     print k,htcoun[k]
        print 'Total number of hashtags:%i' %len(htcoun)

    # print htcoun.most_common(10)
    httoaddc=[i[0] for i in htcoun.most_common(counts)]
    print httoaddc

    for i in httoaddc:
        httoadd.append(i)
    httoaddss=list(set(httoadd))
    return httoaddss,htcoun

def prepare_plots_for_htmn(hpdf,val,httoaddc,char_to_add='#',time_freq='D'):

    def search_in_list_lists(x,name,columnname):
        l=x[columnname]
        if any([name in i for i in l]):
            return 1
        else: 
            return 0
    def add_column(x,name,namelist):
        return search_in_list_lists(x,name,namelist)  

    for name in httoaddc:
        hpdf[name]=hpdf.apply(add_column,args=(name,val),axis=1)
        # hpdf.loc[:,name]=hpdf.apply(add_column,args=(name,val),axis=1)

    ss=hpdf.groupby('date_split').sum().reset_index()
    dic={char_to_add+nam:hpdf.groupby([pd.Grouper(key='date_split',freq=time_freq),nam]).size() for nam in httoaddc}
    hss=pd.DataFrame(dic).reset_index()
    print hss.columns
    if 'level_0' in hss:
        hss.rename(columns = {'level_0':'date_split'}, inplace = True)
    hss.fillna(0,inplace=True)
    if 'level_1' in hss:
        dic=hss[hss['level_1']==1].to_dict()
        nsps={}
        for k,v in dic.items():
            if k!='level_1':
                nsps[k]=[]
            if k=='date_split':
                for kk in sorted(v.keys()):
                    nsps[k].append(v[kk].strftime('%Y%m%d'))
            elif k!='level_1':
                for kk in sorted(v.keys()):
                    nsps[k].append(v[kk])
    else:
        mcol=None
        for col in list(hss.columns):
            if col!='date_split':
                if char_to_add not in col:
                    if mcol==None:
                        mcol=col
                    else:
                        print mcol
                        print col
                        print aaaa
                        
        dic=hss[hss[mcol]==1].to_dict()
        nsps={}
        for k,v in dic.items():
            if k==mcol:
                print k,v
            if k!=mcol:
                nsps[k]=[]
            if k=='date_split':
                for kk in sorted(v.keys()):
                    nsps[k].append(v[kk].strftime('%Y%m%d'))
            elif k!=mcol:
#                 print k,v
#                 print aaa
                for kk in sorted(v.keys()):
                    nsps[k].append(v[kk])
    return nsps

def prepare_plots_for_htmn_one(hpdf,val,httoaddc,char_to_add='#',time_freq='D'):
    if len(httoaddc)>1:
        print 'List must contain only one hashtag!!!!'
        print aaaaaaaaaaaa

    def search_in_list_lists(x,name,columnname):
        l=x[columnname]
        if any([name in i for i in l]):
            return 1
        else: 
            return 0
    def add_column(x,name,namelist):
        return search_in_list_lists(x,name,namelist)  

    for name in httoaddc:
        hpdf[name]=hpdf.apply(add_column,args=(name,val),axis=1)
    ss=hpdf.groupby('date_split').sum().reset_index()
    dic={char_to_add+nam:hpdf.groupby([pd.Grouper(key='date_split',freq=time_freq),nam]).size() for nam in httoaddc}
    hss=pd.DataFrame(dic).reset_index()
    # print hss.columns
    hss.rename(columns = {'level_0':'date_split'}, inplace = True)
    hss.fillna(0,inplace=True)
    dic=hss[hss[httoaddc[0]]==1].to_dict()
    nsps={}
    for k,v in dic.items():
        if k!=httoaddc[0]:
            nsps[k]=[]
        if k=='date_split':
            for kk in sorted(v.keys()):
                nsps[k].append(v[kk].strftime('%Y%m%d'))
        elif k!=httoaddc[0]:
            for kk in sorted(v.keys()):
                nsps[k].append(v[kk])
    return nsps
# 
# Graphs
# 
def create_conc_graph_for_ligh(pdf):
    hastg=pdf.hashtags.tolist()
    usernames=pdf.username.tolist()
    isl=pdf['id'].tolist()
    G=nx.Graph()
    for i,hss in enumerate(hastg):
    #     print l,type(l)
    #     hss=json.loads(l)
        if isinstance(hss,list):
            if len(hss)>1:
                for ii in it.combinations(hss,2):
                    edg=tuple(sorted(ii))
                    if G.has_edge(edg[0],edg[1]):
                        wei =G[edg[0]][edg[1]]['weight']+1
                    else:
                        wei=1
                    G.add_edge(edg[0],edg[1],weight=wei)

    print len(G.nodes())
    print len(G.edges())
    return G

def get_nodes_to_keep(graph,weight_cut=0):
    # graph=G#nx.Graph(Gg)
    print len(graph.nodes()),'==>',
    noddd={}
    nod_to_keep=set()
    for i,nd in enumerate(graph.nodes()):
        noddd[nd]=i

        

    for edd in graph.edges():
    # for edd in graph_no_addr_ent.edges():
        if 'weight' in graph[edd[0]][edd[1]]:
            
    #     if 'weight' in graph_no_addr_ent[edd[0]][edd[1]]:
            wei=graph[edd[0]][edd[1]]['weight']
            if wei>=weight_cut:
                nod_to_keep.add(edd[0])
                nod_to_keep.add(edd[1])
            else:
                continue
    print len(nod_to_keep)
    print 'with cutoff = %i' %weight_cut
    return nod_to_keep

def pol_subj_for_plot(pdf,time_freq='D'):
    from textblob import TextBlob
    from textblob import Sentence
    spdf=pdf[['id','user_id','username','language','created_at','text','date_split']].reset_index()
    def sentim_sent(stri):
        try:
            tt=Sentence(stri).sentiment
        except Exception,e:
            tt=(None,None)
        return tt #[0],tt[1]

    spdf['polarity subjectivity']=spdf.text.apply(sentim_sent)#lambda x: Sentence(x).sentiment)
    spdf['polarity']=spdf['polarity subjectivity'].apply(lambda x: x[0])
    spdf['subjectivity']=spdf['polarity subjectivity'].apply(lambda x: x[1])
    spdf.dropna(axis=0,how='any', thresh=None, subset=['polarity','subjectivity'], inplace=True)
    # print spdf[pd.isnull(spdf.polarity) ]
    ss=spdf.groupby(pd.Grouper(key='date_split',freq=time_freq))
    ssd=ss['polarity'].mean().reset_index()
    pols=ssd.to_dict()
    nod_s={}
    for k,v in pols.items():
        if k=='date_split':
            vv=[ij.strftime('%Y%m%d') for ij in v.values()]
            nod_s['date_split']=vv
        else:
            key=k+'_average'
            nod_s[key]=v.values()
    sss=ss['subjectivity'].mean().reset_index()
    # print sss.columns
    subj=sss.to_dict()
    for k,v in subj.items():
        if k!='date_split':
            key=k+'_average'
            nod_s[key]=v.values()    
    mxs=ss['subjectivity'].max().reset_index()
    msub=mxs.to_dict()
    for k,v in msub.items():
        if k!='date_split':
            key=k+'_max'
            nod_s[key]=v.values()
    mns=ss['subjectivity'].min().reset_index()
    msub=mns.to_dict()
    for k,v in msub.items():
        if k!='date_split':
            key=k+'_min'
            nod_s[key]=v.values()
    mxs=ss['polarity'].max().reset_index()
    msub=mxs.to_dict()
    for k,v in msub.items():
        if k!='date_split':
            key=k+'_max'
            nod_s[key]=v.values()
    mns=ss['polarity'].min().reset_index()
    msub=mns.to_dict()
    for k,v in msub.items():
        if k!='date_split':
            key=k+'_min'
            nod_s[key]=v.values()

    return nod_s,spdf



def create_centralities_list(G,maxiter=2000,pphi=5,centList=[]):
    if len(centList)==0:
        centList=['degree_centrality','closeness_centrality','betweenness_centrality',
    'eigenvector_centrality','katz_centrality','page_rank']
    cenLen=len(centList)
    valus={}
    # plt.figure(figsize=figsi)
    for uu,centr in enumerate(centList):
        if centr=='degree_centrality':
            cent=nx.degree_centrality(G)
            sstt='Degree Centralities'
            ssttt='degree centrality'
            valus[centr]=cent
        elif centr=='closeness_centrality':
            cent=nx.closeness_centrality(G)
            sstt='Closeness Centralities'
            ssttt='closeness centrality'
            valus[centr]=cent

        elif centr=='betweenness_centrality':
            cent=nx.betweenness_centrality(G)
            sstt='Betweenness Centralities'
            ssttt='betweenness centrality'
            valus[centr]=cent

        elif centr=='eigenvector_centrality':
            try:
                cent=nx.eigenvector_centrality(G,max_iter=maxiter)
                sstt='Eigenvector Centralities'
                ssttt='eigenvector centrality'
                valus[centr]=cent

            except:
                valus[centr]=None

                continue
        elif centr=='katz_centrality':
            phi = (1+math.sqrt(pphi))/2.0 # largest eigenvalue of adj matrix
            cent=nx.katz_centrality_numpy(G,1/phi-0.01)
            sstt='Katz Centralities'
            ssttt='Katz centrality'
            valus[centr]=cent

        elif centr=='page_rank':
            try:
                cent=nx.pagerank(G)
                sstt='PageRank'
                ssttt='pagerank'
                valus[centr]=cent

            except:
                valus[centr]=None

                continue
        print '%s done!!!' %sstt

    return valus