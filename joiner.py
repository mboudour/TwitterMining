# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib
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
    return G,upp.nodes(),mid.nodes(),mapping_f.values()
def create_joint_hasht_retweet():
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
    nx.write_graphml(G,'joined_hasht_friends.graphm')

    return G,upp.nodes(),mid.nodes()
def create_joint_hasht_friends():
    G=nx.DiGraph()
    upp=nx.read_graphml('upperlevel_hashtags.graphml')
    for ed in upp.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2])
        G.add_edge(ed[1],ed[0],attr_dict=ed[2])
    down=nx.read_graphml('retweet.graphml')
    for ed in down.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2])
    inter=nx.read_graphml('interlevel_hashtags.graphml')
    for ed in inter.edges(data=True):
        G.add_edge(ed[0],ed[1],attr_dict=ed[2]) 
        G.add_edge(ed[1],ed[0],attr_dict=ed[2])
    nx.write_graphml(G,'joined_hasht_retweet.graphm')

    return G,upp.nodes(),down.nodes()

def create_node_conncomp_graph(G,layer1,layer2,layer3):
    # print layer1
    npartition = list(nx.weakly_connected_components(G))
    print len(npartition)
    # G=nx.Graph(G)
    layers={'layer1':layer1,'layer2':layer2,'layer3':layer3}
    broken_partition={}
    for i,v in enumerate(npartition):
        vs=set(v)
        for ii,vv in layers.items():
            papa=vs.intersection(set(vv))
            if len(papa)==len(v):
                broken_partition['a_%i_%s_s' %(i,ii)]=v
            elif len(papa)>0:
                broken_partition['b_%i_%s' %(i,ii)]=list(papa)
                vs=vs-set(vv)
    # print rbroken_partition
    broken_graph=nx.Graph()
    rbroken_partition=dict()
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green']))
    cl=dict()
    for i,v in broken_partition.items():
        name=i.split('_')
        for ii in v:
            # print ii
            rbroken_partition[ii]=i
        if name[-1]=='s':
            cl[name[1]]=colors.pop()
        elif name[0]=='b' and not cl.has_key(name[1]):
            cl[name[1]]=colors.pop()
    # print rbroken_partition
    for i,v in rbroken_partition.items():
        name=v.split('_')
        broken_graph.add_node(v,color=cl[name[1]])
        edg=G[i]
        # print edg
        for j in edg:
            if j not in broken_partition[v]:
                # print j
                if not broken_graph.has_edge(v,rbroken_partition[j]):
                    broken_graph.add_edge(v,rbroken_partition[j])
    
    return broken_graph,broken_partition,npartition
def create_node_comm_graph(G,layer1,layer2,layer3):
    import community as cm
    G=nx.Graph(G)
    partition = cm.best_partition(G)
    print len(set(partition.values()))
    layers={'layer1':layer1,'layer2':layer2,'layer3':layer3}
    broken_partition={}
    npartition={}
    for i,v in partition.items():
        if v not in npartition:
            npartition[v]=[i]
        else:
            npartition[v].append(i)
    for i,v in npartition.items():
        vs=set(v)
        for ii,vv in layers.items():
            papa=vs.intersection(set(vv))
            if len(papa)==len(v):
                broken_partition['a_%i_%s_s' %(i,ii)]=v
            elif len(papa)>0:
                broken_partition['b_%i_%s' %(i,ii)]=list(papa)
                vs=vs-set(vv)
    broken_graph=nx.Graph()
    rbroken_partition=dict()
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green']))
    cl=dict()
    for i,v in broken_partition.items():
        name=i.split('_')
        for ii in v:
            rbroken_partition[ii]=i
        if name[-1]=='s':
            cl[name[1]]=colors.pop()
        elif name[0]=='b' and not cl.has_key(name[1]):
            cl[name[1]]=colors.pop()
    for i,v in rbroken_partition.items():
        name=v.split('_')
        broken_graph.add_node(v,color=cl[name[1]])
        edg=G[i]
        # print edg
        for j in edg:
            # print j
            if j not in broken_partition[v]:
                # print j
                if not broken_graph.has_edge(v,rbroken_partition[j]):
                    broken_graph.add_edge(v,rbroken_partition[j])
    # npartition = list(nx.connected_components(G))
    for i in G.nodes():
        # attr=G.node[i]
        # print attr
        G.add_node(i,attr_dict=G.node[i],best_partition=partition[i])
        if i in layer1:
            G.add_node(i,attr_dict=G.node[i],layers_3='1')
        elif i in layer2:
            G.add_node(i,attr_dict=G.node[i],layers_3='2')
        else:
            G.add_node(i,attr_dict=G.node[i],layers_3='3')


    # rr=nx.attribute_assortativity_coefficient(G,'layers_3')
    # s_title='Assortativity_coef(3_layers)= %.2f' %rr
    # plt.title(s_title,{'size': '20'})

    return broken_graph,broken_partition,npartition#,G

def plot_graph_stack(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1,withlabels=False,edgelist=[],layout=True,alpha=0.5):
    # import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse, Polygon
    from collections import Counter
    import random
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]

    mlayer_part={}
    for i in broken_partition:
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])
    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v

    broken_pos={}
    mlayer_part={}
    for i in broken_partition:
        # print i.split('_')
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])

    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v
    singles=0
    for i,v in broken_partition.items():       
        name=i.split('_')
        if name[-1]=='s':
            singles+=1
        ndnd=random.choice(v)
        npos=pos[ndnd]
        if ndnd in layer1:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(broken_pos[i])
        elif ndnd in layer2:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]-d1)] 
            bottom_set.add(i)
            right.append(broken_pos[i])
        else:
            broken_pos[i]=[d2*npos[0],d2*(npos[1])] 
            middle_set.add(i)
            down.append(broken_pos[i])
    
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.-d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+d3]
    cleft = [max(xleft)+d1/2.-d4,min(yleft)-d1/2.+d3]
    dleft = [min(xleft)-d1/2.-d4,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.-d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+d3]
    cright = [max(xright)+d1/2.-d4,min(yright)-d1/2.+d3]
    dright = [min(xright)-d1/2.-d4,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.-d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+d3]
    cdown = [max(xdown)+d1/2.-d4,min(ydown)-d1/2.+d3]
    ddown = [min(xdown)-d1/2.-d4,min(ydown)-d1/2.-d3]
    nodesSizes=[]
    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')
   
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    nodesSizes=[i for i in nodeSize]
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    for nds in nodeSize:
        nodesSizes.append(nds)
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]
    for nds in nodeSize:
        nodesSizes.append(nds)
    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)

    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
    
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3)
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    # print G.nodes(data=True)
    # rr=nx.attribute_assortativity_coefficient(G,'asso')
    # print 'Attribute assortativity coefficient wrt layer partition (old)= %f' %orr
    nodesSizes=sorted(nodesSizes,reverse=True)
    title_s='%i weakly connected components (%i 3-layered, %i 2-layered, %i 1-layered)\n Sizes of 6 biggest weakly connected components:(%i,%i,%i,%i,%i,%i)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1],nodesSizes[0],nodesSizes[1],nodesSizes[2],nodesSizes[3],nodesSizes[4],nodesSizes[5])

    # title_s='%i connected components (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])  #  %(len(npartition),len(npartition)-singles,singles)
    plt.title(title_s,{'size': '20'})
    
    plt.axis('off')
    plt.show()
def plot_graph_stack_com(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1,withlabels=False,edgelist=[],layout=True,alpha=0.5):
    # import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse, Polygon
    from collections import Counter
    import random
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]

    mlayer_part={}
    for i in broken_partition:
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])
    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v

    broken_pos={}
    mlayer_part={}
    for i in broken_partition:
        # print i.split('_')
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])

    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v
    singles=0
    for i,v in broken_partition.items():       
        name=i.split('_')
        if name[-1]=='s':
            singles+=1
        ndnd=random.choice(v)
        npos=pos[ndnd]
        if ndnd in layer1:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(broken_pos[i])
        elif ndnd in layer2:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]-d1)] 
            bottom_set.add(i)
            right.append(broken_pos[i])
        else:
            broken_pos[i]=[d2*npos[0],d2*(npos[1])] 
            middle_set.add(i)
            down.append(broken_pos[i])
    
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.-d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+d3]
    cleft = [max(xleft)+d1/2.-d4,min(yleft)-d1/2.+d3]
    dleft = [min(xleft)-d1/2.-d4,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.-d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+d3]
    cright = [max(xright)+d1/2.-d4,min(yright)-d1/2.+d3]
    dright = [min(xright)-d1/2.-d4,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.-d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+d3]
    cdown = [max(xdown)+d1/2.-d4,min(ydown)-d1/2.+d3]
    ddown = [min(xdown)-d1/2.-d4,min(ydown)-d1/2.-d3]
    nodesSizes=[]
    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')
   
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    nodesSizes=[i for i in nodeSize]
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    for nds in nodeSize:
        nodesSizes.append(nds)
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]
    for nds in nodeSize:
        nodesSizes.append(nds)
    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)

    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
    
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3)
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    # print G.nodes(data=True)
    # rr=nx.attribute_assortativity_coefficient(G,'asso')
    # print 'Attribute assortativity coefficient wrt layer partition (old)= %f' %orr
    nodesSizes=sorted(nodesSizes,reverse=True)
    title_s='%i Communities (%i 3-layered, %i 2-layered, %i 1-layered)\n Sizes of 6 biggest Communities:(%i,%i,%i,%i,%i,%i)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1],nodesSizes[0],nodesSizes[1],nodesSizes[2],nodesSizes[3],nodesSizes[4],nodesSizes[5])

    # title_s='%i connected components (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])  #  %(len(npartition),len(npartition)-singles,singles)
    plt.title(title_s,{'size': '20'})
    
    plt.axis('off')
    plt.show()


G,layer1,layer2,layer3=create_joined_multigraph()
# G,layer1,layer2=create_joint_hasht_friends()
# G,layer1,layer2=create_joint_hasht_retweet()
# layer3=[]
# broken_graph,broken_partition,npartition=create_node_comm_graph(G,layer1,layer2,layer3)
broken_graph,broken_partition,npartition=create_node_conncomp_graph(G,layer1,layer2,layer3)
plot_graph_stack(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,layout=False)
broken_graph,broken_partition,npartition=create_node_comm_graph(G,layer1,layer2,layer3)
plot_graph_stack_com(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,layout=False)

# rr=nx.weakly_connected_components(G)
# # sr=nx.strongly_connected_components(G)
# # print len(rr),len(sr)
# for mm in rr:
#     print len(mm)
#     # print len(mm.nodes())
