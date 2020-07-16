import random
from itertools import product, combinations, permutations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import time


arrays = []

comb_behavior = {}

global lp_runs
lp_runs = 0

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
					for i in range(1000):
						print("UNFEASIBLE CONSTRAINTS!!!!")
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


#is_comb_in_base([0,0,1,-1,1,0],[[-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0], [0, 0, 0, -1, 0, 0], [0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, -1], [1, -1, -1, 0, 0, 1], (1, -1, 1, -1, 0, 0), (-1, 1, 0, -1, 0, 1), [1, 0, -1, -1, 1, 1], [1, -1, -1, 1, 0, -1], [0, 0, -1, 0, 0, 1], [1, 1, -1, -1, -1, 1], [1, 0, -1, 0, 1, 0], [0, -1, -1, 1, 1, 0], (0, -1, -1, -1, -1, 1), (1, 1, -1, 0, 0, 0), (-1, 0, 0, -1, 1, 1), (-1, 1, -1, 1, 0, -1), (-1, 0, -1, 0, 0, 0), (-1, 1, 0, 0, 0, -1), (1, 1, 1, -1, -1, -1), (0, 0, 0, 0, -1, 1), (-1, 1, 0, -1, 0, 0), [0, 0, 1, -1, 1, 0], [0, 1, 1, -1, 0, -1], [0, -1, -1, 0, 0, -1], (-1, 1, 1, 1, 1, 0), [0, 1, 0, 0, 0, -1], [1, 0, -1, 1, 0, 0], [-1, 0, -1, 1, 1, 0], (0, 1, 1, -1, 0, 0), (0, 0, 1, -1, 0, -1), [1, -1, 1, 0, -1, 0], [1, -1, 0, 0, 1, 1], [0, 0, -1, 1, 1, 0], [0, 0, 1, 1, 1, 1], (0, -1, 0, -1, 0, 1), (-1, -1, -1, 1, 1, -1), [0, -1, -1, 1, -1, -1], [1, 0, 0, -1, -1, 0], (0, -1, 0, -1, 1, 0), [0, -1, -1, 0, -1, 1], [1, -1, 1, 1, 0, -1], [-1, 1, 0, 0, -1, 1], (1, 1, 0, -1, -1, 0), (-1, -1, -1, 0, 0, 1), [-1, 0, 0, 0, -1, -1], [-1, 1, 1, -1, 1, 1], [1, 0, -1, 0, 0, 0], [0, -1, -1, 0, -1, 0], (0, 0, 1, 0, 1, -1), (1, -1, 1, 0, 1, -1), (1, 1, 1, 1, 1, -1), [-1, 1, 1, 1, 0, -1], (-1, -1, -1, 1, 1, 0), (-1, -1, 0, 1, -1, -1), (1, 1, -1, 1, 0, -1), (-1, 0, 0, 1, 0, 1), [1, -1, -1, 1, 0, 0], [0, 1, -1, 0, 0, -1], [1, 1, 1, -1, 0, 0], (-1, -1, 1, 0, 0, 0), (1, 0, -1, 0, 1, -1), (0, -1, 1, 1, -1, -1), (0, -1, 0, -1, -1, 1), [1, 0, 1, -1, 1, 1], [-1, 1, 0, 1, 0, -1], [1, 1, 1, 0, -1, 1], (-1, 1, 0, -1, 0, -1), [-1, 0, 1, -1, 1, 0], [0, -1, 0, -1, -1, 1], (1, 0, 0, 1, 1, -1), [-1, -1, 1, -1, -1, -1], (1, 1, -1, 0, 0, -1), [0, 0, 1, 0, 0, 1], (-1, -1, 1, -1, 1, 0), [0, -1, 0, -1, 1, 0], (-1, 1, 0, 0, -1, 0), (1, -1, 1, 1, 1, -1), [0, 0, 0, -1, 0, 0], (0, 1, 0, 0, 0, -1), (-1, 1, -1, 1, -1, 1), (1, 1, 1, -1, 1, -1), [0, 0, 0, -1, -1, 0], (-1, 1, -1, -1, -1, 1), [0, -1, -1, 0, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, -1, -1, -1, 0], [1, -1, -1, 1, 1, 0], [-1, -1, -1, 1, 0, 0], (-1, 1, -1, 1, -1, -1), (0, 0, 0, 1, 1, -1), [-1, -1, 1, 0, -1, 0], [0, 0, 0, -1, 1, 0], [1, -1, 1, 0, 0, 1], (1, 0, 0, 1, 1, 1), (0, -1, 0, 0, -1, 0), [-1, 1, 1, -1, 1, 0], [-1, 0, -1, 0, 1, -1], (-1, 0, 0, -1, -1, 0), (0, 1, 0, 1, 0, 1), [-1, 1, 1, 0, 1, 0], (1, -1, 1, -1, 1, 1), [-1, 1, 1, 0, 1, 1], (1, 1, 0, -1, -1, -1), [-1, -1, 0, 1, 1, -1], (1, 1, -1, -1, 0, 1), (1, 0, 1, -1, 1, 1), (1, 0, -1, -1, -1, -1), (-1, 1, 1, 1, 0, 1), (1, 1, -1, 0, 0, 1), (-1, 0, -1, -1, 0, 1), [0, -1, 1, 1, 0, 1], (0, 1, 1, 1, -1, -1), [-1, -1, -1, -1, 1, 0], [-1, 1, 1, 1, -1, -1], [-1, -1, 1, -1, 1, 0], (1, 0, -1, 1, -1, -1), [0, -1, 0, 0, 1, 1], [0, 0, 1, 0, 1, -1], [-1, -1, -1, 1, -1, 0], [1, -1, 0, 1, -1, 0], [0, -1, -1, 1, -1, 1], [-1, -1, -1, 0, 1, 0], [1, 0, -1, -1, 0, 0], [-1, 1, -1, 0, 0, 0], (0, 0, 1, -1, 1, 1), (0, -1, -1, 0, 0, 0), [-1, 1, -1, -1, -1, 0], [0, 1, 0, 1, 0, 0], [-1, 1, 1, -1, 1, -1], (1, 1, 1, 1, -1, 1), [1, 1, -1, -1, 0, -1], [-1, -1, 0, -1, -1, 1], [-1, 0, -1, 0, -1, 0], [1, 0, 1, -1, 0, 0], [1, -1, 1, 1, 1, 1], [-1, 1, -1, 0, 0, -1], [0, -1, 1, 0, 1, -1], [-1, 0, -1, 1, -1, 0], (0, -1, 0, -1, 1, 1), [-1, 0, 0, -1, -1, 0], [-1, -1, 0, -1, 0, -1], [0, 1, 1, 0, 1, 1], [-1, 0, 1, -1, 1, -1], [-1, 0, 0, 0, 0, -1], (-1, 1, 1, -1, 1, 1), (0, -1, 0, 0, 1, 0), (-1, 0, 1, 0, -1, -1), [1, 1, 1, 1, 1, 1], [-1, 0, 0, 1, -1, 1], (0, -1, -1, -1, 0, -1), [-1, 0, 1, -1, 0, -1], [-1, 1, 1, 0, 0, 0], [1, -1, 0, 1, -1, 1], [0, 0, 1, 0, -1, 0], (1, 1, 0, 1, -1, 0), (0, 1, 0, -1, -1, 1), [1, 1, 1, 0, 1, 1], (-1, 1, 1, 1, 0, -1), (-1, -1, -1, -1, 1, 0), [0, 1, -1, -1, 1, 0], (1, 1, 0, -1, 0, -1), (0, 1, -1, 1, -1, -1), [1, 1, 1, 0, 1, 0], (-1, -1, 0, 0, 1, 1), (1, 1, -1, -1, -1, 0), [0, -1, 1, 1, -1, -1], (1, 1, 0, 1, 0, -1), [1, 0, 1, -1, 0, 1], [1, -1, -1, 0, 1, 1], [1, 1, 0, -1, 0, 0], (1, -1, 0, 0, -1, 0), (0, 0, 1, 1, -1, 0), (-1, 0, 1, 0, 0, 1), (1, -1, -1, 1, 0, -1), (1, -1, -1, 1, 1, 0), [0, -1, 1, 0, 1, 0], (0, -1, 1, 1, 0, 1), [0, 1, 0, 0, 0, 0], (-1, 1, -1, 1, -1, 0), (-1, 0, 1, -1, 0, -1), [1, 1, 0, 0, 0, 1], [1, 1, -1, 1, 1, 0], (-1, -1, 1, 0, 0, 1), (0, 1, 1, 0, 0, -1), (1, 1, 0, 0, 1, 0), (1, 0, 0, 0, 1, 0), [-1, -1, 1, -1, 1, 1], (0, 1, -1, -1, 0, 1), (-1, 0, 1, 1, 1, -1), [1, 1, -1, 1, 1, -1], [-1, 0, -1, -1, 1, 0], [0, 1, 1, -1, 0, 0], (1, 0, -1, 1, 0, -1), (1, -1, 0, 0, -1, 1), (-1, -1, 1, -1, 0, -1), (-1, 1, 1, -1, -1, -1), (0, 0, -1, -1, 0, -1), (1, 1, -1, 0, -1, -1), [0, -1, 0, 1, 0, 1], (-1, 1, 0, -1, -1, 0), (0, 1, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (1, -1, -1, 0, 1, -1), [0, 0, 1, 0, 0, -1], (0, -1, -1, 0, 0, -1), [0, -1, -1, -1, -1, 0], [1, 1, -1, -1, 0, 1], (-1, -1, -1, -1, 0, 1), (-1, -1, 1, -1, 1, -1), [1, 0, 0, -1, 0, 1], [1, 0, 0, 1, 1, 1], [1, -1, -1, -1, 0, 0], [-1, 0, -1, 0, 0, 1], [-1, 0, 1, 1, -1, 0], [-1, 0, 1, 0, 1, -1], [0, 1, -1, 1, -1, -1], [-1, -1, 0, 0, 1, 1], [1, -1, 1, -1, -1, -1], [-1, -1, 1, 0, 1, -1], [-1, 0, -1, 0, 0, -1], [0, -1, 1, 1, 0, 0], [1, 1, 0, -1, -1, -1], (1, 0, -1, 0, 0, 0), [-1, 0, 1, 0, 1, 0], [0, 1, 1, 0, -1, -1], (1, 1, 0, 0, 0, 1), [-1, -1, -1, 0, 0, 0], (-1, -1, 0, -1, 0, 0), [0, -1, 0, -1, 0, 0], (-1, -1, 1, 0, -1, 0), [-1, 1, 0, -1, 0, 1], (1, -1, 1, 0, -1, 0), [1, 1, -1, 0, 0, 1], (1, 0, 1, 0, 1, -1), [1, 0, 0, 0, -1, 0], [-1, 0, 0, 0, 1, 1], [1, 1, 0, -1, 0, -1], (-1, 0, 0, -1, 1, 0), (-1, -1, 1, 0, 1, 1), (0, -1, 1, -1, 0, -1), (1, -1, 0, -1, 1, 1), [0, 0, -1, -1, 1, -1], (-1, -1, 0, -1, 0, -1), (-1, 1, 1, 0, -1, 0), (-1, 0, -1, 0, 1, 1), [-1, -1, -1, 0, -1, 0], (0, 1, 1, -1, 0, -1), (-1, 0, 0, 0, 0, -1), (0, -1, -1, -1, 1, 1), [-1, 0, 1, 0, -1, -1], (-1, -1, 0, -1, 1, -1), [0, 1, -1, 1, -1, 0], (-1, -1, -1, 0, 0, 0), [0, 0, 1, -1, -1, 0], [0, 0, 1, 0, 0, 0], [0, 0, -1, 0, 1, 1], [0, -1, 0, 0, -1, 1], [0, -1, -1, -1, -1, 1], [1, 0, -1, 0, -1, 1], [0, -1, -1, 1, 1, -1], [0, 1, 0, 1, 1, 1], [0, 1, 0, -1, 1, -1], [1, 0, 1, -1, -1, 1], (1, 0, -1, 1, 1, 1), [0, -1, 1, 0, -1, -1], (1, 0, -1, 1, 1, 0), (1, 0, 1, -1, 0, -1), (1, -1, 1, 0, 1, 0), [0, 0, 0, -1, 0, -1], (0, -1, 0, 0, 0, -1), (0, 1, 1, -1, -1, -1), (1, 0, 1, 0, -1, -1), (1, 0, 0, 0, 1, -1), (-1, -1, -1, 1, -1, -1), [-1, 1, -1, 1, 0, -1], (-1, -1, 0, -1, 0, 1), [0, -1, 1, -1, -1, 0], (-1, 1, 0, 0, 1, 0), (1, -1, -1, -1, -1, 1), (0, 1, -1, 0, 1, -1), [1, -1, 0, 1, -1, -1], [0, -1, -1, -1, 1, 0], [-1, 1, 0, 0, 0, 0], [0, 1, 0, 0, -1, -1], [0, 1, 0, 1, 1, 0], [0, 0, -1, 0, -1, 0], [-1, 1, 1, 0, -1, 0], [1, 0, 1, 1, -1, 1], (-1, -1, 1, 0, 1, 0), (0, -1, 1, 1, 0, -1), [-1, -1, 1, 1, 1, 1], [1, -1, -1, 0, -1, 1], [-1, -1, 0, 0, 1, 0], (1, 0, 1, 0, 1, 1), (1, 0, -1, -1, -1, 0), [0, 1, 0, 1, -1, 1]])

def is_pareto_dominable(alloc, true_combs_base, all_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]


	for comb in  all_combs:
		eq_by_player = [copy(all_zeros) for i in range(players)]

		for i in range(items):
			if alloc[i] != comb[i]:
				eq_by_player[alloc[i]][i] = 1
				eq_by_player[comb[i]][i] = -1

		isPD = True
		isSPD = False
		for player in range(players):
			if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
				isPD = False
				break
			elif is_comb_in_base(eq_by_player[player], true_combs_base[player]):
				isSPD = True
				continue
			anti_comb = reverse_comb(eq_by_player[player])
			if is_comb_in_base(anti_comb, true_combs_base[player]):
				isPD = False
				break
			else:
				isSPD = True

		if isPD and isSPD:
			return True, eq_by_player

	return False, None

def is_pareto_dominated(alloc, true_combs_base, all_combs, good_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0

	bad_combs = {0: set([]), 1: set([]), 2:set([])}



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
			print("HOW MANY: {}".format(how_many))
			return True

	#print("NOT PD")
	print("HOW MANY: {}".format(how_many))

	return False

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

def autocorr(f_votes, tcb, player):
	count_bad = 0
	for f_vote in f_votes:
		try:
			if f_vote[0] == player:
				anti_fvote = tuple(reverse_comb(f_vote[1]))
				if is_comb_in_base(anti_fvote, tcb):
					count_bad += 1
		except Exception as e:
			print("WAT")
			import pdb
			pdb.set_trace()

	return count_bad


def split_mandatory(all_combs):
	mandatory_combs = []
	later_combs = []
	latest_combs = []

	for comb in all_combs:
		counts = [0,0,0]
		counts[0] = len([i for i in filter(lambda x: x==0, comb)])
		counts[1] = len([i for i in filter(lambda x: x==1, comb)])
		counts[2] = len([i for i in filter(lambda x: x==2, comb)])

		counts.sort()
		if counts[:2] == [1,1]:
			mandatory_combs.append(comb)
		elif 1 in counts:
			later_combs.append(comb)
		elif 0 not in counts:
			latest_combs.append(comb)

	return mandatory_combs, later_combs, latest_combs

global leafs
leafs = 0


def exhaustive_solve(allocs, true_combs_base, good_combs, evil_combs, add_log = []):
	global leafs
	#print("Looking into add log of length {}, add_log: {}".format(len(add_log),add_log))
	init_len = len(allocs)
	#print("SAMPLED ALLOCS BEFORE FILTER {}".format(len(allocs)))
	allocs = filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs, evil_combs)
	#print("SAMPLED ALLOCS AFTER PARETO FILTER {}".format(len(allocs)))
	allocs = filter_efx_envious(allocs, true_combs_base, all_combs, good_combs, evil_combs)
	#print("SAMPLED ALLOCS AFTER EFX FILTER {}".format(len(allocs)))

	if len(add_log) == 0:
		print("Number of allocations: {}".format(len(allocs)))

	if len(allocs) == 0:
		print("All allocs filtered!")

		valuations = {0: [], 1: [], 2:[]}

		for player in range(players):
			valuations[player] = generate_valuation(true_combs_base[player])

		print(valuations)
		import pdb
		pdb.set_trace()
		return True

	for alloc in allocs:
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
				anti_key = tuple(reverse_comb(curr_equ))
				if not is_comb_in_base(anti_key, true_combs_base[pair[0]]) and not is_comb_in_base(curr_equ, true_combs_base[pair[0]]):
					allocs_copy1 = copy(allocs)
					allocs_copy2 = copy(allocs)
					copy1_true_combs_base = {0: [], 1: [], 2: []}
					copy2_true_combs_base = {0: [], 1: [], 2: []}
					copy1_good_combs = {0: set([]), 1: set([]), 2: set([])}
					copy1_evil_combs = {0: set([]), 1: set([]), 2: set([])}		
					copy2_good_combs = {0: set([]), 1: set([]), 2: set([])}
					copy2_evil_combs = {0: set([]), 1: set([]), 2: set([])}					
					for i in range(players):
						copy1_true_combs_base[i] = copy(true_combs_base[i])
						copy2_true_combs_base[i] = copy(true_combs_base[i])
						copy1_good_combs[i] = copy(good_combs[i]) 
						copy1_evil_combs[i] = copy(evil_combs[i]) 
						copy2_good_combs[i] = copy(good_combs[i]) 
						copy2_evil_combs[i] = copy(evil_combs[i]) 

					copy1_true_combs_base[pair[0]].append(tuple(curr_equ))
					copy2_true_combs_base[pair[0]].append(tuple(anti_key))

					#print("DIVING IN over alloc {}".format(alloc))

					add_log1 = copy(add_log)
					add_log2 = copy(add_log)

					add_log1 += [tuple([pair[0], curr_equ])]
					add_log2 += [tuple([pair[0], anti_key])]

					return exhaustive_solve(allocs_copy1, copy1_true_combs_base, copy1_good_combs, copy1_evil_combs, add_log1) or exhaustive_solve(allocs_copy2, copy2_true_combs_base, copy2_good_combs, copy2_evil_combs, add_log2)

	#print("Didn't find any equation to add, folding back".format(alloc))
	leafs += 1
	#print("Went through {} equation branches with current branch {}".format(leafs, add_log))
	return False


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
	for comb1 in all_comb1:
		for comb2 in all_comb2:
			for comb3 in all_comb3:

				running_ind += 1

				if comb1.index(2) > comb1.index(3):
					continue
				if comb1.index(4) > comb1.index(5):
					continue
				
				preferences = []

				if running_ind < 9000:
					continue
				for j in range(3):
					if j == 0:
						perm = [0,1] + comb1
					if j == 1:
						perm = [0,2] + comb2
					elif j == 2:
						perm = [0,3] + comb3

					preferences.append(perm)	

				"""eq_options = []

				for pair in all_pairs:
					first = pair[0]
					second = pair[1]
					for i in range(players):
						if i not in pair:
							third = i

					top = copy(preferences[first][:2])
					option1 = copy(preferences[second])
					option2 = copy(preferences[third])
					for elem in top:
						option1.remove(elem)
						option2.remove(elem)

					option1 = option1[:2]

					for elem in option1:
						option2.remove(elem)

					eq_options.append([tuple([second, option1]), tuple([third,option2])])"""


				eq_ind = 0
				for eq_opt in [item for item in product([i for i in range(4)], repeat=6)]:
					eq_ind += 1

					#if running_ind == 3 and eq_ind < 15:
					#	continue

					print("Running ind: {}, Equation ind: {}/{}".format(running_ind, eq_ind,4096))
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


					pair_ind = 0
					move_on = True

					for pair in all_pairs:

						first = pair[0]
						second = pair[1]
						for i in range(players):
							if i not in pair:
								third = i

						second_alloc = [preferences[second][1]]

						third_alloc = copy(preferences[third])
						third_alloc.remove(0)
						third_alloc.remove(preferences[second][1])
						if preferences[second][2] == preferences[third][1]:
							third_alloc.remove(preferences[second][3])
							second_alloc.append(preferences[second][3])
						else:
							third_alloc.remove(preferences[second][2])
							second_alloc.append(preferences[second][2])

						if eq_opt[pair_ind] == 0:
							pass

						elif eq_opt[pair_ind] == 1:
							third_alloc = third_alloc[1:]
							third_alloc.append(second_alloc[0])
							# add the 2<-->56 

							eq = [0] * 6
							eq[third_alloc[2]] = 1
							eq[third_alloc[0]] = -1
							eq[third_alloc[1]] = -1
							anti_eq = reverse_comb(eq)

							if not is_comb_in_base(anti_eq, true_combs_base[second]):
								true_combs_base[second].append(eq)
								good_combs[second].add(tuple(eq))
								evil_combs[second].add(tuple(anti_eq))
							else:
								print("ooh")
								move_on = False
								break

							if not is_comb_in_base(eq, true_combs_base[third]):
								true_combs_base[third].append(anti_eq)
								good_combs[third].add(tuple(anti_eq))
								evil_combs[third].add(tuple(eq))
							else:
								print("ooh")
								move_on = False
								break	
						
						elif eq_opt[pair_ind] == 2:
							third_alloc = third_alloc[1:]
							third_alloc.append(second_alloc[1])		
							# add the 4<-->56 

							eq = [0] * 6
							eq[third_alloc[2]] = 1
							eq[third_alloc[0]] = -1
							eq[third_alloc[1]] = -1
							
							anti_eq = reverse_comb(eq)

							if not is_comb_in_base(anti_eq, true_combs_base[first]):
								true_combs_base[first].append(eq)
								good_combs[first].add(tuple(eq))
								evil_combs[first].add(tuple(anti_eq))
							else:
								print("ooh")
								move_on = False
								break	

							if not is_comb_in_base(eq, true_combs_base[second]):
								true_combs_base[second].append(anti_eq)
								good_combs[second].add(tuple(anti_eq))
								evil_combs[second].add(tuple(eq))
							else:
								print("ooh")
								move_on = False
								break	

						elif eq_opt[pair_ind] == 3:
							# add the 1<-->24
							eq = [0] * 6
							eq[0] = 1
							eq[second_alloc[0]] = -1
							eq[second_alloc[1]] = -1
							anti_eq = reverse_comb(eq)

							if not is_comb_in_base(anti_eq, true_combs_base[second]):
								true_combs_base[second].append(eq)
								good_combs[second].add(tuple(eq))
								evil_combs[second].add(tuple(anti_eq))
							else:
								print("ooh")
								move_on = False
								break

							if not is_comb_in_base(eq, true_combs_base[third]):
								true_combs_base[third].append(anti_eq)
								good_combs[third].add(tuple(anti_eq))
								evil_combs[third].add(tuple(eq))

							else:
								print("ooh")
								move_on = False
								break

						dominating_two = []

						for elem in preferences[first]:
							if elem in third_alloc:
								dominating_two.append(elem)
								if len(dominating_two) == 2:
									break

						eq = [0] * 6
						eq[0] = 1
						eq[dominating_two[0]] = -1
						eq[dominating_two[1]] = -1
						true_combs_base[first].append(eq)
						good_combs[first].add(tuple(eq))
						anti_eq = reverse_comb(eq)
						evil_combs[first].add(tuple(anti_eq))

						pair_ind += 1

					"""for i in range(6):
						j, rel = eq_options[i][eq_opt[i]]
						eq = [0] * 6
						eq[0] = -1
						eq[rel[0]] = 1
						eq[rel[1]] = 1
						true_combs_base[j].append(eq)
						good_combs[j].add(tuple(eq))
						anti_eq = reverse_comb(eq)
						evil_combs[j].add(tuple(anti_eq))"""

					if move_on == False:
						continue

					# Add the 3-1 envy
					eq = [0] * 6
					eq[0] = -1
					eq[3] = 1
					eq[4] = 1
					eq[5] = 1

					anti_key = reverse_comb(eq)

					for i in range(players):
						if not is_comb_in_base(anti_key, true_combs_base[i]):
							true_combs_base[i].append(eq)
							good_combs[i].add(tuple(eq))
							anti_eq = reverse_comb(eq)
							evil_combs[i].add(tuple(anti_eq))
						else:
							print("ooh")
							move_on = False
							break


					if move_on == False:
						continue


					copy_good_combs = {0: set([]), 1: set([]), 2: set([])}
					copy_evil_combs = {0: set([]), 1: set([]), 2: set([])}					
					for i in range(players):
						copy_good_combs[i] = copy(good_combs[i]) 
						copy_evil_combs[i] = copy(evil_combs[i]) 

					leafs = 0
					exhaustive_solve(allocs, true_combs_base, copy_good_combs, copy_evil_combs)



