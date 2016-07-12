# -*- coding: utf-8 -*-
import json
import twi_stat_to_panda as tpa  
# import twi_stat_to_panda_p as tpp 
import pandas as pd
import glob
import sys
import os
def create_df(fildir,selt,outname,write_csv=False,multihas=False,r_or_p='ruby'):
    # print fildir
    # print selt
    # print outname
    os.chdir(fildir)

    json_files = glob.glob('*.json')
    if len(json_files) == 0:
        raise RuntimeError('No dump files to convert.')
    print json_files
    lol=[]
    seen=set()

    # fop = open('untitled.json')
    for filna in json_files:
        cos=400000
        tem=cos
        fop = open(filna)
        # fop = open('/home/sergios-len/Documents/W5/Palestine_israel/06/tweets_palestine_abbas_netanyahu_israel_gaza_hash.json')
        # fop =open('/home/sergios-len/Documents/W5/Palestine_israel/01/gaza_palestine_hamas_Operation%20Cast%20Lead_israel_hash.json')
        # fop=open('/home/mab/MEGA/ObamaCare_18102013.json')
        u=0
        for fo in fop:
            try:
                dici=json.loads(fo)
                # if selt=='p':
                    # print dici
                    # print type(dici)
                    # dici=json.loads(dici)
            except Exception,e:
                # print e
                continue
            
            if selt=='r':
                h,lolo=tpa.TweetToPandas(dici,r_or_p).as_dict_hash()
            elif selt=='p':
                h,lolo=tpp.TweetToPandas(dici,r_or_p).as_dict_hash()
            elif selt=='rr':
                h,lolo=tpa.TweetToPandas(dici,r_or_p).users_as_dict_hash()
            if multihas:
                h,lolo=tpa.TweetToPandas(dici,r_or_p).hsa_as_dic_hash()
                # print h
                # print lolo
                # print aaa
            # nlolo=dict(lolo)
                for hasht in h['hashtags']:
                    nlolo=dict(lolo)
                    nlolo['Hashtag']=hasht#.encode('utf-8')
                    lol.append(nlolo)
            # lolo['hashtags_list']=list(h['hashtags'])

            elif not multihas:
                if h == False or dici['id'] in seen:
                    continue


                lol.append(lolo)    
            #  


            seen.add(dici['id'])
            if u >=tem:
                print u
                # break
                # print aaaaa
                tem +=cos
            u+=1
        # print aaaaaa
        print len(lol)
        # print lol[-1]
        # print lol[-2]
        # print aaaa
    pdf=pd.DataFrame(lol)
    print pdf.columns
        # pdf['created_at']=pd.to_datetime(pdf['created_at'],format='%a %b %d %H:%M:%S +0000 %Y')
    if write_csv:
        pdf.to_csv(outname,header=True)
    return pdf,json_files
    # 
    # 
if __name__ == '__main__':
    print 'test_class_tpa is being run by itself'
    print sys.argv

    fildir=sys.argv[1]
    selt=sys.argv[2]
    outname=sys.argv[3]
    os.chdir(fildir)
    # json_files = glob.glob('*.json')
    # if len(json_files) == 0:
    #     raise RuntimeError('No dump files to convert.')
    create_df(fildir,selt,outname+'out.ccc')

else:
    print 'I am being imported from another module'
    # filedir='/home/sergios-len/MEGAsync Downloads/' #refugees_dic.json'
    # selt='p'
    # outname='/home/sergios-len/MEGAsync Downloads/'
    # create_df(filedir, selt, outname)

