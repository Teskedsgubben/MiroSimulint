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
    radius = np.sqrt(len(nodes))
    for i in range(len(nodes)):
        layout.append([radius*(1-2*rng.random()), radius*(1-2*rng.random())])
    return layout

def PlotLayout(graph, layout, save_name = False, title=False):
    plt.clf()
    plt.scatter(*zip(*layout))
    for i in range(len(graph.labels)):
        plt.annotate(graph.labels[i], layout[i])
    for link in graph.links:
        source = link['Source']
        target = link['Target']
        link_line = [layout[source], layout[target]]
        plt.plot(*zip(*link_line))
    if title:
        plt.title(title)
    if save_name:
        # print('saving to: '+save_name)
        plt.savefig(save_name)
    else:
        plt.show()
    

def WriteGraph(links):
    filestream = open(graphfile, "w")
    filestream.truncate(0)
    filestream.write(json.dumps(links))

def ReadGraph(filename):
    if not filename:
        filename = graphfile
    filestream = open(filename, "r")
    graph = Graph()
    name, ext = os.path.splitext(filename)
    if ext == '.json':
        graph.append(json.loads(filestream.read()), symmetric = True)
    if ext == '.dat':
        link = filestream.readline().split()
        while(len(link)>0):
            graph.append({'Source': link[0], 'Target': link[1], 'Weight': 1}, symmetric = True)
            link = filestream.readline().split()
    return graph

def GenerateMap(iterations = 100, filename = False, log = True, output_name=False):
    graph = ReadGraph(filename)
    layout = RandomLayout(graph.labels, seed = 1)
    loss_old = computeLossFunction(graph, layout)
    dots = 0
    if log:
        if not output_name:
            output_name = 'NodeMap/Module_Map_Before_local.png'
        PlotLayout(graph, layout, save_name=output_name, title='Before')
    
    print('Initial loss:', loss_old)
    for i in range(iterations):
        if(capture):
            PlotLayout(graph, layout, save_name='NodeMap/capture_local/graph_plot_'+str(i).zfill(5)+'.png')
        updateLayout(graph, layout, 2*10**-0)
        if dots < (i/iterations)*20:
            dots = dots + 1
            print('.', end = '', flush = True)
    if(capture):
        PlotLayout(graph, layout, save_name='NodeMap/capture_local/graph_plot_'+str(iterations).zfill(5)+'.png')

    print(' Done!')
    if log:
        if output_name == 'NodeMap/Module_Map_Before_local.png':
            output_name = 'NodeMap/Module_Map_After_local.png'
        PlotLayout(graph, layout, save_name=output_name, title='After')
        print('\nSaved map as: '+output_name)
    
    loss_new = computeLossFunction(graph, layout)
    print('Final loss:', loss_new)


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
    W = []
    S = []
    
    # Compute similarity norms
    for i in range(len(layout)):
        S.append(0)
        for j in range(len(layout)):
            if j != i:
                S[i] = S[i] + computeSimilarity(layout[i], layout[j])

        # Compute probability norms
        W.append(0)
        subG = graph.ExtractSubGraph(i)
        for link in subG.links:
            W[i] = W[i] + link['Weight']

    # Step in the layout
    grad=[]
    for i in range(len(layout)):
        grad.append(computeGradient(i, graph, layout, W, S))
        
    
    for i in range(len(layout)):
        for dim in [0,1]:
            layout[i][dim] = layout[i][dim]-grad[i][dim]*eps

def computeGradient(index, graph, layout, W, S):
    # return numericGradient(index, graph, layout, W, S)
    return analyticGradient(index, graph, layout, W, S)

def getNormalized(vec):
    d = 0
    n = []
    for v in vec:
        d = d + v**2
    for v in vec:
        n.append(v/d**(1/2))
    return  n

###############################################################################
############################## ANALYTIC GRADIENT ##############################
###############################################################################

def analyticGradient(index, graph, layout, W, S, dh = 10**-8):
    k = index
    n = len(layout)
    other_nodes = [i for i in range(n) if i != k]
    subG_k = graph.ExtractSubGraph(k)

    # w_k = 0
    # S_k = 0
    # for link in subG.links:
    #     w_k = w_k + link['Weight']
    # for i in other_nodes:
    #     S_k = S_k + computeSimilarity(layout[k], layout[i])

    grad = [0, 0]
    for link in subG_k.links:
        i = link['Target']
        # subG_i = graph.ExtractSubGraph(i)
        # w_i = 0
        # for link_i in subG_i.links:
        #     w_i = w_i + link_i['Weight']
        S_ik = computeSimilarity(layout[i], layout[k])
        term = -(1/W[k] + 1/W[i])*2*S_ik
        grad[0] = grad[0] + term*(layout[i][0] - layout[k][0])
        grad[1] = grad[1] + term*(layout[i][1] - layout[k][1])

    for i in other_nodes:
        # S_i = 0
        # for j in range(n):
        #     if j != i:
        #         S_i = S_i + computeSimilarity(layout[i], layout[j])
        S_ik = computeSimilarity(layout[i], layout[k])
        term = (1/S[k] + 1/S[i])*2*S_ik**2
        grad[0] = grad[0] + term*(layout[i][0] - layout[k][0])
        grad[1] = grad[1] + term*(layout[i][1] - layout[k][1])

    return grad

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
