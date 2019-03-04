def EdgePathtoNodePath(edgePath):
    """Convert a path represented edges to a path represented by respective nodes"""
    nodePath = []
    for path in edgePath:
        node_path = [path[0].node_a,path[0].node_b]
        if len(path)>1:
            for edge in path[1:]:
                node_path.append(edge.node_b)
        nodePath.append(node_path)
    return nodePath

def overlapBetweenStrings(string1,string2):
    """Brute force find overlap between suffix of string1 and prefix of string 2"""
    i = 0
    suffString1 = string1
    prefString2 = string2
    while prefString2 != suffString1:
        i += 1
        suffString1 = string1[i:]
        prefString2 = string2[0:len(suffString1)]
    return len(prefString2)-1  

def stringSpelledByNodePath(path,reads_map):
    """String spelled by a path represented by node values"""
    string = reads_map[path[0]]
    for i in range(1,len(path)):
        string1 = reads_map[path[i-1]] 
        string2 = reads_map[path[i]]
        index = overlapBetweenStrings(string1,string2)
        string += string2[index+1:]
    return string

def contig_assembly(graph,reads_map):
    """ 
    input: DiGraph object
    output: list of contigs (strings formed by non_branching_paths)
    """
    contigs = []
    nodePath = EdgePathtoNodePath(graph.maximal_non_branching_paths())
    for path in nodePath:
        contigs += [stringSpelledByNodePath(path,reads_map)]
        
    return contigs