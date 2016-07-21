#!/usr/bin/env python
import pydot
from winter import Graph,print_out
import os, sys
import time
import subprocess
import platform

# clears the terminal
def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

#opens a file
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
    time.sleep(0.1)
    clear()
    time.sleep(0.1)

#creates graph from dataset
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
        d1=float(edge_list[2])
        d2=float(edge_list[3])
        if x not in node_set:
            graph.add_node(x)
            node_set = node_set.union(set([x]))
        if y not in node_set:
            graph.add_node(y)
            node_set = node_set.union(set([y]))
        graph.add_edge(x,y,d1,d2)
        graph.add_edge(y,x,d1,d2)
    # print len(node_set)
    edgefile.close()
    return node_set

# creates graph for display from dataset using pydot library
def file_to_initial_graph(file):
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
        x=edge_list[0]
        y=edge_list[1]
        d1=edge_list[2]
        d2=edge_list[3]
        edge_info="weight1:"+d1+"\n"+"weight2:"+d2
        nodex=pydot.Node(x,style="filled",fillcolor="blue")
        nodey=pydot.Node(y,style="filled",fillcolor="blue")
        if x not in node_set:
            initial_graph.add_node(nodex)
            node_set = node_set.union(set([x]))
        if y not in node_set:
            initial_graph.add_node(nodey)
            node_set = node_set.union(set([y]))
        initial_graph.add_edge(pydot.Edge(nodex, nodey,label=edge_info))
    edgefile.close()

# creates final graph after optimization applied
def file_to_final_graph(file):
    edgefile = open(file+'.txt','r')
    node_set = set([])
    for line in edgefile:
        edge_list=[]
        word=''
        for character in line:
            if(character == ' ' or character == '\n'):
                if(word != ''):
                    edge_list.append(word)
                    word=''
            else:
                word = word+character
        x=edge_list[0]
        y=edge_list[1]
        d1=edge_list[2]
        d2=edge_list[3]
        nodex=pydot.Node(x,style="filled",fillcolor="blue")
        nodey=pydot.Node(y,style="filled",fillcolor="blue")
        edge_info="weight1:"+d1+"\n"+"weight2:"+d2
        
        if x in path_set:
            nodex=pydot.Node(x,style="filled",fillcolor="green")
        if y in path_set:
            nodey=pydot.Node(y,style="filled",fillcolor="green")
        if x not in node_set:
            final_graph.add_node(nodex)
            node_set = node_set.union(set([x]))
        if y not in node_set:
            final_graph.add_node(nodey)
            node_set = node_set.union(set([y]))
        
        if ((x in path_set) and (y in path_set)) :
            final_graph.add_edge(pydot.Edge(nodex, nodey,label=edge_info,color="green"))
        else:
            final_graph.add_edge(pydot.Edge(nodex, nodey,label=edge_info))
    edgefile.close()

#The main function of the code
if __name__ == '__main__':
    graph = Graph()
    while(True):
        try:
            file=raw_input("Enter the Test File Name :")
            open_file(file+'.txt')
            node_set = file_to_graph(file)
            break
        except Exception:
            print ("\n\n")
            print ("Invalid Entry. Try Again!")
            continue
        except KeyboardInterrupt:
            print ("\n\n")
            print "\n\nThank you! Hope you liked it."
            sys.exit()
    
    initial_graph = pydot.Dot(graph_type='graph',label="graph from "+file+".txt")
    file_to_initial_graph(file)
    initial_graph.write_png('initial.png')
    open_file('initial.png')

    # stores count of the iterations run by the program  
    count=1
    while(True):
        print ('Data Set used from:'+file+'.txt')
        try:
            source=raw_input("Enter the Source :")
            if source not in node_set:
                print "This node doesn't exist.Try Again!"
                print ("\n\n")
                continue
            target=raw_input("Enter the Target :")
            if target not in node_set:
                print "This node doesn't exist.Try Again!"
                print ("\n\n")
                continue
            if source == target:
                print "Don't choose the same node!Try Again"
                print ("\n\n")
                continue
            limit = raw_input("Enter the Limit on constraint:")
        except Exception:
            print "\n\nThank you! Hope you liked it."
            sys.exit()
        except KeyboardInterrupt:
            print "\n\nThank you! Hope you liked it."
            sys.exit()

        n = 100 #the increment factor taken default
        
        returned = print_out(graph, source, target, limit, n)

        if float(limit)<float(returned[1]) :
            print ("Path Not Possible")
            print ("\n\n")
            continue

        message="Source:"+source+"\n"+"Target:"+target+"\n"+"Optimal Distance:"+str(returned[0])+"\n"+"Oxygen used:"+str(returned[1])
        path_set = set(returned[2])
        
        final_graph = pydot.Dot(graph_type='graph',label=message)
        file_to_final_graph(file)
        final_graph.write_png('final'+str(count)+'.png')
        open_file('final'+str(count)+'.png')
        count = count+1        
        
        # all relevant details are displayed
        print 'Optimal Distance between %s and %s is: %s'%(source,target,str(returned[0]))
        print 'Oxygen Used: ',returned[1]
        print 'The Optimal Path taken is: ',returned[2]
        print ("\n\n")