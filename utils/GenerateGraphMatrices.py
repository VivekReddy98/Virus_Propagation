import scipy, math
from scipy import sparse
import numpy as np
import networkx as nx
from random import shuffle

class GenerateGraphMatrices(): 
	def __init__(self, g): 
		self.Graph = nx.Graph()
		self.g = g

	def __getGroup(self, num_vertices):
		self.verticesGroup = {} 
		vertices = [i for i in range(0,num_vertices)]
		shuffle(vertices)
		if self.g>num_vertices:
			raise Exception("The value of g cannot be greater than num_vertices")		
		chunk_size = int(math.ceil(num_vertices/self.g))
		#print(chunk_size)
		self.group_num = 0
		i = 0
		while self.group_num<self.g:
			if i+chunk_size<num_vertices:
				yield vertices[i:i+chunk_size]
				i = i+chunk_size
				self.verticesGroup[self.group_num] =  vertices[i:i+chunk_size]
				self.group_num = self.group_num+1
			else:
				yield vertices[i:num_vertices]
				self.verticesGroup[self.group_num] =  vertices[i:num_vertices]
				self.group_num = self.group_num+1
		yield None

	def __GenSeedScoresMatrix(self, num_vertices):
		Ei = np.zeros((num_vertices, self.g))
		itr = self.__getGroup(num_vertices)
		list_vertices = next(itr)
		while list_vertices!=None:
			Ei[list_vertices,self.group_num] = 1
			list_vertices = next(itr)
		return sparse.csc_matrix(Ei)
	
	def __generator_function(self, limit):
		for i in range(0,limit):
			yield i

	def CreateVertices(self, num_vertices):
		itr = self.__generator_function(num_vertices)
		self.Graph.add_nodes_from(itr)
		#print("Graph has {} nodes and {} vertices".format(self.Graph.number_of_nodes(), self.Graph.number_of_edges()))
		Identity = scipy.sparse.identity(num_vertices, format='csc')
		return Identity, self.__GenSeedScoresMatrix(num_vertices)

	def GenerateGraphObj(self, EdgeFilePath):
		with open(EdgeFilePath,"r") as f:
			count_vertices_edges = f.readline().strip().split(" ")
			Identity, Seed = self.CreateVertices(int(count_vertices_edges[0]))
			for line in f:
				edges = line.strip().split(" ")
				self.Graph.add_edge(int(edges[0]), int(edges[1]))
		#print("{} has {} nodes and {} vertices".format(EdgeFilePath, self.Graph.number_of_nodes(), self.Graph.number_of_edges()))
		AdjMatrix = nx.to_scipy_sparse_matrix(self.Graph, format='csc')
		n,m = AdjMatrix.shape
		diags = AdjMatrix.sum(axis=1)
		DiagonalMatrix = scipy.sparse.spdiags(diags.flatten(), [0], m, n, format='csc')
		#print("The Matrices have been computed and are available for usage")
		return Identity, Seed, AdjMatrix, DiagonalMatrix


## Testing this class
if __name__ == '__main__':
	#sc=SparkContext("local", "degree.py")
	#sqlContext = SQLContext(sc)
	#sqlContext.sql("set spark.sql.shuffle.partitions=2")
	#sc.setLogLevel("WARN")
	#G = GenerateGraphMatrices()
	#S, A, G, graph = G.GenerateGraphObj(EdgeFilePath='datasets/autonomous/0_autonomous.txt', g=10)
	#S, A, G, graph = G.ComputeAffinityMatrix(EdgeFilePath='datasets/autonomous/1_autonomous.txt')

	print(S.shape, A.shape, G.shape, graph.number_of_edges(), graph.number_of_nodes())
 





