import random, math, json
from utils.GenerateGraphMatrices import GenerateGraphMatrices

class Simulator():
	def __init__(self, A1, A2, resultsPath, num_initial_nodes=None):
		self.A1 = A1 #Path to alternating1.network
		self.A2 = A2 #Path to alternating2.network
		self.results_path = resultsPath #Just a Location or directory
		self.initial_num = num_initial_nodes
		self.stats_dict = {'frac_infected':{0:0}}

	def initialize(self):
		G1 = GenerateGraphMatrices()
		G1.GenGraphObj(EdgeFilePath=self.A1)
		G2 = GenerateGraphMatrices()
		G2.GenGraphObj(EdgeFilePath=self.A2)
		self.numVertices = G1.numVertices
		if self.initial_num == None:
			self.initial_num = int(self.numVertices/10)
		self.Graph1 = G1.Graph
		self.Graph2 = G2.Graph
		self.zombies = set(random.sample([i for i in range(0, self.numVertices)], int(math.floor(self.initial_num))))
		self.stats_dict['frac_infected'][0] = self.initial_num/self.numVertices
		return None

	def start(self, num_TimeSteps, alpha, beta):
		self.initialize()
		nodes_by_time = [self.zombies]
		for i in range(1, num_TimeSteps+1):
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
		return self.zombies

	def print_stats(self):
		dict_values = self.stats_dict['frac_infected']
		for key, value in dict_values.items():
			print("At time {}, the number of nodes infected is {}".format(key, value*self.numVertices))

	def give_stats(self):
		return self.stats_dict

class TimeStep():
	def __init__(self, Graph, alpha, beta, nodes):
		self.Graph = Graph 
		self.alpha = alpha
		self.beta = beta
		self.zombies = set(nodes) # Should be a set
		self.num_zombies = len(self.zombies)
		#print(len(self.zombies))

	def recover(self):
		recovered_nodes = set(random.sample(self.zombies, int(math.ceil(self.alpha*self.num_zombies))))
		#print(len(recovered_nodes))
		self.zombies = self.zombies.difference(recovered_nodes)
		self.num_zombies = self.num_zombies - len(recovered_nodes)
		#print(len(self.zombies))
		return self.zombies

	def infect(self):
		neigh = []
		for node in self.zombies:
			neigh.extend([n for n in self.Graph.neighbors(node)])
		neigh = set(neigh)
		#print("length of nodes is {}".format(len(neigh)))
		neigh.difference(self.zombies)
		#print("length of nodes is {}".format(len(neigh)))
		zombified_nodes = set(random.sample(neigh, int(math.floor(self.beta*len(neigh)))))
		#print("length of zombified nodes is {}".format(len(zombified_nodes)))
		self.zombies = self.zombies.union(zombified_nodes)
		#print(len(self.zombies))
		return None