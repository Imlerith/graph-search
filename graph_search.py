# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 06:40:06 2016

@author: nasekin
"""

# Graph optimization
# Finding shortest paths through MIT buildings

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graphs import * 

#
# Step 1: Building up the Campus Map
#


def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    mitmap = open(mapFilename)
#    for line in mitmap:
#        print line
            
    gg = WeightedDigraph()
    nodprs = []
    allnds = []
    for line in mitmap:
        nods = set([line.split()[0],line.split()[1]])
        nds  = [line.split()[0],line.split()[1]]
        dists = [line.split()[2],line.split()[3]]
        if nods not in nodprs:
#            ndsedgs = line.split()
            nodprs.append(nods)
            nd1 = Node(list(nds)[0])
            nd2 = Node(list(nds)[1])
            if nd1 not in allnds:
                allnds.append(nd1)
                gg.addNode(nd1)
            if nd2 not in allnds:
                allnds.append(nd2)
                gg.addNode(nd2)
            edg = WeightedEdge(nd1, nd2, dists[0], dists[1])
            gg.addEdge(edg)   
        else:
            nd1 = Node(list(nds)[0])
            nd2 = Node(list(nds)[1])
            edg = WeightedEdge(nd1, nd2, dists[0], dists[1])
            gg.addEdge(edg)
    print "Loading map from file..."
    return gg
    
     
#mitmap = open('mit_map.txt')
#
#for line in mitmap:
#    print line
        

#
# Step 2: Finding the Shortest Path using Brute Force Search
#
    
    
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    
    """Auxiliary recursive Depth-First-Search function to find candidate paths"""
    def dfs(digraph,start,end,maxTotalDist,maxDistOutdoors,disttot=0,distout=0,path=[],paths=[]):
            
        path = path + [start]
        print path, (disttot,distout)
        if start == end:
            paths.append([path,(disttot,distout)])
    
        for node, edg in zip(digraph.childrenOf(Node(start)),digraph.edges[Node(start)]):
            if node not in path:
                if disttot <= maxTotalDist and distout <= maxDistOutdoors:
                    dfs(digraph, node, end, maxTotalDist, maxDistOutdoors, disttot+edg[1][0], distout+edg[1][1], path, paths)   
                    
        return paths
        

    startA = Node(start)
    endA = Node(end)
    pths = dfs(digraph,startA,endA,maxTotalDist,maxDistOutdoors,disttot=0,distout=0,path=[],paths = []) 
    
    goodpths = []
    totdsts = []
    for pth in pths:
        if pth[1][0] <= maxTotalDist and pth[1][1] <= maxDistOutdoors:
            goodpths.append(pth)
            totdsts.append(pth[1][0])
            
    if goodpths == []:
        raise ValueError
    else:
        indmin = totdsts.index(min(totdsts))
        finpath = goodpths[indmin][0]    
        
        return map(str,finpath)
        

"""Step 3: Finding the Shortest Path using Directed Depth-First Search (DFS) approach:
   we do not want to travel down the path which is already longer than the shortest
   path found so far: this approach is more computationally efficient than brute force
"""
        
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first
    search approach. The total distance traveled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path
    must not exceed maxDistOutdoors.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    
    """Auxiliary recursive Depth-First-Search function to find candidate paths"""
    def dfs(digraph,start,end,maxTotalDist,maxDistOutdoors,disttot=0,distout=0,path=[],paths=[],shortest=None):
            
        path = path + [start]
        print path, (disttot,distout)
        if start == end:
            paths.append([path,(disttot,distout)])
            if shortest == None or len(path) < len(shortest):
                shortest = path
    
        for node, edg in zip(digraph.childrenOf(Node(start)),digraph.edges[Node(start)]):
            if node not in path:
                if disttot <= maxTotalDist and distout <= maxDistOutdoors and (shortest == None or len(path)<len(shortest)):
                    dfs(digraph, node, end, maxTotalDist, maxDistOutdoors, disttot+edg[1][0], distout+edg[1][1], path, paths,shortest)   
                    
        return paths
        

    startA = Node(start)
    endA = Node(end)
    pths = dfs(digraph,startA,endA,maxTotalDist,maxDistOutdoors,disttot=0,distout=0,path=[],paths = []) 
    
    goodpths = []
    totdsts = []
    for pth in pths:
        if pth[1][0] <= maxTotalDist and pth[1][1] <= maxDistOutdoors:
            goodpths.append(pth)
            totdsts.append(pth[1][0])
            
    if goodpths == []:
        raise ValueError
    else:
        indmin = totdsts.index(min(totdsts))
        finpath = goodpths[indmin][0]    
        
        return map(str,finpath)
    

#Testing the code
digraph = load_map('mit_map.txt')
path = directedDFS(digraph, '1', '10', 100, 100)

