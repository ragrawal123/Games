import random
import itertools
import copy
import traceback
import sys
import percolator
w = 0
nv = 0
class Vertex:
    def __init__(self, index, color=-1):
        self.index = index
        self.color = color

    def __repr__(self):
        if self.color == -1:
            return "Vertex({0})".format(self.index)
        else:
            return "Vertex({0}, {1})".format(self.index, self.color)

    '''def __eq__(self, other):
        if self.index == other.index and self.color and other.color:
            return True
        return False'''

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Edge({0}, {1})".format(self.a, self.b)

    '''def __eq__(self, other):
        if self.a == other.a and self.b == other.b:
            return True
        return False'''



class Graph:
    def __init__(self, v, e):
        self.V = set(v)
        self.E = set(e)

    def __repr__(self):
        return "Graph({0}, {1})".format(self.V, self.E)

    '''def __eq__(self, other):
        for v1, v2 in self.V, other.V:
            if v1 != v2:
                return False
        for e1, e2 in self.E, other.E:
            if e1 != e2:
                return False
        return True'''


    # Gets a vertex with given index if it exists, else return None.
    def GetVertex(self, i):
        for v in self.V:
            if v.index == i:
                return v
        return None

    # Returns the incident edges on a vertex.
    def IncidentEdges(self, v):
        return [e for e in self.E if (e.a == v or e.b == v)]

    def isIsolated(self, v):
        for e in self.E:
            if e.a == v or e.b == v:
                return False
        return True
    # Removes the given vertex v from the graph, as well as the edges attached to it.
    # Removes all isolated vertices from the graph as well.
    def Percolate(self, v):
        # Get attached edges to this vertex, remove them.
        E1 = copy.copy(self.E)
        for e in E1:
            v1 = e.a
            v2 = e.b
            if v1 == v:
                self.E.remove(e)
                if self.isIsolated(v2):
                    self.V.remove(v2)
            elif v2 == v:
                self.E.remove(e)
                if self.isIsolated(v1):
                    self.V.remove(v1)

        # Remove this vertex.
        self.V.remove(v)
        # Remove all isolated vertices.


# This is the main game loop.
def PlayGraph(s, t, graph):
    global w
    global nv
    players = [s, t]
    active_player = 0
    

    # Phase 1: Coloring Phase
    while any(v.color == -1 for v in graph.V):
        # First, try to just *run* the player's code to get their vertex.
        try:
            chosen_vertex = players[active_player].ChooseVertexToColor(copy.copy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != -1:
                return 1 - active_player
            # If output is reasonable, color this vertex.
            original_vertex.color = active_player
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player

        # Swap current player.
        active_player = 1 - active_player

    # Check that all vertices are colored now.
    assert all(v.color != -1 for v in graph.V)

    #gr = copy.deepcopy(graph)
    #asd = percolator.PercolationPlayer.auxwinnable(graph, 0)
    #print ("W:" + str(asd))
    #w = w + asd

    # Phase 2: Removal phase
    # Continue while both players have vertices left to remove.
    while len([v for v in graph.V if v.color == active_player]) > 0:
        # First, try to just *run* the removal code.
        try:
            chosen_vertex = players[active_player].ChooseVertexToRemove(copy.copy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                print ("not valid V: " + str(active_player))
                nv += 1
                return 1 - active_player
            if original_vertex.color != active_player:
                return 1 - active_player
            # If output is reasonable, remove ("percolate") this vertex + edges attached to it, as well as isolated vertices.
            graph.Percolate(original_vertex)
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Swap current player
        active_player = 1 - active_player

    # Winner is the non-active player.
    
    #if (asd == 1 and 1 - active_player == 1):
        #print("fail")
    return 1 - active_player


# This method generates a binomial random graph with 2k vertices
# having probability p of an edge between each pair of vertices.
def BinomialRandomGraph(k, p):
    v = {Vertex(i) for i in range(2 * k)}
    e = {Edge(a, b) for (a, b) in itertools.combinations(v, 2) if random.random() < p}
    return Graph(v, e)


# This method creates and plays a number of random graphs using both passed in players.
def PlayBenchmark(p1, p2, iters):
    graphs = (
        BinomialRandomGraph(random.randint(1, 10), random.random())
        for _ in range(iters)
    )
    wins = [0, 0]
    for graph in graphs:
        g1 = copy.deepcopy(graph)
        g2 = copy.deepcopy(graph)
        # Each player gets a chance to go first on each graph.
        winner_a = PlayGraph(p1, p2, g1)
        wins[winner_a] += 1
        winner_b = PlayGraph(p2, p1, g2)
        wins[1-winner_b] += 1
    return wins


# This is a player that plays a legal move at random.
class RandomPlayer:
    # These are "static methdods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        m = random.choice([v for v in graph.V if v.color == -1])
        #print("R: " + str(m.index))
        return m

    def ChooseVertexToRemove(graph, active_player):
        return random.choice([v for v in graph.V if v.color == active_player])

class TestPlayer:
    # These are "static methdods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.

    def ChooseVertexToColor(graph, active_player):
        V = [Vertex(0), Vertex(1)]
        E = [Edge(V[0], V[1])]
        graph = Graph(V, E)
        return V[0]

    def ChooseVertexToRemove(graph, active_player):
        return random.choice([v for v in graph.V if v.color == active_player])


def part1(s, t, graph):
    players = [s, t]
    active_player = 0
    

    # Phase 1: Coloring Phase
    while any(v.color == -1 for v in graph.V):
        # First, try to just *run* the player's code to get their vertex.
        try:
            chosen_vertex = players[active_player].ChooseVertexToColor(copy.copy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != -1:
                return 1 - active_player
            # If output is reasonable, color this vertex.
            original_vertex.color = active_player
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(fil0=sys.stdout)
            return 1 - active_player

        # Swap current player.
        active_player = 1 - active_player
def part2(s, t, graph):
    active_player = 0
    players = [s, t]
    # Phase 2: Removal phase
    # Continue while both players have vertices left to remove.
    while len([v for v in graph.V if v.color == active_player]) > 0:
        # First, try to just *run* the removal code.
        try:
            chosen_vertex = players[active_player].ChooseVertexToRemove(copy.copy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
                print ("not valid V: " + str(active_player))
            if original_vertex.color != active_player:
                print ("not valid color V: " + str(active_player))
                return 1 - active_player
            # If output is reasonable, remove ("percolate") this vertex + edges attached to it, as well as isolated vertices.
           # print("valid player: " + str(active_player) + " v: " + str(chosen_vertex.index))
            
            graph.Percolate(original_vertex)
            #print(graph)
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print("no V given" + str(active_player))
            return 1 - active_player
        # Swap current player
        active_player = 1 - active_player

    # Winner is the non-active player.
    

    return 1 - active_player

if __name__ == "__main__":
    # NOTE: we are not creating INSTANCES of these classes, we're defining the players
    # as the class itself. This lets us call the static methods.
    l1 = []
    l2 = []

    wins = PlayBenchmark(percolator.PercolationPlayer, RandomPlayer, 2000)
    print(wins)
    print(
        "Player 1: {0} Player 2: {1}".format(
            1.0 * wins[0] / sum(wins), 1.0 * wins[1] / sum(wins)
        )
    )
    #print (1 - percolator.PercolationPlayer.auxwinnable(g, 0))
    #print (percolator.PercolationPlayer.winnable(g))

    for i in range(1):
        break
        g = BinomialRandomGraph(15, 0.5)
        #print(i)
        part1(RandomPlayer, RandomPlayer, g)
        #print(g)
        #l1.append(1 - percolator.PercolationPlayer.auxwinnable(g, 0))
        l2.append(percolator.PercolationPlayer.winnable(g))
        #if(l1[i] != l2[i]):
        #    print(l1[i])
        #    print(l2[i])
        #    print(g)

    #print(l1)
    #print(l2)
    print(l1==l2)
    
    '''v = [Vertex(0, 0), Vertex(1, 0),
     Vertex(2, 1), Vertex(3, 1)]
    e = [Edge(v[0], v[2]), Edge(v[0], v[3]), Edge(v[1], v[2])]


    g = Graph(v, e)
    print(g)
    for i in range(1000):
        win = part2(TestPlayer, RandomPlayer, copy.deepcopy(g))
        if win == 1:

            print("fail: " + str(i))
            break
    print(percolator.PercolationPlayer.auxwinnable(g, 0))
    print(percolator.PercolationPlayer.winnable(g))'''
   

    '''g = BinomialRandomGraph(5, 0.5)
    
    part1(RandomPlayer, RandomPlayer, g)
    print(g)
    print(percolator.PercolationPlayer.auxwinnable(copy.deepcopy(g), 0))'''
    '''l1 = [Vertex(3, 1), Vertex(4, 1),
      Vertex(1, 0), Vertex(0, 0),
      Vertex(9, 0)]
    l2 = [Edge(l1[0], l1[4]), Edge(l1[1], l1[2]), Edge(l1[1], l1[3])]
    g = Graph(l1, l2)
    #print(g)
    print("W: " + str(percolator.PercolationPlayer.auxwinnable(g, 0)))
    
    
    iters = 100
    p1 = percolator.PercolationPlayer
    p2 = RandomPlayer
    
    wins = PlayBenchmark(p1, p2, iters)
    print(wins)
    print(
        "Player 1: {0} Player 2: {1}".format(
            1.0 * wins[0] / sum(wins), 1.0 * wins[1] / sum(wins)
        )
    )
    print("amtW: " + str(w))
    print(nv)
     iters = 1
    #print ("WW: " + str(w))
    graphs = (
        BinomialRandomGraph(7, random.random())
        for _ in range(iters)
    )

    for i in range(100):
        g = BinomialRandomGraph(2, 0.5)
        part1(RandomPlayer, RandomPlayer, g)

        l1.append(percolator.PercolationPlayer.auxwinnable(g, 1))
        l2.append(percolator.PercolationPlayer.winnable(g))
    print(l1)
    print(l2)
    print(l1==l2)
    Graph({Vertex(4, 0), Vertex(0, 1), Vertex(3, 0), Vertex(5, 0), Vertex(1, 1), Vertex(2, 1)}, {Edge(Vertex(4, 0), Vertex(5, 0)), Edge(Vertex(3, 0), Vertex(0, 1)), 
    Edge(Vertex(4, 0), Vertex(1, 1)), Edge(Vertex(3, 0), Vertex(5, 0)), 
    Edge(Vertex(5, 0), Vertex(1, 1)), Edge(Vertex(2, 1), Vertex(5, 0)), 
    Edge(Vertex(3, 0), Vertex(2, 1)), Edge(Vertex(2, 1), Vertex(1, 1)),
    Edge(Vertex(4, 0), Vertex(0, 1))})
    '''
   








