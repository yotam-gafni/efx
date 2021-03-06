import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()



arrays = []

comb_behavior = {}

def pareto_dominates(new_val, old_val):
	failed = False
	reallyGained = False
	for player in range(players):
		if new_val[player] < old_val[player]:
			failed = True
		elif new_val[player] > old_val[player]:
			reallyGained = True

	return reallyGained and not failed

def generate_valuation(base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []

	for item in range(items):
		variables.append("x{}".format(item))


	for elem in base:
		con_string = ""
		for item in range(items):
			if elem[item] == 1:
				con_string += "+ x{}".format(item)
			elif elem[item] == -1:
				con_string += "- x{}".format(item)
		constraints.append(con_string + " < 0")

	opt_goal = "5"

	constraint_string = "{" + ",".join(constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))

	valuation = []

	for item in range(items):
		if type(is_feasible[1][item][1]) == int:
			valuation.append(is_feasible[1][item][1])
		else:
			valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])

	return valuation


def reverse_comb(comb):
	new_comb = []
	for i in comb:
		new_comb.append(-i)

	return new_comb

def is_comb_in_base(comb, base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []
	item_constraints = ["" for j in range(len(comb))]
	for i in range(len(base)):
		variables.append("x{}".format(i))
		constraints.append("x{} >= 0".format(i))
		for j in range(len(comb)):
			if base[i][j] == 1:
				item_constraints[j] += "+ x{}".format(i)
			elif base[i][j] == -1:
				item_constraints[j] += " - x{}".format(i)


	opt_goal = item_constraints[0]
	for j in range(len(comb)):
		item_constraints[j] += " == {}".format(comb[j])

	all_constraints = item_constraints + constraints

	constraint_string = "{" + ",".join(all_constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))


	return type(is_feasible[0]) == int


#is_comb_in_base([0,0,1,-1,1,0],[[-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0], [0, 0, 0, -1, 0, 0], [0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, -1], [1, -1, -1, 0, 0, 1], (1, -1, 1, -1, 0, 0), (-1, 1, 0, -1, 0, 1), [1, 0, -1, -1, 1, 1], [1, -1, -1, 1, 0, -1], [0, 0, -1, 0, 0, 1], [1, 1, -1, -1, -1, 1], [1, 0, -1, 0, 1, 0], [0, -1, -1, 1, 1, 0], (0, -1, -1, -1, -1, 1), (1, 1, -1, 0, 0, 0), (-1, 0, 0, -1, 1, 1), (-1, 1, -1, 1, 0, -1), (-1, 0, -1, 0, 0, 0), (-1, 1, 0, 0, 0, -1), (1, 1, 1, -1, -1, -1), (0, 0, 0, 0, -1, 1), (-1, 1, 0, -1, 0, 0), [0, 0, 1, -1, 1, 0], [0, 1, 1, -1, 0, -1], [0, -1, -1, 0, 0, -1], (-1, 1, 1, 1, 1, 0), [0, 1, 0, 0, 0, -1], [1, 0, -1, 1, 0, 0], [-1, 0, -1, 1, 1, 0], (0, 1, 1, -1, 0, 0), (0, 0, 1, -1, 0, -1), [1, -1, 1, 0, -1, 0], [1, -1, 0, 0, 1, 1], [0, 0, -1, 1, 1, 0], [0, 0, 1, 1, 1, 1], (0, -1, 0, -1, 0, 1), (-1, -1, -1, 1, 1, -1), [0, -1, -1, 1, -1, -1], [1, 0, 0, -1, -1, 0], (0, -1, 0, -1, 1, 0), [0, -1, -1, 0, -1, 1], [1, -1, 1, 1, 0, -1], [-1, 1, 0, 0, -1, 1], (1, 1, 0, -1, -1, 0), (-1, -1, -1, 0, 0, 1), [-1, 0, 0, 0, -1, -1], [-1, 1, 1, -1, 1, 1], [1, 0, -1, 0, 0, 0], [0, -1, -1, 0, -1, 0], (0, 0, 1, 0, 1, -1), (1, -1, 1, 0, 1, -1), (1, 1, 1, 1, 1, -1), [-1, 1, 1, 1, 0, -1], (-1, -1, -1, 1, 1, 0), (-1, -1, 0, 1, -1, -1), (1, 1, -1, 1, 0, -1), (-1, 0, 0, 1, 0, 1), [1, -1, -1, 1, 0, 0], [0, 1, -1, 0, 0, -1], [1, 1, 1, -1, 0, 0], (-1, -1, 1, 0, 0, 0), (1, 0, -1, 0, 1, -1), (0, -1, 1, 1, -1, -1), (0, -1, 0, -1, -1, 1), [1, 0, 1, -1, 1, 1], [-1, 1, 0, 1, 0, -1], [1, 1, 1, 0, -1, 1], (-1, 1, 0, -1, 0, -1), [-1, 0, 1, -1, 1, 0], [0, -1, 0, -1, -1, 1], (1, 0, 0, 1, 1, -1), [-1, -1, 1, -1, -1, -1], (1, 1, -1, 0, 0, -1), [0, 0, 1, 0, 0, 1], (-1, -1, 1, -1, 1, 0), [0, -1, 0, -1, 1, 0], (-1, 1, 0, 0, -1, 0), (1, -1, 1, 1, 1, -1), [0, 0, 0, -1, 0, 0], (0, 1, 0, 0, 0, -1), (-1, 1, -1, 1, -1, 1), (1, 1, 1, -1, 1, -1), [0, 0, 0, -1, -1, 0], (-1, 1, -1, -1, -1, 1), [0, -1, -1, 0, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, -1, -1, -1, 0], [1, -1, -1, 1, 1, 0], [-1, -1, -1, 1, 0, 0], (-1, 1, -1, 1, -1, -1), (0, 0, 0, 1, 1, -1), [-1, -1, 1, 0, -1, 0], [0, 0, 0, -1, 1, 0], [1, -1, 1, 0, 0, 1], (1, 0, 0, 1, 1, 1), (0, -1, 0, 0, -1, 0), [-1, 1, 1, -1, 1, 0], [-1, 0, -1, 0, 1, -1], (-1, 0, 0, -1, -1, 0), (0, 1, 0, 1, 0, 1), [-1, 1, 1, 0, 1, 0], (1, -1, 1, -1, 1, 1), [-1, 1, 1, 0, 1, 1], (1, 1, 0, -1, -1, -1), [-1, -1, 0, 1, 1, -1], (1, 1, -1, -1, 0, 1), (1, 0, 1, -1, 1, 1), (1, 0, -1, -1, -1, -1), (-1, 1, 1, 1, 0, 1), (1, 1, -1, 0, 0, 1), (-1, 0, -1, -1, 0, 1), [0, -1, 1, 1, 0, 1], (0, 1, 1, 1, -1, -1), [-1, -1, -1, -1, 1, 0], [-1, 1, 1, 1, -1, -1], [-1, -1, 1, -1, 1, 0], (1, 0, -1, 1, -1, -1), [0, -1, 0, 0, 1, 1], [0, 0, 1, 0, 1, -1], [-1, -1, -1, 1, -1, 0], [1, -1, 0, 1, -1, 0], [0, -1, -1, 1, -1, 1], [-1, -1, -1, 0, 1, 0], [1, 0, -1, -1, 0, 0], [-1, 1, -1, 0, 0, 0], (0, 0, 1, -1, 1, 1), (0, -1, -1, 0, 0, 0), [-1, 1, -1, -1, -1, 0], [0, 1, 0, 1, 0, 0], [-1, 1, 1, -1, 1, -1], (1, 1, 1, 1, -1, 1), [1, 1, -1, -1, 0, -1], [-1, -1, 0, -1, -1, 1], [-1, 0, -1, 0, -1, 0], [1, 0, 1, -1, 0, 0], [1, -1, 1, 1, 1, 1], [-1, 1, -1, 0, 0, -1], [0, -1, 1, 0, 1, -1], [-1, 0, -1, 1, -1, 0], (0, -1, 0, -1, 1, 1), [-1, 0, 0, -1, -1, 0], [-1, -1, 0, -1, 0, -1], [0, 1, 1, 0, 1, 1], [-1, 0, 1, -1, 1, -1], [-1, 0, 0, 0, 0, -1], (-1, 1, 1, -1, 1, 1), (0, -1, 0, 0, 1, 0), (-1, 0, 1, 0, -1, -1), [1, 1, 1, 1, 1, 1], [-1, 0, 0, 1, -1, 1], (0, -1, -1, -1, 0, -1), [-1, 0, 1, -1, 0, -1], [-1, 1, 1, 0, 0, 0], [1, -1, 0, 1, -1, 1], [0, 0, 1, 0, -1, 0], (1, 1, 0, 1, -1, 0), (0, 1, 0, -1, -1, 1), [1, 1, 1, 0, 1, 1], (-1, 1, 1, 1, 0, -1), (-1, -1, -1, -1, 1, 0), [0, 1, -1, -1, 1, 0], (1, 1, 0, -1, 0, -1), (0, 1, -1, 1, -1, -1), [1, 1, 1, 0, 1, 0], (-1, -1, 0, 0, 1, 1), (1, 1, -1, -1, -1, 0), [0, -1, 1, 1, -1, -1], (1, 1, 0, 1, 0, -1), [1, 0, 1, -1, 0, 1], [1, -1, -1, 0, 1, 1], [1, 1, 0, -1, 0, 0], (1, -1, 0, 0, -1, 0), (0, 0, 1, 1, -1, 0), (-1, 0, 1, 0, 0, 1), (1, -1, -1, 1, 0, -1), (1, -1, -1, 1, 1, 0), [0, -1, 1, 0, 1, 0], (0, -1, 1, 1, 0, 1), [0, 1, 0, 0, 0, 0], (-1, 1, -1, 1, -1, 0), (-1, 0, 1, -1, 0, -1), [1, 1, 0, 0, 0, 1], [1, 1, -1, 1, 1, 0], (-1, -1, 1, 0, 0, 1), (0, 1, 1, 0, 0, -1), (1, 1, 0, 0, 1, 0), (1, 0, 0, 0, 1, 0), [-1, -1, 1, -1, 1, 1], (0, 1, -1, -1, 0, 1), (-1, 0, 1, 1, 1, -1), [1, 1, -1, 1, 1, -1], [-1, 0, -1, -1, 1, 0], [0, 1, 1, -1, 0, 0], (1, 0, -1, 1, 0, -1), (1, -1, 0, 0, -1, 1), (-1, -1, 1, -1, 0, -1), (-1, 1, 1, -1, -1, -1), (0, 0, -1, -1, 0, -1), (1, 1, -1, 0, -1, -1), [0, -1, 0, 1, 0, 1], (-1, 1, 0, -1, -1, 0), (0, 1, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (1, -1, -1, 0, 1, -1), [0, 0, 1, 0, 0, -1], (0, -1, -1, 0, 0, -1), [0, -1, -1, -1, -1, 0], [1, 1, -1, -1, 0, 1], (-1, -1, -1, -1, 0, 1), (-1, -1, 1, -1, 1, -1), [1, 0, 0, -1, 0, 1], [1, 0, 0, 1, 1, 1], [1, -1, -1, -1, 0, 0], [-1, 0, -1, 0, 0, 1], [-1, 0, 1, 1, -1, 0], [-1, 0, 1, 0, 1, -1], [0, 1, -1, 1, -1, -1], [-1, -1, 0, 0, 1, 1], [1, -1, 1, -1, -1, -1], [-1, -1, 1, 0, 1, -1], [-1, 0, -1, 0, 0, -1], [0, -1, 1, 1, 0, 0], [1, 1, 0, -1, -1, -1], (1, 0, -1, 0, 0, 0), [-1, 0, 1, 0, 1, 0], [0, 1, 1, 0, -1, -1], (1, 1, 0, 0, 0, 1), [-1, -1, -1, 0, 0, 0], (-1, -1, 0, -1, 0, 0), [0, -1, 0, -1, 0, 0], (-1, -1, 1, 0, -1, 0), [-1, 1, 0, -1, 0, 1], (1, -1, 1, 0, -1, 0), [1, 1, -1, 0, 0, 1], (1, 0, 1, 0, 1, -1), [1, 0, 0, 0, -1, 0], [-1, 0, 0, 0, 1, 1], [1, 1, 0, -1, 0, -1], (-1, 0, 0, -1, 1, 0), (-1, -1, 1, 0, 1, 1), (0, -1, 1, -1, 0, -1), (1, -1, 0, -1, 1, 1), [0, 0, -1, -1, 1, -1], (-1, -1, 0, -1, 0, -1), (-1, 1, 1, 0, -1, 0), (-1, 0, -1, 0, 1, 1), [-1, -1, -1, 0, -1, 0], (0, 1, 1, -1, 0, -1), (-1, 0, 0, 0, 0, -1), (0, -1, -1, -1, 1, 1), [-1, 0, 1, 0, -1, -1], (-1, -1, 0, -1, 1, -1), [0, 1, -1, 1, -1, 0], (-1, -1, -1, 0, 0, 0), [0, 0, 1, -1, -1, 0], [0, 0, 1, 0, 0, 0], [0, 0, -1, 0, 1, 1], [0, -1, 0, 0, -1, 1], [0, -1, -1, -1, -1, 1], [1, 0, -1, 0, -1, 1], [0, -1, -1, 1, 1, -1], [0, 1, 0, 1, 1, 1], [0, 1, 0, -1, 1, -1], [1, 0, 1, -1, -1, 1], (1, 0, -1, 1, 1, 1), [0, -1, 1, 0, -1, -1], (1, 0, -1, 1, 1, 0), (1, 0, 1, -1, 0, -1), (1, -1, 1, 0, 1, 0), [0, 0, 0, -1, 0, -1], (0, -1, 0, 0, 0, -1), (0, 1, 1, -1, -1, -1), (1, 0, 1, 0, -1, -1), (1, 0, 0, 0, 1, -1), (-1, -1, -1, 1, -1, -1), [-1, 1, -1, 1, 0, -1], (-1, -1, 0, -1, 0, 1), [0, -1, 1, -1, -1, 0], (-1, 1, 0, 0, 1, 0), (1, -1, -1, -1, -1, 1), (0, 1, -1, 0, 1, -1), [1, -1, 0, 1, -1, -1], [0, -1, -1, -1, 1, 0], [-1, 1, 0, 0, 0, 0], [0, 1, 0, 0, -1, -1], [0, 1, 0, 1, 1, 0], [0, 0, -1, 0, -1, 0], [-1, 1, 1, 0, -1, 0], [1, 0, 1, 1, -1, 1], (-1, -1, 1, 0, 1, 0), (0, -1, 1, 1, 0, -1), [-1, -1, 1, 1, 1, 1], [1, -1, -1, 0, -1, 1], [-1, -1, 0, 0, 1, 0], (1, 0, 1, 0, 1, 1), (1, 0, -1, -1, -1, 0), [0, 1, 0, 1, -1, 1]])



players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

items = 9
all_combs = [item for item in product([i for i in range(players)], repeat=items)]

random.shuffle(all_combs)

efx_combs = []

#valuations = {0: [8,2,12,2,0,17,1],1: [5,0,9,4,10,0,3],2: [0,0,0,0,9,10,2]}
#valuations = {0: [1.02, 5.01, 5, 1, 3,0.009,0.009,0], 1: [1, 0.375, 1.3, 0.125, 0.125,0,0,0], 2: [1, 5.01, 4.5, 3, 1.1,0.01,0.1,0.01]}
#valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.001], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0],3:[0,0,0,0.01,0,0,0,0,0]}
#valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1]}
#valuations = {0: [1.02, 5.01, 1, 1, 3,0.009], 1: [1, 0.375, 1.15, 0.125, 0.125,0.001], 2: [1, 5.01, 3, 3, 1.1,0.1]}
#valuations = {0: [1.02, 5.01, 1, 1, 3], 1: [1, 0.375, 1.15, 0.125, 0.125], 2: [1, 5.01, 3, 3, 1.1]}
#valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.01], 1: [1, 1.1, 1.15, 0.125, 0.125,0,0,0,0.01], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0]}#valuations = {0: [1.02, 5.01, 1, 1, 3,0.0001,0.0003,0,0.0027], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0]}
#valuations = {0: [1, 5.1, 5, 1, 3,0.001], 1: [1, 0.375, 1.3, 0.125, 0.125,0.001], 2: [1, 5, 4.5, 3, 1,0.001]}

#valuations = {0: [1, 5.1, 5, 1, 3,0.2], 1: [1, 0.375, 1.3, 0.125, 0.125, 0], 2: [1, 5, 4.5, 3, 1, 0]}
epsilon = 0.0001
#valuations = {0: [1, 5.1, 5, 1, 3], 1: [1, 0.375, 1.3, 0.125, 0.125], 2: [1, 5, 4.5, 3, 1]}
#valuations = {0: [30,26,20,5,25,30], 1: [100,120,100,5,40,20], 2: [4,8,4,10,5,5]}

# 3 EFX + PO
#valuations = {0: [30,26,20,5,25,30], 1: [100,120,100,5,90,30], 2: [4,8,4,9,5,5]}

# 2 EFX + PO ATTEMPT
#valuations = {0: [1, 5.1, 5, 1, 3], 1: [1, 0.375, 1.3, 0.125, 0.125], 2: [1, 5, 4.5, 3, 1]}


#valuations = {0: [1, 0.9765625, 1.8125, 1.5, 1.4375, 2.3203125], 1: [1, 3.6666666666666665, 1, 3, 1.3333333333333333, 0.3333333333333333], 2: [1, 4.25, 3.75, 0.625, 3, 6.25]}
#valuations = {0: [-1, -7.5, -6, -2, -3.5], 1: [1, 0.7125, 1.6625, 0.08125, 0.08125], 2: [1, 6.5, 5.75, 4, 1.25]}
#valuations = {0: [1, 7.25, 6.5, 1.25, 4], 1: [1, 0.5223214285714286, 1.3947704081632653, 0.16358418367346939, 0.1482780612244898], 2: [1, 6, 5.375, 3.75, 1.125]}
#valuations = {0: [1, 5.1, 5, 1, 3], 1: [1, 0.375, 1.3, 0.125, 0.125], 2: [1, 5, 4.5, 3, 1]}
#valuations = {0: [1, 5.75, 4.5, 0.5, 3.75], 1: [1, 0.71875, 1.6458333333333333, 0.13020833333333334, 0.08854166666666667], 2: [1, 5.25, 5, 3.375, 1.125]}
#valuations = {0: [1, 17, 13, 4.5, 6.5], 1: [1, 0.4107142857142857, 1.4017857142857142, 0.13392857142857142, 0.20535714285714285], 2: [1, 5.75, 5.25, 3.75, 1.25]}
#valuations = {0: [1, 20, 14, 4, 8], 1: [1, 0.96875, 2.53125, 0.875, 0.625], 2: [1, 5.625, 5, 3.75, 1.125]}
#valuations = {0: [1, 41, 27, 4.5, 29.5, 9], 1: [1, 0.140625, 3.15625, 0.109375, 0.703125, 0.203125], 2: [1, 18.25, 13.75, 5.625, 3.625, 4]}
#valuations = {0: [1, 15.5, 15.125, 3.25, 6.875, 4.5], 1: [1, 0.40080782312925173, 3.1193027210884354, 0.22517006802721087, 0.2302721088435374, 0.26305272108843536], 2: [1, 16.25, 9.5, 1.625, 1.875, 5.5]}
#valuations = {0: [1, 15.5, 15.125, 3.25, 6.875, 4.5], 1: [1, 0.40080782312925173, 3.1193027210884354, 0.22517006802721087, 0.2302721088435374, 0.26305272108843536], 2: [1, 16.25, 9.5, 1.625, 1.875, 5.5]}
#valuations = {0: [1, 3.3854166666666665, 3.03125, 0.5208333333333334, 1.3958333333333333, 0.22916666666666666], 1: [1, 0.40595238095238095, 2.2220238095238094, 0.22380952380952382, 0.039285714285714285, 0.611904761904762], 2: [1, 4.59375, 4.28125, 0.8125, 1.7291666666666667, 1.1458333333333333]}
#valuations = {0: [1, 14, 10.875, 3.5625, 5.4375, 1.375], 1: [1, 0.4041666666666667, 2.2158854166666666, 0.22291666666666668, 0.0421875, 0.6098958333333333], 2: [1, 4.5625, 4.3125, 0.7916666666666666, 1.75, 1.1666666666666667]}
#valuations = {0: [1, 15.25, 14.875, 3.25, 6.75, 4.075, 0.3], 1: [1, 0.27291666666666664, 2.75, 0.15208333333333332, 0.15208333333333332, 0.17291666666666666, 0.00001], 2: [1, 21.25, 12, 2.75, 2, 6.75, 1]}
#valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.01], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1, 5.01, 3, 3, 1.1,0.01,0.1,0.01,0]}
#valuations = {0: [1, 8.9375, 7.875, 3.5625, 3.4375, 1.4375,0], 1: [1, 0.8145833333333333, 3.221875, 0.68125, 0.38125, 0.5354166666666667,0], 2: [1, 5.041666666666667, 4.75, 0.5833333333333334, 1.6458333333333333, 1.8125, 0.1]}
#valuations = {0: [1, 5.559895833333333, 6.105729166666666, 0.2557291666666667, 2.0494791666666665, 1.3708333333333333, 1.5536458333333334], 1: [1, 5.536147186147186, 6.612337662337662, 1.8571428571428572, 1.3417748917748917, 1.5372294372294372, 0.01103896103896104], 2: [1, 5.801897321428571, 3.7631138392857144, 0.012834821428571428, 2.1679129464285716, 2.3016183035714284, 0.4330357142857143]}
#valuations = {0: [1, 6.520833333333333, 7.271527777777778, 1.2416666666666667, 1.8125, 1.054861111111111, 2.290277777777778], 1: [1, 6.1953125, 7.5390625, 2.2265625, 1.84375, 0.125, 0.2265625], 2: [1, 8.895833333333334, 6.1875, 0.026041666666666668, 2.75, 2.4322916666666665, 0.40625]}
#valuations = {0: [1, 6.520833333333333, 7.271527777777778, 1.2416666666666667, 1.8125, 1.054861111111111, 2.290277777777778, 0.3], 1: [1, 6.1953125, 7.5390625, 2.2265625, 1.84375, 0.125, 0.2265625, 0], 2: [1, 8.895833333333334, 6.1875, 0.026041666666666668, 2.75, 2.4322916666666665, 0.40625, 0]}
#valuations = {0: [1, 6.204861111111111, 6.846875, 1.1395833333333334, 1.6875, 1.0315972222222223, 2.1586805555555557], 1: [1, 6.859375, 8.078125, 2.5208333333333335, 2.2604166666666665, 0.078125, 0.16145833333333334], 2: [1, 10.58203125, 7.154947916666667, 0.0078125, 2.96875, 3.1822916666666665, 0.7161458333333334]}
#valuations = {0: [1, 2.125, 1, 1, 2.5, 1.75], 1: [1, 1, 1.5, 1, 1, 2], 2: [1, 1.8125, 1, 1.5625, 1, 1.5]}
#valuations = {0: [1, 2.25, 2.75, 2, 1, 2.5], 1: [1, 0.5, 2.625, 3.25, 2.5, 0.75], 2: [1, 0.5, 0.6875, 1.4375, 1.5625, 0.625]}
#valuations = {0: [1, 1.84375, 0.5, 2.25, 2, 2.28125], 1: [1, 1, 1, 1.375, 1.75, 1.5], 2: [1, 0.7552083333333334, 0.16666666666666666, 0.4947916666666667, 0.3697916666666667, 0.22916666666666666]}
#valuations = {0: [1, 0.5, 0.390625, 0.6875, 0.9375, 1.015625], 1: [1, 1.9375, 1, 0.5, 1.875, 1.625], 2: [1, 0.6875, 2.4375, 4, 0.9375, 2.9375]}
#valuations = {0: [1, 1.8125, 1, 2.5625, 2, 2.5], 1: [1, 0.96875, 0.25, 0.125, 0.65625, 0.1875], 2: [1, 1, 2, 1.75, 1.625, 1.5]}
#valuations = {0: [1, 4, 12, 14, 9, 10, 13], 1: [1, 0.7265625, 0.0078125, 1.0286458333333333, 1.703125, 1.4453125, 1.1953125], 2: [1, 1, 3.75, 6.75, 2.75, 6.25, 7]}
#valuations = {0: [1, 1.84375, 0.5, 2.25, 2, 2.28125], 1: [1, 1, 1, 1.375, 1.75, 1.5], 2: [1, 0.7552083333333334, 0.16666666666666666, 0.4947916666666667, 0.3697916666666667, 0.22916666666666666]}
#valuations = {0: [1, 1.8125, 1, 2.5625, 2, 2.5], 1: [1, 0.96875, 0.25, 0.125, 0.65625, 0.1875], 2: [1, 1, 2, 1.75, 1.625, 1.5]}

#valuations = {0: [1, 1.5, 1.6328125, 0.921875, 1.8828125, 3.390625, 3.328125], 1: [1, 11, 20, 7, 22, 19, 4], 2: [1, 0.5078125, 0.9635416666666666, 0.5364583333333334, 0.5520833333333334, 0.7135416666666666, 0.8385416666666666]}
#valuations = {0: [1, 0.853515625, 1.048828125, 0.095703125, 1.775390625, 1.791015625], 1: [1, 0.6517676767676768, 0.5393642305407012, 0.3667260843731432, 0.5804292929292929, 0.261712715389186], 2: [1, 0.2048611111111111, 1.671875, 1.7048611111111112, 0.7881944444444444, 1.0052083333333333]}

#valuations = {0: [1, 2.6666666666666665, 2.5208333333333335, 2.1979166666666665, 2.28125, 3.40625], 1: [1, 0.399375, 0.2075, 0.415, 0.631875, 0.49], 2: [1, 0.45476190476190476, 1.2976190476190477, 1.0946428571428573, 0.6934523809523809, 0.6755952380952381]}
#valuations = {0: [1, 0.109375, 0.359375, 0.125, 0.16666666666666666, 0.421875, 0.609375], 1: [1, 0.0625, 0.30439453125, 0.35947265625, 0.56435546875, 0.18173828125, 1.0328125], 2: [1, 0.21614583333333334, 0.5338541666666666, 0.2786458333333333, 1.0416666666666667, 0.21614583333333334, 1.5442708333333333]}
#valuations = {0: [1, 0.853515625, 1.048828125, 0.095703125, 1.775390625, 1.791015625, 0.3], 1: [1, 0.6517676767676768, 0.5393642305407012, 0.3667260843731432, 0.5804292929292929, 0.261712715389186, 0], 2: [1, 0.2048611111111111, 1.671875, 1.7048611111111112, 0.7881944444444444, 1.0052083333333333, 0]}

#valuations = {0: [1, 13.5, 4.5, 6.5, 14.5, 3.5, 15], 1: [1, 12, 4.5, 2.5, 20, 5.5, 19.5], 2: [1, 9.5, 6.25, 1, 5.25, 1, 8.75]}
#valuations = {0: [1, 0.5013020833333334, 0.8197544642857143, 0.125, 0.9665178571428571, 1.2771577380952381, 0.24590773809523808, 0.017857142857142856], 1: [1, 0.1, 2.565625, 0.565625, 2.832291666666667, 2.1875, 0.13645833333333332, 0.005208333333333333], 2: [1, 0.25370592948717946, 0.9791666666666666, 0.7771434294871795, 0.8147536057692307, 1.7819511217948718, 0.19200721153846154, 0.06104767628205128]}
#valuations = {0: [1, 9, 4, 8, 14, 16, 1], 1: [1, 6, 6, 12, 9, 19, 1], 2: [1, 1, 3.875, 6.125, 3.75, 9.125, 1]}
#valuations = {0: [1, 4, 11, 6, 3, 15, 10], 1: [1, 7.5, 4.5, 3, 7, 2, 0.5], 2: [1, 0.5, 0.25, 0.9375, 0.625, 0.25, 0.125]}
#valuations = {0: [1, 3.75, 9.875, 5.75, 3, 6.375, 1], 1: [1, 7.5, 4.5, 3, 7, 2, 0.5], 2: [1, 0.5, 0.25, 0.9375, 0.625, 0.25, 0.125]}


#valuations = {0: [1, 4, 13, 6, 3, 4.5, 25], 1: [1, 7.5, 4.5, 3, 7, 2, 0.5], 2: [1, 0.5, 0.25, 0.9375, 0.625, 0.25, 0.125]}

#valuations = {0: [30,26,20,5,20,25], 1: [100,120,100,5,100,20], 2: [4,8,4,10,4,5]}

#valuations = {0: [1, 0.853515625, 1.048828125, 0.095703125, 1.775390625, 1.791015625], 1:[1, 0.6517676767676768, 0.5393642305407012, 0.3667260843731432, 0.5804292929292929,0.261712715389186], 2: [1, 0.2048611111111111, 1.671875, 1.7048611111111112,0.7881944444444444, 1.0052083333333333]}

#valuations = {0: [1, 0.8535, 1.0488, 0.0957, 1.7753, 1.7910], 1:[1, 0.6517, 0.5393, 0.3667, 0.5804,0.2617], 2: [1, 0.2048, 1.671, 1.7048,0.7881, 1.0052]}

#valuations = {0: [20,27,23,28,1, 1], 1:[12,28,6,28,21,5], 2:[15,8,9,23,8,37]}

#valuations = {0: [1, 0.9375, 0.90625, 0.7291666666666666, 0.6770833333333334, 0.5520833333333334, 0.4791666666666667], 1: [1, 0.9270833333333334, 0.8880208333333334, 0.9583333333333334, 0.7369791666666666, 1.125, 0.9192708333333334], 2: [1, 0.75, 0.8125, 0.78125, 1.5, 0.875, 0.765625]}
#valuations = {0: [1, 0.6145833333333334, 0.3229166666666667, 0.19791666666666666, 0.13541666666666666, 0.125], 1: [1, 0.3125, 0.8125, 0.0625, 0.03125, 0.015625], 2: [1, 0.71875, 0.46875, 0.96875, 0.59375, 0.21875]}
valuations = {0: [1.02, 5.01, 1, 1, 3,0.009,0.009,0,0.01], 1: [1, 0.375, 1.15, 0.125, 0.125,0,0,0,0], 2: [1 + epsilon/2, 5.01 + epsilon, 3 + epsilon, 3.05 + epsilon, 1.1 + epsilon,0.005 + epsilon,0.1 + epsilon/2,0.02 + epsilon,0 + epsilon]}



all_zeros = [0 for j in range(items)]

part_val = [22,15,10]

for comb in all_combs:
	all_poss_j = []
	isAlreadyJealous = False
	for pair in all_pairs:
		side1_items = []
		side2_items = []
		for i in range(len(comb)):
			if comb[i] == pair[0]:
				side1_items.append(i)
			elif comb[i] == pair[1]:
				side2_items.append(i)
		val_side1 = 0
		for side1_item in side1_items:
			val_side1 += valuations[pair[0]][side1_item]
		for j in range(len(side2_items)):
			val_side2 = 0
			for side2_item in (side2_items[:j] + side2_items[j+1:]):
				val_side2 += valuations[pair[0]][side2_item]

			if val_side2 > val_side1:
				isAlreadyJealous = True


	if isAlreadyJealous == False:
		efx_combs.append(comb)

efx_valuations = []
for comb in efx_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)
	efx_valuations.append([new_val, comb])

#print(efx_valuations)
#print(efx_combs)

old_efx_valuations = copy(efx_valuations)

print("All EFX Valuations: {}".format(old_efx_valuations))
for comb in all_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)

	new_efx_valuations = []
	for e_val, e_comb in efx_valuations:
		if not pareto_dominates(new_val, e_val):
			new_efx_valuations.append([e_val, e_comb])
		#else:
		#	print("EFX comb {} with values {} superseded by {} due to combination {}".format(e_comb, e_val, new_val, comb))
	efx_valuations = new_efx_valuations
	if efx_valuations == []:
		print("REALLY??")
		import pdb
		pdb.set_trace()
print("EFX+PO Valuations: {}".format(efx_valuations))
max_ev = 0
ev_instance = []
for ev in old_efx_valuations:
	if sum(ev[0]) > max_ev:
		max_ev = sum(ev[0])
		ev_instance = ev

print("MAX {}, {}".format(max_ev, ev_instance))

import pdb
pdb.set_trace()
