import math


def g_add_node(g, i, j, price):
    g[i][j] = price
    g[j][i] = price


def g_change(g, deleted, remain):
    for neighbours in g:
        if (remain in neighbours) and (deleted in neighbours):
            neighbours[remain] = min(neighbours[remain], neighbours[deleted])
        try:
            del neighbours[deleted]
        except KeyError:
            pass


def g_get_tree(g, todo='min'):
    if todo == 'max':
        for neighbours in g:
            for key, value in neighbours.items():
                if value != 0:
                    neighbours[key] = 1 / value
    connections = []
    i, j, price = 0, 0, 0
    for _ in range(len(g)-1):
        i, (j, price) = min(
                          map(lambda x: (x[0], min(x[1].items(), key=lambda y: y[1])), enumerate(g)),
                          key=lambda z: z[1][1]
                          )
        connections.append([i, j, price])
        g_change(g, j, i)
        g[j] = {j: math.inf}
    g[i] = {i: math.inf}
    return connections
