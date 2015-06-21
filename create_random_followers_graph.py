# -*- coding: utf-8 -*-
__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"
import networkx as nx

def create_random_followers_graph(followers_list,fil=None):
    '''Creates a random_followers_graph with nodes the followers_list'''
    if fil==None:
        fil='random_followers_graph.graphml'
    n=len(followers_list)
    G=nx.gnc_graph(n)
    F=G.__class__()
    mapping_f={}
    for i,v in enumerate(followers_list):
        mapping_f[i]=v
    for edg in G.edges(data=True):
        F.add_edge(mapping_f[edg[0]],mapping_f[edg[1]],attr_dict=edg[2])
    for i in G.nodes():
        att=G.node[i]
        F.add_node(mapping_f[i], attr_dict=att)
    return F


# followers_list=['a','b','c','d','e']
# F=create_random_followers_graph(followers_list)
# print F.edges()
# print F.nodes()
