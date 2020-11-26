# Import is different depending on if the map is rendered from within MiroSim or as a stand alone script.
try:
    import NodeMap
except:
    from NodeMap import NodeMap

NodeMap.GenerateMap()