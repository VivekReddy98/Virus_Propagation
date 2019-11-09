from utils.GenerateGraphMatrices import GenerateGraphMatrices, StrengthAlter
from utils.Simulator import Simulator
from utils.ImmunizationPolicies import Policy
import json

if __name__ == '__main__':
	# data_dir = "datasets/"
	# with open("hyper_params.json") as f:
	# 	hyper = json.load(f)
	

	# G1 = GenerateGraphMatrices()
	# G1.GenGraphObj(EdgeFilePath=data_dir+"alternating/alternating1.network")
	# S11 = G1.GenSystemMatrix(hyper['alpha']['1'], hyper['beta']['1'])
	# S12 = G1.GenSystemMatrix(hyper['alpha']['2'], hyper['beta']['2'])

	# G2 = GenerateGraphMatrices()
	# G2.GenGraphObj(EdgeFilePath=data_dir+"alternating/alternating2.network")
	# S21 = G2.GenSystemMatrix(hyper['alpha']['1'], hyper['beta']['2'])
	# S22 = G2.GenSystemMatrix(hyper['alpha']['2'], hyper['beta']['2'])

	# EffStren1 = StrengthAlter(S11, S21).value(n=2)
	# EffStren2 = StrengthAlter(S12, S22).value(n=2)
	# print(EffStren1)
	# print(EffStren2)

	results_dir = "results/sim_results"
	A1 = "datasets/alternating/alternating1.network"
	A2 = "datasets/alternating/alternating2.network"
	with open("hyper_params.json") as f:
		hyper = json.load(f)
	Simulate = Simulator(A1, A2, results_dir)
	Simulate.initialize()
	#int(hyper['t']['1'])
	infected_nodes = Simulate.start(20, float(hyper['alpha']['1']), float(hyper['beta']['1']))
	Simulate.print_stats()

	print(".............................................................................................................")

	Immunize = Policy(A1, A2, results_dir)
	infected_nodes = Immunize.A(200, float(hyper['alpha']['1']), float(hyper['beta']['1']), infected_nodes, results_dir, 20)

	print(".............................................................................................................")

	Simulate = Simulator(A1, A2, results_dir)
	Simulate.initialize()
	#int(hyper['t']['1'])
	infected_nodes = Simulate.start(20, float(hyper['alpha']['1']), float(hyper['beta']['1']))

	Immunize = Policy(A1, A2, results_dir)
	infected_nodes = Immunize.B(200, float(hyper['alpha']['1']), float(hyper['beta']['1']), infected_nodes, results_dir, 20)





