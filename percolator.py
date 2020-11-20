import heapq
import util
import random
import copy
import functools
import heapq

def memoize(f):	
	cache = {}
	def g(graph, alpha = -1, beta = 2, maximizingPlayer = 0, first = 1):
		if first:
			cache.clear()
		d = (tuple(graph.V), tuple(graph.E), alpha, beta, maximizingPlayer)
		if d not in cache:
			cache[d] = f(graph, alpha, beta, maximizingPlayer)
			#print (cache)
		return cache[d]
	return g

bestmove = None
class PercolationPlayer:
	
	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
# Should return a vertex `v` from graph.V where v.color == -1
	def ChooseVertexToColor(graph, player):
		return random.choice([v for v in graph.V if v.color == -1])

# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
# Should return a vertex `v` from graph.V where v.color == player
# Right now, this is an pretty inefficient way that finds the best move off what vertexes is connected to.
# Essentially, if a vertex is connected to a Vertex that is the same color as itself, it adds one to the value
# on the other hand, if it connected to a Vertex that is a different color, then its subtracts 1
# Then is finds the bestmove(like if I was finding the biggest from a list)
# Winrate against Random is ~60%.
# ignore the rest for now, it doesn't really do anything yet. 
	def ChooseVertexToRemove(graph, player):
		gE = {e for e in graph.E if e.a.color == player and e.b.color == player}
		best = -100000
		bestmove = 0
		for v in graph.V:
			if v.color == player:
					eA= graph.IncidentEdges(v)
					eS = set(eA) & gE
					h = len(eS) * -2 + len(eA) + len(eA)
					if h > best:
						best = h
						bestmove = v
		return bestmove
		'''bestmove = None
		bestval = -1000
		l = []
		for v in graph.V:
			if v.color == player:
				val = 0 
				for e in graph.IncidentEdges(v):
					if e.a.color == player and e.b.color == player:
						val += 1
					else:
						val -= 1
				if val > bestval:
					bestval = val
					bestmove = v
		return bestmove'''


	def auxwinnable(graph, player, alpha = -1, beta = 2, maximizingPlayer = 1):
		if PercolationPlayer.isWin(graph, player, maximizingPlayer):
			return 1 - maximizingPlayer
		if maximizingPlayer:

			best = -1
			
			for v in graph.V:
				if v.color == player:
					g = copyGraph(graph)
					g.Percolate(g.GetVertex(v.index))
					val = PercolationPlayer.auxwinnable(g, player, alpha, beta, 0)

					best = max(best, val)
					alpha = max(alpha, best)

					if beta <= alpha:
						break		

			return best

		else:

			best = 2

			for v in graph.V:
				if v.color != player:
					g = copyGraph(graph)
					g.Percolate(g.GetVertex(v.index))
					val = PercolationPlayer.auxwinnable(g, player, alpha, beta, 1)

					best = min(best, val)
					beta = min(beta, best)

					if beta <= alpha:
						break

			
			return best

	#@functools.lru_cache(maxsize=None)
	@memoize
	def winnable(graph, alpha = -1, beta = 2, maximizingPlayer = 0, first = 1):
		if PercolationPlayer.isWin2(graph, maximizingPlayer):
			return 1 - maximizingPlayer

		if maximizingPlayer:

			best = -1
			
			for v in graph.V:
				if v.color == maximizingPlayer:
					g = copyGraph(graph)
					g.Percolate(g.GetVertex(v.index))
					val = PercolationPlayer.winnable(g, alpha, beta, 0, 0)

					best = max(best, val)
					alpha = max(alpha, best)

					if beta <= alpha:
						break		

			return best

		else:

			best = 2

			for v in graph.V:
				if v.color == maximizingPlayer:
					g = copyGraph(graph)
					g.Percolate(g.GetVertex(v.index))
					val = PercolationPlayer.winnable(g, alpha, beta, 1, 0)

					best = min(best, val)
					beta = min(beta, best)

					if beta <= alpha:
						break

			
			return best

	def isWin(graph, player, maximizingPlayer):
		if maximizingPlayer:
			p = player
		else:
			p = 1 - player

		return PercolationPlayer.isWin1(graph, p) 


		

	def isWin1(graph, player):
		for v in graph.V:
			if v.color == player:
				return False
		return True

	def isWin2(graph, maximizingPlayer):

		for v in graph.V:
			if v.color == maximizingPlayer:
				return False
		return True


	


'''	def winnable(self, graph, player, alpha = 0, beta = 0, maximizingPlayer = 1):

		if self.isEmpty(graph):
			return maximizingPlayer

		if maximizingPlayer:

			best = -1

			for v in graph.V:
				if v.color == player:
					val = self.winnable(graph.Percolate(v), player, alpha, beta, 0)

					best = max(best, val)
					alpha = max(alpha, best)

					if beta <= alpha:
						break
			
			return best

		else:

			best = 2

			for v in graph.V:
				if v.color != player:
					val = self.winnable(graph.Percolate(v), player, alpha, beta, 1)

					best = min(best, val)
					beta = min(beta, best)

					if beta <= alpha:
						break

			return best
'''
	


def copyGraph(graph):
	Vs = copy.copy(graph.V)
	Es = copy.copy(graph.E)
	return util.Graph(Vs, Es)
	



# Feel free to put any personal driver code here.
def main():
	pass





if __name__ == "__main__":
    main()
