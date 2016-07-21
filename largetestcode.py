#!/usr/bin/env python
from graphdijkstra import Graph,dijkstra,shortest_path
import os, sys
import time
import subprocess
import platform

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
    time.sleep(0.1)
    clear()
    time.sleep(0.1)

def file_to_graph(file):
    edgefile = open(file+'.txt','r')
    node_set = set([])
    for line in edgefile:
        edge_list=[]
        word = ''
        for character in line:
            if(character == ' ' or character == '\n'):
                if(word != ''):
                    edge_list.append(word)
                    word=''
            else:
                word = word+character
        # print edge_list
        x=edge_list[0]
        y=edge_list[1]
        d=float(edge_list[2])
        if x not in node_set:
            graph.add_node(x)
            node_set = node_set.union(set([x]))
        if y not in node_set:
            graph.add_node(y)
            node_set = node_set.union(set([y]))
        graph.add_edge(x,y,d)
        # graph.add_edge(y,x,d)
    # print node_set
    edgefile.close()


if __name__ == '__main__':
    graph = Graph()
    file=raw_input("Enter the Large Test File Name :")
    file_to_graph(file)
    # open_file(file+'.txt')
    
    source=raw_input("Enter the Source :")
    target=raw_input("Enter the Target :")
    returned = shortest_path(graph, source, target)
    message = "Source:"+source+"\n"+"Target:"+target+"\n"+"Shortest Distance:"+str(returned[0])    
    # print 'Shortest Distance between %s and %s is: %d'%(source,target,returned[0])
    print message
    print 'The Path taken is: ',returned[1]