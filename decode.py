import queue


def decode(Prufer):
    T = []
    n = len(Prufer) + 2
    D = []
    B = []
    for i in range(n - 2):
        D.append(i + 2)
        B.append(True)
    B.append(True)
    B.append(True)
    f = list(zip(D, Prufer))
    L = []
    for i in range(n - 2):
        if B[f[i][0] - 1] and B[f[i][1] - 1]:
            if f[i][1] != 1 and f[i][1] != n:
                if f[i][0] == f[f[i][1] - 2][1]:
                    B[f[i][0] - 1] = False
                    B[f[i][1] - 1] = False
                    if f[i][0] <= f[i][1]:
                        L.append((f[i][0], f[i][1]))
                    else:
                        L.append((f[i][1], f[i][0]))

    L.sort(reverse=True)

    a = [1]
    for l in L:
        if l[0] == l[1]:
            a.append(l[0])
        else:
            a.append(l[0])
            a.append(l[1])
    a.append(n)
    for i in range(len(a) - 1):
        T.append((a[i], a[i + 1]))
        B[a[i] - 1] = False
    B[a[-1] - 1] = False
    for d in D:
        if B[d - 1]:
            T.append((f[d - 2][0], f[d - 2][1]))
    return T


# print(decode([4, 10, 2, 5, 9, 1, 12, 6, 2, 9]))


class edge:
    def __init__(self, u, v, w=1):
        self.u = u
        self.v = v
        self.w = w


def fitness(Prufer,w):
    T = decode(Prufer)
    n = len(Prufer) + 2
    Adj = []
    for i in range(n + 1):
        Adj.append([])

    for e in T:
        Adj[e[0]].append(edge(e[0], e[1]))
        Adj[e[1]].append(edge(e[1], e[0]))
    cost = 0
    for i in range(n):
        vs = [False for j in range(n + 1)]
        cost_v = [0 for j in range(n + 1)]
        Q = queue.Queue()
        Q.put(i+1)
        vs[i+1] = True
        while not Q.empty():
            u = Q.get()

            for j in range(len(Adj[u])):
                v = Adj[u][j].v
                if not vs[v]:
                    Q.put(v)
                    # cost_v[v] = cost_v[u] + Adj[u][j].w
                    cost_v[v] = cost_v[u] + w[u-1][v-1]
                    cost += cost_v[v]
                    vs[v] = True

    return cost/2


# import numpy as np
# import random
# n = 4
# w = np.zeros((n, n))
# for i in range(0, n):
#     for j in range(i + 1, n):
#         w[i][j] = random.randint(1, 100)
# for i in range(0, n):
#     for j in range(0, i + 1):
#         w[i][j] = w[j][i]
# print(w)
# print(fitness([3,2],w))
