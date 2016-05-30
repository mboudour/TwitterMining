import pandas as pd

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