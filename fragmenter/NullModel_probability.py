

def probabilityPerm(surface, fragmentObj):
    # This function will slightly perturb one of the computed parcellations for permutation purposes
    # The surface argument requires a tuple with 2 arrays (coordinates and faces)
    # fragmentObj is the fitted fragmented object (make sure that it has the 'label_' attribute)
    # The idea is that vertices at the edge of each parcel will be re-assigned with probability proportional 
    # to the number of its neighbors from different parcels.
    # It returns a vector with a label for each vertex
    
    # Get the neighbors of each vertex
    A = adjacency.SurfaceAdjacency(surface[0], surface[1])
    A.generate() # A.adj to get the adjacency list
    
    # Get the new set of labels for all vertices
    nVerts = np.size(fragmentObj.label_)
    newLbls = []
    for vertex in np.arange(nVerts):
        labels = fragmentObj.label_[A.adj[vertex]] # Assign the original parcel labels to the vertex's neighbors
        newLbls.append(np.random.choice(labels)) # Reassign a label

    return newLbls