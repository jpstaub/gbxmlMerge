from topologicpy import topologic

def faceByVertices(vertices):
    vertices
    edges = []
    for i in range(len(vertices)-1):
        v1 = vertices[i]
        v2 = vertices[i+1]
        try:
            e = topologic.Edge.ByStartVertexEndVertex(v1, v2)
            if e:
                edges.append(e)
        except:
            continue

    v1 = vertices[-1]
    v2 = vertices[0]
    try:
        e = topologic.Edge.ByStartVertexEndVertex(v1, v2)
        if e:
            edges.append(e)
    except:
        pass
    if len(edges) > 3:
        c = topologic.Cluster.ByTopologies(edges, False)
        w = c.SelfMerge()
        if w.Type() == topologic.Wire.Type() and w.IsClosed():
            f = topologic.Face.ByExternalBoundary(w)
        else:
            raise Exception("Error: Could not get a valid wire")
    else:
        raise Exception("Error: could not get a valid number of edges")
    return f

v1 = topologic.Vertex.ByCoordinates(0,0,0)
v2 = topologic.Vertex.ByCoordinates(10,0,0)
v3 = topologic.Vertex.ByCoordinates(10,10,0)
v4 = topologic.Vertex.ByCoordinates(0,10,0)
f1 = faceByVertices([v1,v2,v3,v4])
print(f1)
c1 = f1.Centroid()
print("Centroid:", c1.X(), c1.Y(), c1.Z())
