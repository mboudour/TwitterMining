# -*- coding: utf-8 -*-
import networkx as nx

def create_joined_multigraph():
    G=nx.DiGraph()
    upp=nx.read_graphml('upperlevel_hashtags.graphml')
    for ed in upp.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2])
        G.add_edge(ed[1],ed[0],attr_dict=ed[2])
    mid=nx.read_graphml('friendship_graph.graphml')
    for ed in mid.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2]) 
    inter=nx.read_graphml('interlevel_hashtags.graphml')
    for ed in inter.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2]) 
        G.add_edge(ed[1],ed[0],attr_dict=ed[2])
    down=nx.read_graphml('retweet.graphml')
    mapping_f={}
    for i,v in enumerate(down.nodes()):
        mapping_f[v]='%iretweet_net' %i
    for ed in down.edges(data=True):
        G.add_edge(mapping_f[ed[0]],mapping_f[ed[1]],attr_dict=ed[2]) 

    for nd in mid.nodes():
        if nd in mapping_f:
            G.add_edge(nd,mapping_f[nd])
            G.add_edge(mapping_f[nd],nd)
    nx.write_graphml(G,'joined_3layerdigraph.graphm')
    return G
G=create_joined_multigraph()
# rr=nx.weakly_connected_components(G)
# # sr=nx.strongly_connected_components(G)
# # print len(rr),len(sr)
# for mm in rr:
#     print len(mm)
#     # print len(mm.nodes())
