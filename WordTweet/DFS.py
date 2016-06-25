WHITE = 0
GRAY = 1
BLACK = 2


class Adj:
    def __init__(self):
        self.n = 0
        self.next = None


class Vertex:
    def __init__(self, name):
        self.color = WHITE
        self.parent = -1
        self.name = name
        self.n = 0
        self.first = None
        self.weight = 0

    def add(self, v):
        a = Adj()
        a.n = v.n
        a.next = self.first
        self.first = a
        self.weight += 1

    def copy(self, other):
        self.color = other.color
        self.parent = other.parent
        self.name = other.name
        self.n = other.n
        self.first = other.first


class DFSVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.d = 0
        self.f = 0

    def copy(self, other):
        super().copy(other)
        self.d = other.d
        self.f = other.f


class Queue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.sz = 0
        self.buf = []

    def create_queue(self, sz):
        self.sz = sz
        self.buf = list(range(sz))  # malloc(sizeof(int)*sz)

    def enqueue(self, val):
        self.buf[self.rear] = val
        self.rear = (self.rear + 1) % self.sz

    def dequeue(self):
        res = self.buf[self.front]
        self.front = (self.front + 1) % self.sz
        return res

    def is_empty(self):
        return self.front == self.rear


def g_transpose(vertices, vertices1):
    for i in range(len(vertices1)):
        vertices1[i].first = None
    for v in vertices:
        p = v.first
        while p:
            vertices1[p.n].add(v)
            p = p.next


class DepthFirstSearch:
    def __init__(self):
        self.time = 0
        self.vertices = None
        self.scclist = []

    def set_vertices(self, vertices):
        self.vertices = vertices
        for i in range(len(self.vertices)):
            self.vertices[i].n = i

    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.time += 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next
        u.color = BLACK
        self.time += 1
        u.f = self.time

    def transpose(self):
        vertices1 = []
        for v in self.vertices:
            v1 = DFSVertex(v.name)
            v1.copy(v)
            vertices1.append(v1)
        g_transpose(self.vertices, vertices1)
        self.set_vertices(vertices1)

    def left(self, n):
        return 2 * n + 1

    def right(self, n):
        return 2 * n + 2

    def heapify(self, A, i, heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            self.heapify(A, largest, heapsize)

    def buildheap(self, A):
        for i in range(len(A) // 2 + 1, 0, -1):
            self.heapify(A, i - 1, len(A))

    def heapsort(self, A):
        self.buildheap(A)
        for i in range(len(A), 1, -1):
            A[i - 1], A[0] = A[0], A[i - 1]
            self.heapify(A, 0, i - 1)

    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices

    def scc(self):
        self.dfs()
        self.transpose()
        sorted = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in sorted:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n])
                for i in range(5):
                    maxcnt = -1
                    maxset = None
                    for tmp in self.scclist:
                        if maxcnt <= tmp[0]:
                            maxcnt = tmp[0]
                            maxset = tmp
                    if maxcnt != -1:
                        print(i + 1, ".", end="")
                        self.printscc(maxset[1])
                        self.scclist.remove(maxset)
                        print("")

    def printscc(self, u):
        print(u.name, end=" ")
        vset = self.vertices
        if u.parent >= 0:
            self.printscc(vset[u.parent])

    def findscccnt(self, u):
        cnt = 1
        vset = self.vertices
        if u.parent >= 0:
            cnt += self.findscccnt(vset[u.parent])
        return cnt

    def scc_find(self, u):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n])
            v = v.next
        if not found:
            self.scclist.append([self.findscccnt(u), u])
        u.color = BLACK
