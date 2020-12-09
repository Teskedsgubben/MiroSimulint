import random as rng
import json

class Graph():
    def __init__(self):
        self.links = []
        self.labels = []

    def append(self, link, symmetric = False):
        if type(link) == type([]):
            for lk in link:
                self.append(lk, symmetric)
        else:
            for side in ['Source', 'Target']:
                if not str(link[side]) in self.labels:
                    self.labels.append(str(link[side]))
                if type(link[side]) == type(''):
                    link[side] = self.labels.index(link[side])
            self.links.append(link)
            if symmetric:
                link_sym = {
                    'Source': int(link['Target']),
                    'Target': int(link['Source']),
                    'Weight': link['Weight'],
                }
                self.links.append(link_sym)
    
    def getLink(self, i): 
        return self.links[i]

    def generateRandom(self, nr_of_nodes, nr_of_neighbors):
        if type(nr_of_neighbors) != type([]):
            nr_of_neighbors = [nr_of_neighbors]
        if max(nr_of_neighbors) >= nr_of_nodes:
            print('More neighbors then nodes, graph not generated')
            return
        for i in range(nr_of_nodes):
            neighs = []
            nr_neighs = nr_of_neighbors[rng.randrange(0, len(nr_of_neighbors))]
            for j in range(nr_neighs):
                new_neigh = i
                while new_neigh == i or new_neigh in neighs:
                    # new_neigh = rng.randrange(0, nr_of_nodes)
                    new_neigh = round(rng.normalvariate(i, nr_neighs/1.41))
                    new_neigh = new_neigh + (1*(new_neigh < 0) - 1*(new_neigh >= nr_of_nodes))*nr_of_nodes
                    if new_neigh < 0:
                        new_neigh = new_neigh + nr_of_nodes
                    if new_neigh >= nr_of_nodes:
                        new_neigh = new_neigh - nr_of_nodes
                neighs.append(new_neigh)
                link = {
                    'Source': i,
                    'Target': new_neigh,
                    'Weight': 1,
                }
                self.append(link)

    def writeToFile(self, filename):
        '''Currently loses labels'''
        filestream = open(filename, "w")
        filestream.truncate(0)
        labeled_links = []
        for link in self.links:
            labeled_links.append({
                    'Source': self.labels[link['Source']],
                    'Target': self.labels[link['Target']],
                    'Weight': link['Weight'],
                })
        filestream.write(json.dumps(labeled_links))


    
    # type Link struct {
    #     Source int64
    #     Target int64
    #     Weight float64
    # }

    # func (g Graph) Sort() {
    #     sort.Slice(g, func(i, j int) bool {
    #         if g[i].Source != g[j].Source {
    #             return g[i].Source < g[j].Source
    #         }
    #         return g[i].Target < g[j].Target
    #     })
    # }

    # //
    # func (g Graph) IsSorted() bool {
    #     for i := 1; i < len(g); i++ {
    #         if g[i-1].Source > g[i].Source {
    #             return false
    #         }
    #         if g[i-1].Source == g[i].Source && g[i-1].Target > g[i].Target {
    #             return false
    #         }
    #     }
    #     return true
    # }

    # //
    # func (g Graph) SortSearchWeight(source, target int64, fallback float64) float64 {
    #     start := sort.Search(len(g), func(i int) bool {
    #         return g[i].Source > source || (g[i].Source == source && g[i].Target >= target)
    #     })
    #     if start == len(g) {
    #         return fallback
    #     }
    #     if g[start].Source == source && g[start].Target == target {
    #         return g[start].Weight
    #     }
    #     return fallback
    # }

    def ExtractSubGraph(self, source, bidi = False):
        subG = Graph()
        for link in self.links:
            if link['Source'] == source:
                subG.append(link)
            if bidi and link['Target'] == source:
                subG.append(link)
        return subG
    

    # func (g Graph) GetSources() []int64 {
    #     found := make(map[int64]bool)
    #     sources := make([]int64, 0)
    #     for i := range g {
    #         _, exists := found[g[i].Source]
    #         if !exists {
    #             sources = append(sources, g[i].Source)
    #             found[g[i].Source] = true
    #         }
    #     }
    #     return sources
    # }

    # //
    # func (g Graph) GetTargets() []int64 {
    #     found := make(map[int64]bool)
    #     targets := make([]int64, 0)
    #     for i := range g {
    #         _, exists := found[g[i].Target]
    #         if !exists {
    #             targets = append(targets, g[i].Target)
    #             found[g[i].Target] = true
    #         }
    #     }
    #     return targets
    # }

    # //
    # func (g Graph) GetAllNodes() []int64 {
    #     nodes := g.GetSources()
    #     nodes = append(nodes, g.GetTargets()...)
    #     return RemoveDuplicates(nodes)
    # }

    # //
    # func RemoveDuplicates(elements []int64) []int64 {
    #     encountered := map[int64]bool{}
    #     result := []int64{}
    #     for _, v := range elements {
    #         if !encountered[v] {
    #             encountered[v] = true
    #             result = append(result, v)
    #         }
    #     }
    #     return result
    # }

    # //
    # func (g Graph) GetFilteredGraph(minW, okW float64, maxN int) Graph {

    #     type tw struct {
    #         target int64
    #         w      float64
    #     }
    #     sources := g.GetSources()
    #     cleaned := make(Graph, 0)
    #     for _, source := range sources {
    #         subG := g.ExtractSubGraph(source)
    #         tws := make([]tw, len(subG))
    #         for i := 0; i < len(subG); i++ {
    #             tws[i] = tw{
    #                 target: subG[i].Target,
    #                 w:      subG[i].Weight,
    #             }
    #         }
    #         sort.Slice(tws, func(i, j int) bool {
    #             return tws[i].w > tws[j].w
    #         })
    #         for i, twi := range tws {
    #             if (twi.w >= okW) || (i < maxN && twi.w >= minW) {
    #                 cleaned = append(cleaned, Link{
    #                     Source: source,
    #                     Target: twi.target,
    #                     Weight: twi.w,
    #                 })
    #             }
    #         }
    #     }
    #     return cleaned
    # }

    # //
    # func (g Graph) KeepTheseNodes(r2V map[int64]float64, threshold float64) Graph {
    #     cleaned := make(Graph, 0)
    #     for _, e := range g {
    #         if r2V[e.Source] > threshold && r2V[e.Target] > threshold {
    #             cleaned = append(cleaned, e)
    #         }
    #     }
    #     return cleaned
    # }
