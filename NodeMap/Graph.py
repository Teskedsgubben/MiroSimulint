

class Graph():
    def __init__(self):
        self.links = []
        self.labels = []

    def append(self, link, symmetric = False):
        if type(link) == type([]):
            for lk in link:
                self.append(lk)
        else:
            for side in ['Source', 'Target']:
                if type(link[side]) == type(''):
                    if not link[side] in self.labels:
                        self.labels.append(str(link[side]))
                    link[side] = self.labels.index(link[side])
            self.links.append(link)
            if symmetric:
                link_sym = {
                    'Source': link['Target'],
                    'Target': link['Source'],
                    'Weight': link['Weight'],
                }
                self.links.append(link_sym)
    
    def getLink(self, i):
        return self.links[i]

    
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

    def ExtractSubGraph(self, source):
        subG = Graph()
        for link in self.links:
            if link['Source'] == source or link['Target'] == source:
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
