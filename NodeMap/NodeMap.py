import numpy as np
import scipy as sp
import math
import copy
import random as rng
import json
import os

try:
    from NodeMap.Graph import Graph
except:
    from Graph import Graph

graphfile = 'NodeMap/module_graph.json'
capture = False
# ffmpeg -framerate 10 -i NodeMap/capture_local/graph_plot_%05d.png -b:v 100M NodeMap/capture_local/dev_timelapse.avi

try: 
    import matplotlib.pyplot as plt
except: # Temporary tkinter workaround
    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt

def RandomLayout(nodes, seed = False):
    if seed:
        rng.seed(a = seed)
    layout = []
    for i in range(len(nodes)):
        layout.append([1-2*rng.random(), 1-2*rng.random()])
    return layout

def PlotLayout(graph, layout, save_name = False):
    plt.clf()
    plt.scatter(*zip(*layout))
    for i in range(len(graph.labels)):
        plt.annotate(graph.labels[i], layout[i])
    for link in graph.links:
        source = link['Source']
        target = link['Target']
        link_line = [layout[source], layout[target]]
        plt.plot(*zip(*link_line))
    if save_name:
        # print('saving to: '+save_name)
        plt.savefig(save_name)
    else:
        plt.show()
    

def WriteGraph(links):
    filestream = open(graphfile, "w")
    filestream.truncate(0)
    filestream.write(json.dumps(links))

def ReadGraph():
    filestream = open(graphfile, "r")
    graph = Graph()
    graph.append(json.loads(filestream.read()), symmetric = True)

    return graph

def GenerateMap():
    graph = ReadGraph()
    layout = RandomLayout(graph.labels, seed = 1)
    loss_old = computeLossFunction(graph, layout)
    iterations = 500
    dots = 0
    for i in range(iterations):
        if(capture):
            PlotLayout(graph, layout, save_name='NodeMap/capture_local/graph_plot_'+str(i).zfill(5)+'.png')
        updateLayout(graph, layout, 5*10**-2)
        if dots < (i/iterations)*20:
            dots = dots + 1
            print('.', end = '', flush = True)
    if(capture):
        PlotLayout(graph, layout, save_name='NodeMap/capture_local/graph_plot_'+str(iterations).zfill(5)+'.png')
    output_name = 'NodeMap/Module_Map_local.png'
    PlotLayout(graph, layout, save_name=output_name)
    print(' Done!\n\nSaved map as: '+output_name)


###############################################################################
########################## LOSS FUNCTION COMPUTATION ##########################
###############################################################################

def computeLossFunction(graph, layout):
    loss = 0
    similarityNorm = 0
    for k in range(len(layout)):
        for l in range(len(layout)):
            if k != l:
                similarityNorm = similarityNorm + computeSimilarity(layout[k], layout[l])
    for source in range(len(graph.labels)):
        subG = graph.ExtractSubGraph(source)
        loss = loss + computeLossForSingleSource(subG, layout, similarityNorm)
    return loss

def computeSimilarity(v, u): # q_ij
	distSq = (v[0]-u[0])**2 + (v[1]-u[1])**2
	return 1.0 / (1.0 + distSq) 

def computeLossForSingleSource(subG, layout, similarityNorm):
    loss = 0
    source = subG.links[0]['Source']
    probabilityNorm = 0
    # similarityNorm = 0
    
    for link in subG.links:
        probabilityNorm = probabilityNorm + link['Weight']
    # for i in range(len(layout)):
    #     similarityNorm = similarityNorm + computeSimilarity(layout[source], layout[i])  
	# // for i := range layout {
    for link in subG.links:
        probabilitySourceToNodei = link['Weight'] / probabilityNorm
        similaritySourceToNodei = computeSimilarity(layout[link['Source']], layout[link['Target']]) / similarityNorm
        loss = loss - probabilitySourceToNodei * math.log(similaritySourceToNodei)
	# // fmt.Println("subG", subG, norm)
    return loss

def updateLayout(graph, layout, eps = 10**-6):
    for i in range(len(layout)):
        grad = computeGradient(i, graph, layout)
        for dim in [0,1]:
            layout[i][dim] = layout[i][dim]-grad[dim]*eps

def computeGradient(index, graph, layout):
    return numericGradient(index, graph, layout)

###############################################################################
############################## ANALYTIC GRADIENT ##############################
###############################################################################

###############################################################################
########################### NUMERIC GRADIENT METHOD ###########################
###############################################################################

def numericGradient(index, graph, layout, dh = 10**-8):
    subG = graph.ExtractSubGraph(index)
    grad = [0,0]
    layout_p = copy.deepcopy(layout)
    layout_n = copy.deepcopy(layout)
    for dim in [0, 1]:
        layout_p[index][dim] = layout_p[index][dim] + dh/2
        layout_n[index][dim] = layout_n[index][dim] - dh/2
        grad[dim] = (computeLossFunction(graph, layout_p) - computeLossFunction(graph, layout_n))/dh
        layout_p[index][dim] = layout_p[index][dim] - dh/2
        layout_n[index][dim] = layout_n[index][dim] + dh/2
    return grad


def analyticGradient(index, graph, layout, dh = 10**-8):
    grad = [0,0]
    similarityNorm = 0
    probabilityNorm = 0
    subG = graph.ExtractSubGraph(index)

    for k in range(len(layout)):
        for l in range(len(layout)):
            if k != l:
                similarityNorm = similarityNorm + computeSimilarity(layout[k], layout[l])

    for link in subG.links:
        probabilityNorm = probabilityNorm + link['Weight']

    for link in subG.links:
        sim = computeSimilarity(layout[link['Source']], layout[link['Target']])
        p_ij = link['Weight'] / probabilityNorm
        q_ij = sim / similarityNorm
        for dim in [0, 1]:
            # q = 
            x_i = layout[link['Source']][dim]
            x_j = layout[link['Target']][dim]
            gr = 1
            gr = gr*(0 - q_ij)
            gr = gr*(x_i - x_j)
            gr = gr*sim
            grad[dim] = grad[dim] + gr
    
    return grad

def analyticGradient2(index, graph, layout, dh = 10**-8):
    grad = [0,0]
    k = index

    for i in range(len(layout)):
        subG = graph.ExtractSubGraph(i)
        probabilityNorm = 0
        for link in subG.links:
            probabilityNorm = probabilityNorm + link['Weight']
        
        for link in subG.links:
            j = link['Target']
            for dim in [0,1]:
                x_i = layout[i][dim]
                x_j = layout[j][dim]
                S = computeSimilarity(layout[i], layout[j])
                dS = -2*computeSimilarity(layout[i], layout[j])**2*( (k == i) - (k == j) )*(x_i - x_j)
                Sm = 0
                dSm = 0
                for m in range(len(layout)):
                    x_m = layout[m][dim]
                    Sm = Sm + computeSimilarity(layout[i], layout[m])
                    dSm = dSm - 2*computeSimilarity(layout[i], layout[m])**2*( (k == i) - (k == m) )*(x_i - x_m)
                print(S)
                print(dSm)
                grad[dim] = grad[dim] + -1/probabilityNorm*(dS/S + Sm/dSm)

    return grad


def analyticGradient3(index, graph, layout, dh = 10**-8):
    k = index
    n = len(layout)

    w_k = 0
    S_k = 0
    subG = graph.ExtractSubGraph(k)
    for link in subG.links:
        w_k = w_k + link['Weight']
        S_k = S_k + computeSimilarity(layout[k], layout[link['Target']])

    grad = [0, 0]
    for link in subG.links:
        i = link['Target']
        subG_i = graph.ExtractSubGraph(i)
        w_i = 0
        for link_i in subG_i.links:
            w_i = w_i + link_i['Weight']
        term = (1/w_k + 1/w_i)*computeSimilarity(layout[i], layout[k])
        grad[0] = grad[0] + term*(layout[i][0] - layout[k][0])

    for i in range(n):
        subG = graph.ExtractSubGraph(k)
        w_i = 0
        S_i = 0
        for link in subG.links:
            w_i = w_i + link['Weight']
            S_i = S_i + computeSimilarity(layout[k], layout[link['Target']])
        term = link
