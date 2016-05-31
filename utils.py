import pandas as pd
from collections import Counter

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

def prepare_plot_ids(pdf,val,time_freq='D',query_count=None):

    ss=pd.DataFrame({'count':pdf.groupby([pd.Grouper(key='date_split',freq=time_freq),val]).size()}).reset_index()
    if query_count!=None:
        query='count >= %i' %query_count
        ss=ss.query(query)
    ssp=ss.pivot(index='date_split',columns=val,values='count').fillna(0).reset_index()
    sps=ssp.to_dict()
    nsps=create_beaker_com_dict(sps)
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

def most_common_of(pdf,val,httoadd=[],counts=10):

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
    # print htcoun.most_common(10)
    httoaddc=[i[0] for i in htcoun.most_common(10)]
    httoaddc

    for i in httoaddc:
        httoadd.append(i)
    httoaddss=list(set(httoadd))
    return httoaddss

def prepare_plots_for_htmn(hpdf,val,httoaddc,time_freq='D'):

    def search_in_list_lists(x,name,columnname):
        l=x[columnname]
        if any([name in i for i in l]):
            return 1
        else: 
            return 0
    def add_column(x,name,namelist):
        return search_in_list_lists(x,name,namelist)  

    for name in httoaddc:
        hpdf[name]=hpdf.apply(add_column,args=(name,'hashtags'),axis=1)
    ss=hpdf.groupby('date_split').sum().reset_index()
    dic={nam+'_count':hpdf.groupby([pd.Grouper(key='date_split',freq=time_freq),nam]).size() for nam in httoaddc}
    hss=pd.DataFrame(dic).reset_index()
    hss.rename(columns = {'level_0':'date_split'}, inplace = True)
    hss.fillna(0,inplace=True)
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
    return nsps