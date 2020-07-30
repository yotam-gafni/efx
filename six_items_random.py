import random
from itertools import product, combinations, permutations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import pickle
import time



arrays = []

comb_behavior = {}

global lp_runs
lp_runs = 0


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

	try:
		is_feasible = session.evaluate(wlexpr(lp_string))

		valuation = []

		for item in range(items):
			if type(is_feasible[1][item][1]) == int:
				valuation.append(is_feasible[1][item][1])
			else:
				try:
					valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])
				except Exception as e:
					#print("UNFEASIBLE CONSTRAINTS!!!!")
					return None
	except Exception as e:
		print("EXCEPTION IN GENERATE VALUATION")
		import pdb
		pdb.set_trace()

	return valuation


def reverse_comb(comb):
	new_comb = []
	for i in comb:
		new_comb.append(-i)

	return new_comb

def is_comb_in_base(comb, base):
	global lp_runs
	lp_runs += 1

	if lp_runs % 10000 == 0:
		print("LP_RUNS: {}".format(lp_runs))

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




def filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	filtered_allocs = []
	players = len(true_combs_base)
	items = len(allocs[0])

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		foundPD = False
		for comb in  all_combs_copy:
			running_ind += 1
			eq_by_player = [copy(all_zeros) for i in range(players)]

			for i in range(items):
				if alloc[i] != comb[i]:
					eq_by_player[alloc[i]][i] = 1
					eq_by_player[comb[i]][i] = -1

			isPD = True
			isSPD = False
			more_thorough = []
			for player in range(players):
				if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
					continue
				elif 1 not in eq_by_player[player]:
					isSPD = True
					continue
				elif -1 not in eq_by_player[player]:
					isPD = False
					break
				else:
					more_thorough.append(player)
			
			if isPD: 
				for player in more_thorough:
					how_many += 1
					if tuple(eq_by_player[player]) in good_combs[player]:
						isSPD = True
						continue

					elif tuple(eq_by_player[player]) in bad_combs[player]:
						isPD = False
						break

					if is_comb_in_base(eq_by_player[player], true_combs_base[player]):
						isSPD = True
						good_combs[player].add(tuple(eq_by_player[player]))
						continue
					else:
						isPD = False
						bad_combs[player].add(tuple(eq_by_player[player]))
						break

			if isPD and isSPD:
				#print("FOUND PD IN RUN INDEX {}".format(running_ind))
				#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))
				#print("alloc {} is pareto dominated by comb {}, removing".format(alloc, comb))
				foundPD = True
				break

		#print("NOT PD")
		if not foundPD:
			filtered_allocs.append(alloc)
		#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))

	return filtered_allocs

def filter_efx_envious(allocs, true_combs_base, all_combs, good_combs, bad_combs):
	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	filtered_allocs = []
	for alloc in allocs:
		all_poss_j = []
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			equ = copy(all_zeros)
			for i in range(len(alloc)):
				if alloc[i] == pair[0]:
					side1_items.append(i)
					equ[i] = 1
				elif alloc[i] == pair[1]:
					side2_items.append(i)
					equ[i] = -1

			for j in side2_items:
				curr_equ = copy(equ)
				curr_equ[j] = 0
				if sum(curr_equ) == 0 and len(set(curr_equ)) == 1:
					continue
				all_poss_j.append(tuple([pair[0], curr_equ]))

		random.shuffle(all_poss_j)
		isAlreadyJealous = False
		count_ops = 0
		for elem in all_poss_j:
			#anti_comb = reverse_comb(elem[1])
			if tuple(elem[1]) in good_combs[elem[0]]: 
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			elif tuple(elem[1]) in bad_combs[elem[0]]:
				continue
			elif is_comb_in_base(tuple(elem[1]), true_combs_base[elem[0]]):
				count_ops += 1
				good_combs[elem[0]].add(tuple(elem[1]))
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break
			else:
				bad_combs[elem[0]].add(tuple(elem[1]))
				continue
		if isAlreadyJealous == False:
			#print("alloc {} has no current envy, performed {} ops".format(alloc, count_ops))
			filtered_allocs.append(alloc)

	return filtered_allocs

def rearrange_pref(eqs, pref):

	new_eqs = []

	for eq in eqs:
		new_eq = [0] * 6
		for i in range(6):
			new_eq[pref[i]] = eq[i]

		new_eqs.append(new_eq)

	return new_eqs



players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

for items in range(6,7):

	all_combs = [item for item in product([i for i in range(players)], repeat=items)]
	all_eqs = [item for item in product([-1,0,1], repeat=items)]

	max_stop = 0
	max_conf = {}

	all_comb1 = [list(elem) for elem in permutations([2,3,4,5])]
	all_comb2 = [list(elem) for elem in permutations([1,3,4,5])]
	all_comb3 = [list(elem) for elem in permutations([1,2,4,5])]

	perm = [0,1,2,3,4,5]

	running_ind = 0
	#all_eqs = presets(perm)
	infile = open("eqs_6", "rb")
	all_eqs = pickle.load(infile)

	for running_ind in range(1000):
		preferences = []

		for j in range(3):
			random.shuffle(perm)
			preferences.append(copy(perm))

		print("Running ind: {}".format(running_ind))
		true_combs_base = {0: [], 1: [], 2: []}

		all_zeros = [0 for j in range(items)]
		good_combs = {0: set([]), 1: set([]), 2: set([])}
		evil_combs = {0: set([]), 1: set([]), 2: set([])}

		for i in range(players):
			true_combs_base[i] = []
			for j in range(items):
				unit_vector = copy(all_zeros)
				unit_vector[j] = -1
				true_combs_base[i].append(unit_vector)
				good_combs[i].add(tuple(unit_vector))
				anti_v = reverse_comb(unit_vector)
				evil_combs[i].add(tuple(anti_v))
		allocs = copy(all_combs)

		seteq1 = random.choice(all_eqs)
		seteq2 = random.choice(all_eqs)
		seteq3 = random.choice(all_eqs)

		eq_set1 = rearrange_pref(seteq1, preferences[0])
		eq_set2 = rearrange_pref(seteq2, preferences[1])
		eq_set3 = rearrange_pref(seteq3, preferences[2])


		for j in range(3):
			perm = preferences[j]

			print("Player {}, preference order {}".format(j, perm))
			for i in range(5):
				eq = [0] * 6
				eq[perm[i]] = -1
				eq[perm[i+1]] = 1
				true_combs_base[j].append(eq)
				good_combs[j].add(tuple(eq))
				anti_eq = reverse_comb(eq)
				evil_combs[j].add(tuple(anti_eq))

		for eq in eq_set1:
			anti_eq = reverse_comb(eq)
			true_combs_base[0].append(eq)
			good_combs[0].add(tuple(eq))
			anti_eq = reverse_comb(eq)
			evil_combs[0].add(tuple(anti_eq))	


		for eq in eq_set2:
			anti_eq = reverse_comb(eq)
			true_combs_base[1].append(eq)
			good_combs[1].add(tuple(eq))
			anti_eq = reverse_comb(eq)
			evil_combs[1].add(tuple(anti_eq))	


		for eq in eq_set3:
			anti_eq = reverse_comb(eq)
			true_combs_base[2].append(eq)
			good_combs[2].add(tuple(eq))
			anti_eq = reverse_comb(eq)
			evil_combs[2].add(tuple(anti_eq))


		allocs = filter_efx_envious(allocs, true_combs_base, all_combs, good_combs, evil_combs)

		if len(allocs) == 0:
			print("huh")
			import pdb
			pdb.set_trace()

		allocs = filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, evil_combs)

		if len(allocs) == 0:
			print("WOOPEE")
			import pdb
			pdb.set_trace()
		else:
			print("Allocs after filter: {}".format(len(allocs)))



