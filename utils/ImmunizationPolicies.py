import scipy, json, random, math
import numpy as np
import networkx as nx
from numpy import linalg as LA
from scipy.sparse.linalg import eigs
from utils.Simulator import Simulator, TimeStep
from utils.GenerateGraphMatrices import GenerateGraphMatrices

class Policy(Simulator):
	def __init__(self, A1, A2, resultsPath, num_initial_nodes=None):
		self.A1 = A1 #Path to alternating1.network
		self.A2 = A2 #Path to alternating2.network
		self.initial_num = num_initial_nodes
		self.results_path = resultsPath #Just a Location or directory
		self.stats_dict = {'frac_infected':{0:0}}

	## Override
	def initialize(self):
		G1 = GenerateGraphMatrices()
		G1.GenGraphObj(EdgeFilePath=self.A1)
		G2 = GenerateGraphMatrices()
		G2.GenGraphObj(EdgeFilePath=self.A2)
		self.numVertices = G1.numVertices
		self.Graph1 = G1.Graph
		self.Graph2 = G2.Graph
		return None

	def start(self, num_TimeSteps, alpha, beta):
		nodes_by_time = [self.zombies]
		for i in range(1, num_TimeSteps+1):
			if i%2!=0:
				T = TimeStep_Immune(self.Graph1, alpha, beta, self.zombies)
			else:
				T = TimeStep_Immune(self.Graph2, alpha, beta, self.zombies)
			T.infect()
			self.zombies = T.recover()
			self.stats_dict['frac_infected'][i] = len(self.zombies)/self.numVertices
			nodes_by_time.append(self.zombies)
		print("Simulation has been completed")
		with open(self.results_path+'/simulation_stats_'+str(alpha)+"_"+str(beta)+".json", "w+") as f:
			 json.dump(self.stats_dict, f)
		with open(self.results_path+'/nodes_by_time'+str(alpha)+"_"+str(beta)+".txt", 'w+') as f:
			for tstp in nodes_by_time:
				for _string in tstp:
					f.write(str(_string))
					f.write("\t")
				f.write("\n")
		return self.zombies

	def A(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		print("Before Immunization: {}".format(len(self.zombies)))
		immunized_nodes = set(random.sample([i for i in range(0, self.numVertices)], k))
		self.zombies = self.zombies.difference(immunized_nodes)
		print("After Immunization: {}".format(len(self.zombies)))
		self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		self.Graph1.remove_nodes_from(immunized_nodes) # Will remove edges and nodes
		self.Graph2.remove_nodes_from(immunized_nodes)
		self.Graph1.add_nodes_from(immunized_nodes) #Will only add edges
		self.Graph2.add_nodes_from(immunized_nodes)
		#self.zombies = self.start(itr, alpha, beta)
		#print("After Immunization and Simulation: {}".format(len(self.zombies)))
		# if verbose:
		# 	self.print_stats()
		# with open(self.results_path+'/simulation_stats_'+'PolA'+"_"+str(alpha)+"_"+str(beta)+".json", "w+") as f:
		#  	json.dump(self.stats_dict, f)
		return self.zombies

	def B(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		print("Before Immunization: {}".format(len(self.zombies)))
		immunized_nodes = np.argsort(-1*np.sum(nx.to_numpy_matrix(self.Graph1), axis=0))[0:1,0:k].tolist()[0]

		self.Graph1.remove_nodes_from(immunized_nodes) # Will remove edges and nodes
		self.Graph2.remove_nodes_from(immunized_nodes)
		self.Graph1.add_nodes_from(immunized_nodes) #Will only add nodes
		self.Graph2.add_nodes_from(immunized_nodes)

		self.zombies = self.zombies.difference(set(immunized_nodes))
		print("After Immunization: {}".format(len(self.zombies)))
		self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		# self.zombies = self.start(itr, alpha, beta)
		# print("After Immunization and Simulation: {}".format(len(self.zombies)))
		# if verbose:
		# 	self.print_stats()
		# with open(self.results_path+'/simulation_stats_'+'PolB'+"_"+str(alpha)+"_"+str(beta)+".json", "w+") as f:
		#  	json.dump(self.stats_dict, f)
		return self.zombies

	def C(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		print("Before Immunization: {}".format(len(self.zombies)))
		nodes = list(self.Graph1.nodes)
		immunized_nodes = []
		for j in range(1, k+1):
			if j%2!=0:
				degrees = self.Graph1.degree(nodes)
				degrees = [node[1] for node in degrees]
				high_degree_node = np.argsort(-1*np.asarray(degrees), axis=0)[0:1].tolist()
				#print(type(high_degree_node))
				immunized_nodes.extend(high_degree_node)
				self.Graph1.remove_nodes_from(high_degree_node) # Will remove edges and nodes
				self.Graph2.remove_nodes_from(high_degree_node)
				self.Graph1.add_nodes_from(high_degree_node) #Will only add edges
				self.Graph2.add_nodes_from(high_degree_node)
			else:
				degrees = self.Graph2.degree(nodes)
				degrees = [node[1] for node in degrees]
				high_degree_node = np.argsort(-1*np.asarray(degrees), axis=0)[0:1].tolist()
				immunized_nodes.extend(high_degree_node)
				self.Graph1.remove_nodes_from(high_degree_node) # Will remove edges and nodes
				self.Graph2.remove_nodes_from(high_degree_node)
				self.Graph1.add_nodes_from(high_degree_node) #Will only add edges
				self.Graph2.add_nodes_from(high_degree_node)

		print(len(immunized_nodes), immunized_nodes[0])
		self.zombies = self.zombies.difference(set(immunized_nodes))
		print("After Immunization: {}".format(len(self.zombies)))

		# self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		# self.zombies = self.start(itr, alpha, beta)
		# print("After Immunization and Simulation: {}".format(len(self.zombies)))
		# if verbose:
		# 	self.print_stats()
		# with open(self.results_path+'/simulation_stats_'+'PolC'+"_"+str(alpha)+"_"+str(beta)+".json", "w+") as f:
		# 	 json.dump(self.stats_dict, f)
		return self.zombies

	def __give_common_nodes(self, im1, im2, k):
		im = im1.intersection(im2)
		rem = im1.union(im2)
		rem = rem.difference(im)
		rem = set(random.sample(list(rem), k-len(im)))
		return im.union(rem)

	def D(self, k1, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		print("Before Immunization: {}".format(len(self.zombies)))
		LG1 = nx.to_scipy_sparse_matrix(self.Graph1)
		LG2 = nx.to_scipy_sparse_matrix(self.Graph2)
		values, VecG1 = eigs(LG1.asfptype(), k=1) 
		values, VecG2 = eigs(LG2.asfptype(), k=1)

		immunized_nodesLG1 = np.argsort(-1*VecG1, axis=0)[0:k1,0].tolist()
		immunized_nodesLG2 = np.argsort(-1*VecG2, axis=0)[0:k1,0].tolist()
		immunized_nodes = self.__give_common_nodes(set(immunized_nodesLG1), set(immunized_nodesLG2), k1)

		self.Graph1.remove_nodes_from(immunized_nodes) # Will remove edges and nodes
		self.Graph2.remove_nodes_from(immunized_nodes)
		self.Graph1.add_nodes_from(immunized_nodes) #Will only add edges
		self.Graph2.add_nodes_from(immunized_nodes)

		self.zombies = self.zombies.difference(set(immunized_nodes))
		print("After Immunization: {}".format(len(self.zombies)))
		# self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		# self.zombies = self.start(itr, alpha, beta)
		# print("After Immunization and Simulation: {}".format(len(self.zombies)))
		# if verbose:
		# 	self.print_stats()
		# with open(self.results_path+'/simulation_stats_'+'PolD'+"_"+str(alpha)+"_"+str(beta)+".json", "w+") as f:
		# 	 json.dump(self.stats_dict, f)
		return self.zombies

class TimeStep_Immune(TimeStep):
	def __init__(self, Graph, alpha, beta, nodes):
		self.Graph = Graph 
		self.alpha = alpha
		self.beta = beta
		self.zombies = set(nodes) # Should be a set
		self.num_zombies = len(self.zombies)

	def infect(self):
		neigh = []
		for node in self.zombies:
			neigh.extend([n for n in self.Graph.neighbors(node)])
		neigh = set(neigh)
		neigh.difference(self.zombies)
		zombified_nodes = set(random.sample(neigh, int(math.floor(self.beta*len(neigh)))))
		self.zombies = self.zombies.union(zombified_nodes)
		return None




