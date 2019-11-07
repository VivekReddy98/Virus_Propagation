import random, math, json
from utils.GenerateGraphMatrices import GenerateGraphMatrices

class Simulator():
	def __init__(self, A1, A2, resultsPath, num_initial_nodes=None):
		self.A1 = A1 #Path to alternating1.network
		self.A2 = A2 #Path to alternating2.network
		self.results_path = resultsPath #Just a Location or directory
		self.initial_num = num_initial_nodes
		self.iter = num_TimeSteps
		self.stats_dict = {'frac_infected':{0:0}}

	def initialize():
		G1 = GenerateGraphMatrices()
		G1.GenGraphObj(EdgeFilePath=self.A1)
		G2 = GenerateGraphMatrices()
		G2.GenGraphObj(EdgeFilePath=self.A2)
		self.numVertices = G1.numVertices
		if self.num_initial_nodes == None:
			self.num_initial_nodes = int(self.numVertices/10)
		self.Graph1 = G1.Graph
		self.Graph2 = G2.Graph
		self.zombies = set(random.sample([i for i in range(0, self.numVertices)], int(math.floor(self.initial_num))))
		self.stats_dict['frac_infected'][0] = self.initial_num/self.numVertices
		return None

	def start(num_TimeSteps, alpha, beta):
		self.initialize()
		nodes_by_time = [self.zombies]
		for i in range(1, num_TimeSteps+1):
			if i%2!=0:
				T = TimeStep(self.Graph1, alpha, beta, self.zombies)
			else:
				T = TimeStep(self.Graph2, alpha, beta, self.zombies)
			T.recover()
			self.zombies = T.infect()
			self.stats_dict['frac_infected'][i] = len(self.zombies)/self.numVertices
			nodes_by_time.append(self.zombies)
		print("Simulation has been completed")
		with open(self.results_path+'/simulation_stats_'+self.alpha+"_"+self.beta+".json", "w") as f:
			 json.dump(self.stats_dict, f)

		with open(self.results_path+'/nodes_by_time'+self.alpha+"_"+self.beta+".txt", 'w') as f:
			for tstp in nodes_by_time:
				for _string in tstp:
					f.write(str(_string))
				f.write("\n")
		return self.zombies

	def print_stats():
		for key, value in self.stats_dict['frac_infected']:
			print("At time {}, the frac of  nodes infected is {}".format(key, value))

class TimeStep():
	def __init__(self, Graph, alpha, beta, nodes):
		self.Graph = Graph 
		self.alpha = alpha
		self.beta = beta
		self.zombies = set(nodes) # Should be a set
		self.num_zombies = len(self.zombies)

	def recover():
		recovered_nodes = set(random.sample(self.zombies, int(math.ceil(self.alpha*self.num_zombies))))
		self.zombies.difference(recovered_nodes)
		self.num_zombies = self.num_zombies - len(recovered_nodes)
		return None 

	def infect():
		neigh = []
		for node in self.zombie_nodes:
			neigh.append([n for n in self.Graph.neighbours(node)])
		neigh = set(neigh)
		neigh.difference(self.zombies)
		zombified_nodes = set(random.sample(neigh, int(math.floor(self.beta*len(neigh)))))
		self.zombies.union(zombified_nodes)
		return self.zombies









			







