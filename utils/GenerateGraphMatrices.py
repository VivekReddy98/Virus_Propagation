import scipy
import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigs

class GenerateGraphMatrices(): 
	def __init__(self): 
		self.Graph = nx.Graph()
	
	def __generator_function(self, limit):
		for i in range(0,limit):
			yield i

	def __CreateIdentity(self, num_vertices):
		itr = self.__generator_function(num_vertices)
		self.Graph.add_nodes_from(itr)
		#print("Graph has {} nodes and {} vertices".format(self.Graph.number_of_nodes(), self.Graph.number_of_edges()))
		self.Identity = scipy.sparse.identity(num_vertices, format='csc')
		return None

	def GenGraphObj(self, EdgeFilePath):
		with open(EdgeFilePath,"r") as f:
			count_vertices_edges = f.readline().strip().split(" ")
			self.numVertices = int(count_vertices_edges[0])
			self.numEdges = int(count_vertices_edges[1])
			self.__CreateIdentity(int(count_vertices_edges[0]))
			for line in f:
				edges = line.strip().split(" ")
				self.Graph.add_edge(int(edges[0]), int(edges[1]))
		#print("{} has {} nodes and {} vertices".format(EdgeFilePath, self.Graph.number_of_nodes(), self.Graph.number_of_edges()))
		self.AdjMatrix = nx.to_scipy_sparse_matrix(self.Graph, format='csc')
		#print("The Matrices have been computed and are available for usage")
		return None

	def GenSystemMatrix(self, alpha, beta):
		return self.Identity.multiply(1-float(alpha)) + self.AdjMatrix.multiply(float(beta))

	# def ReturnADJI(self):
	# 	return self.Identity, self.AdjMatrix

	# def GetGraph(self):
	# 	return self.Graph


class StrengthAlter():
	def __init__(self, mat1, mat2): 
		self.mat1 = mat1
		self.mat2 = mat2

	def __multiply(self):
		return self.mat1.dot(self.mat2)

	def value(self, n=1):
		vals, vecs = eigs(self.__multiply(), k=n)
		return vals



 





