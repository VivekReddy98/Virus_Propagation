import scipy, json, random
import numpy as np
import networkx as nx
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

	def A(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		recovered_nodes = set(random.sample(self.zombies, k))
		self.zombies = self.zombies.difference(recovered_nodes)
		self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		self.zombies = self.start(itr, alpha, beta)
		if verbose:
			self.print_stats()
		return self.zombies

	def B(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		immunized_nodes = np.argsort(-1*np.sum(nx.to_numpy_matrix(self.Graph1), axis=0))[0:1,0:k].tolist()[0]
		#print(immunized_nodes)
		self.Graph1.remove_nodes_from(immunized_nodes) # Will remove edges and nodes
		self.Graph2.remove_nodes_from(immunized_nodes)
		self.Graph1.add_nodes_from(immunized_nodes) #Will only add edges
		self.Graph2.add_nodes_from(immunized_nodes)
		self.zombies = self.zombies.difference(set(immunized_nodes))
		self.stats_dict['frac_infected'][0] = len(self.zombies)/self.numVertices
		self.zombies = self.start(itr, alpha, beta)
		if verbose:
			self.print_stats()
		return self.zombies

	def C(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		nodes_by_time = [self.zombies]
		for i in range(1, itr+1):
			high_degree_node = np.argsort(-1*nx.to_scipy_sparse_matrix(self.Graph1, format='csr').sum(axis=0).toarray())[0:1].tolist()
			self.Graph1.remove_nodes_from(high_degree_node) # Will remove edges and nodes
			self.Graph2.remove_nodes_from(high_degree_node)
			self.Graph1.add_nodes_from(high_degree_node) #Will only add edges
			self.Graph2.add_nodes_from(high_degree_node)
			if i%2!=0:
				T = TimeStep(self.Graph1, alpha, beta, self.zombies)
			else:
				T = TimeStep(self.Graph2, alpha, beta, self.zombies)
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
		if verbose:
			self.print_stats()
		return self.zombies

	def D(self, k, alpha, beta, zombies, results_path, itr, verbose=True):
		self.initialize()
		self.zombies = zombies
		values, Vec = LA.eig()
		LG1 = nx.laplacian_matrix(self.Graph1)
		LG2 = nx.laplacian_matrix(self.Graph2)
		values, VecG1 = eigs(LG1, k=1)
		values, VecG2 = eigs(LG2, k=1)
		immunized_nodesLG1 = np.argsort(-1*VecG1)[0:k]
		immunized_nodesLG2 = np.argsort(-1*VecG2)[0:k]

		self.Graph1.remove_nodes_from(immunized_nodesLG1) # Will remove edges and nodes
		self.Graph2.remove_nodes_from(immunized_nodesLG2)
		self.Graph1.add_nodes_from(immunized_nodesLG1) #Will only add edges
		self.Graph2.add_nodes_from(immunized_nodesLG2)

		self.zombies = self.start(itr, alpha, beta)
		if verbose:
			self.print_stats()
		return self.zombies







# if __name__ == '__main__':
# 	results_dir = "results/sim_results"
# 	A1 = "datasets/alternating/alternating1.network"
# 	A2 = "datasets/alternating/alternating2.network"
# 	with open("hyper_params.json") as f:
# 		hyper = json.load(f)
# 	Simulate = Policy(A1, A2, results_dir, [1, 2, 3, 5, 6])
# 	infected_nodes = Simulate.start(int(hyper['t']['1']), float(hyper['alpha']['2']), float(hyper['beta']['2']))
# 	Simulate.print_stats()




