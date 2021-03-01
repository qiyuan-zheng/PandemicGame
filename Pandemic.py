import networkx as nx

network=nx.Graph()

network.add_node("Atlanta")
network.add_node("Chicago")
network.add_node("Washington")
network.add_node("New York")
network.add_node("Montreal")
network.add_node("San Francisco")
network.add_node("London")
network.add_node("Madrid")
network.add_node("Essen")
network.add_node("St. Petersburg")
network.add_node("Milan")
network.add_node("Paris")

network.add_node("Miami")
network.add_node("Mexico City")
network.add_node("Los Angeles")
network.add_node("Bogota")
network.add_node("Lima")
network.add_node("Santiago")
network.add_node("Buenos Aires")
network.add_node("Sao Paolo")
network.add_node("Kinshasa")
network.add_node("Lagos")
network.add_node("Khartoum")
network.add_node("Johannesburg")

network.add_node("Cairo")
network.add_node("Istanbul")
network.add_node("Moscow")
network.add_node("Baghdad")
network.add_node("Riyadh")
network.add_node("Karachi")
network.add_node("Chennai")
network.add_node("Mumbai")
network.add_node("Kolkatta")
network.add_node("Delhi")
network.add_node("Algiers")
network.add_node("Tehran")

network.add_node("Sydney")
network.add_node("Jakarta")
network.add_node("Manilla")
network.add_node("Ho Chi Minh City")
network.add_node("Bangkok")
network.add_node("Hong Kong")
network.add_node("Beijing")
network.add_node("Shanghai")
network.add_node("Tokyo")
network.add_node("Taipei")
network.add_node("Seoul")
network.add_node("Osaka")

print("Number of Cities: ",str(len(network.nodes())))

#blue edges
network.add_edge("Atlanta","Chicago")
network.add_edge("Atlanta","Washington")
network.add_edge("Atlanta","Miami")
network.add_edge("Chicago","Mexico City")
network.add_edge("Chicago","Los Angeles")
network.add_edge("Chicago","San Francisco")
network.add_edge("Chicago","Montreal")
network.add_edge("Washington","New York")
network.add_edge("Washington","Miami")
network.add_edge("Washington","Montreal")
network.add_edge("New York","Montreal")
network.add_edge("New York","Madrid")
network.add_edge("London","New York")
network.add_edge("London","Madrid")
network.add_edge("London","Essen")
network.add_edge("London","Paris")
network.add_edge("Madrid","Sao Paolo")
network.add_edge("Madrid","Paris")
network.add_edge("Madrid","Algiers")
network.add_edge("San Francisco","Los Angeles")
network.add_edge("San Francisco","Tokyo")
network.add_edge("San Francisco","Manilla")
network.add_edge("Paris","Milan")
network.add_edge("Paris","Essen")
network.add_edge("Paris","Algiers")
network.add_edge("Essen","St. Petersburg")
network.add_edge("Essen","Milan")
network.add_edge("St. Petersburg","Moscow")
network.add_edge("St. Petersburg","Istanbul")

#yellow edges
network.add_edge("Miami","Mexico City")
network.add_edge("Miami","Bogota")
network.add_edge("Bogota","Lima")
network.add_edge("Bogota","Mexico City")
network.add_edge("Bogota","Sao Paolo")
network.add_edge("Bogota","Buenos Aires")
network.add_edge("Lima","Mexico City")
network.add_edge("Lima","Santiago")
network.add_edge("Buenos Aires","Sao Paolo")
network.add_edge("Lagos","Sao Paolo")
network.add_edge("Lagos","Kinshasa")
network.add_edge("Lagos","Khartoum")
network.add_edge("Khartoum","Johannesburg")
network.add_edge("Khartoum","Kinshasa")
network.add_edge("Khartoum","Cairo")
network.add_edge("Los Angeles","Sydney")
network.add_edge("Los Angeles","Mexico City")

#black edges
network.add_edge("Algiers","Istanbul")
network.add_edge("Algiers","Cairo")
network.add_edge("Istanbul","Moscow")
network.add_edge("Istanbul","Baghdad")
network.add_edge("Istanbul","Cairo")
network.add_edge("Baghdad","Tehran")
network.add_edge("Baghdad","Karachi")
network.add_edge("Baghdad","Cairo")
network.add_edge("Baghdad","Riyadh")
network.add_edge("Tehran","Moscow")
network.add_edge("Tehran","Delhi")
network.add_edge("Tehran","Karachi")
network.add_edge("Riyadh","Cairo")
network.add_edge("Karachi","Riyadh")
network.add_edge("Karachi","Mumbai")
network.add_edge("Karachi","Delhi")
network.add_edge("Mumbai","Delhi")
network.add_edge("Mumbai","Chennai")
network.add_edge("Delhi","Kolkatta")
network.add_edge("Delhi","Chennai")
network.add_edge("Kolkatta","Hong Kong")
network.add_edge("Kolkatta","Bangkok")
network.add_edge("Chennai","Kolkatta")
network.add_edge("Chennai","Jakarta")
network.add_edge("Chennai","Bangkok")

#red edges
network.add_edge("Jakarta","Sydney")
network.add_edge("Jakarta","Ho Chi Minh City")
network.add_edge("Jakarta","Bangkok")
network.add_edge("Bangkok","Ho Chi Minh City")
network.add_edge("Bangkok","Hong Kong")
network.add_edge("Hong Kong","Ho Chi Minh City")
network.add_edge("Hong Kong","Manilla")
network.add_edge("Hong Kong","Taipei")
network.add_edge("Hong Kong","Shanghai")
network.add_edge("Sydney","Manilla")
network.add_edge("Manilla","Ho Chi Minh City")
network.add_edge("Manilla","Taipei")
network.add_edge("Taipei","Osaka")
network.add_edge("Taipei","Shanghai")
network.add_edge("Shanghai","Tokyo")
network.add_edge("Shanghai","Seoul")
network.add_edge("Shanghai","Beijing")
network.add_edge("Tokyo","Osaka")
network.add_edge("Tokyo","Seoul")
network.add_edge("Seoul","Beijing")

print("Number of Connections: ",str(len(network.edges())))


###Compute centralities###

def compute_dc(G):
    """
    G: Graph
    return: dict, a map between each node to its degree centrality
    """
    acc={}
    for node in G.nodes:
        acc[node] = len([n for n in G.neighbors(node)])
    return acc


def compute_ec(G):
    """
    G: Graph
    return: dict, a map between each node to its eigenvector centrality
    values are rounded to 5 digits after the decimal point
    """

    n = len(G.nodes())

    # initial guess
    ec = {node: 1 for node in G.nodes() }

    # this is the maximum number of iterations we want to run
    # hopefully things will converge much faster
    for i in range(100):

        # new guess
        new_ec = ec.copy()

        # update
        for node in G.nodes():
            for nei in G.neighbors(node):
                new_ec[node] += ec[nei]

        # normalize
        sum_ecs = sum(new_ec.values())
        new_ec = {node: n*(new_ec[node] / sum_ecs) for node in G.nodes() }

        # calculate difference from previous solution
        diff = 0
        for node in G.nodes():
            diff += abs(ec[node] - new_ec[node])
        diff /= n

        # we have converged!
        if diff < 0.0001:
            break

        ec = new_ec.copy()

    
    return { node: round(new_ec[node],5) for node in G.nodes() }




def compute_bc(G):
    """
    G: Graph
    return: dict, a map between each node to its betweenness centrality
    """
    nodes=list(G.nodes())
    n=len(nodes)
    bc={node:0 for node in nodes}
    for source in range(n):
        sigma=[0 for t in range(n)]
        D=[-1 for i in range(n)]
        delta=[0 for t in range(n)]
        P=[[] for i in range(n)]
        S=[]
        Q=[source]
        D[source]=0
        sigma[source]=1
        while len(Q)>0:
            v=Q.pop(0)
            S+=[v]
            neis=list(G.neighbors(nodes[v]))
            for w in neis:
                if D[nodes.index(w)]==-1:
                    D[nodes.index(w)]=D[v]+1
                    Q+=[nodes.index(w)]
                if D[nodes.index(w)]==D[v]+1:
                    P[nodes.index(w)]+=[v]
                    sigma[nodes.index(w)]+=sigma[v]
        while len(S)>0:
            w=S.pop()
            for v in P[w]:
                delta[v]+= (sigma[v]/sigma[w])*(1+delta[w])
            if w!=source:
                bc[w]=bc[w]+delta[nodes.index(w)]
        
    return bc

print("The betweenness centrality for each city in the network: ",
      str(compute_bc(network)))

def BFS(G, source):

    n = len(G.nodes())
    
    visited = [ False for i in range(n) ]
    distances = [ -1 for i in range(n) ]
    
    visited[source] = True
    distances[source] = 0

    next_nodes = [ (source,0) ]

    while len(next_nodes) > 0:

        curr_node, curr_dist = next_nodes.pop(0)

        for nei in G.neighbors(curr_node):
            if not visited[nei]:
                visited[nei] = True
                distances[nei] = curr_dist + 1
                next_nodes+=[(nei,curr_dist+1)]
    return distances

def invert(l):
    acc=[]
    for item in l:
        if item==0:
            pass
        else:
            acc=acc+ [1/item]
    return acc
        
def compute_hc(G):
    """
    G: Graph
    return: dict, a map between each node to its harmonic centrality
    values are rounded to 5 digits after the decimal point
    """
    hcs={node:0 for node in G.nodes()}
    for node in G.nodes():
        dists=BFS(G,node)
        dists=invert(dists)
        hcs[node]=round((1/(len(G.nodes())-1))*sum(dists),5)
    return hcs

dc_list=[]
degs=compute_dc(network)
k=sorted(degs,key=degs.get,reverse=True)
for city in k:
    dc_list+=[(city,degs[city])]
print(dc_list)



ec_list=[]
x=compute_ec(network)
j=sorted(x, key=x.get,reverse=True)

for city in j:
    ec_list+=[(city, x[city])]
print(ec_list)

import random

pull_deck=k+6*["Epidemic Card"]+5*["Event Card"]












