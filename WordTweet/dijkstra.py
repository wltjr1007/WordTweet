from collections import defaultdict


class Graph(object):
    def __init__(self):
        self.vertices = set()
        self.edge = defaultdict(list)
        self.dist = {}

    def addvertex(self, idnum):
        self.vertices.add(idnum)

    def addedge(self, frm, to, dist):
        self.edge[frm].append(to)
        self.edge[to].append(frm)
        self.dist[(frm, to)] = dist


def dijkstra(g, start):
    vertices = set(g.vertices)
    visit = {start: 0}
    path = {}

    while vertices:
        minvert = extractmin(vertices, visit)
        if minvert is None:
            break
        relax(g, vertices, minvert, visit, path)
    return visit, path


def extractmin(vertices, visit):
    minvert = None
    for vertex in vertices:
        if vertex in visit:
            if minvert is None:
                minvert = vertex
            elif visit[vertex] < visit[minvert]:
                minvert = vertex
    return minvert


def relax(g, vertices, minvert, visit, path):
    vertices.remove(minvert)
    current_weight = visit[minvert]
    for edge in g.edge[minvert]:
        try:
            weight = current_weight + g.dist[(minvert, edge)]
        except:
            continue
        if edge not in visit or weight < visit[edge]:
            visit[edge] = weight
            path[edge] = minvert
    return visit, path


def shortest_path(g, origin, dest):
    visited, paths = dijkstra(g, origin)
    fullpath = []
    tempdest = paths[dest]

    while tempdest != origin:
        fullpath.insert(0, tempdest)
        tempdest = paths[tempdest]

    fullpath.insert(0, origin)
    fullpath.append(dest)

    return visited[dest], fullpath
